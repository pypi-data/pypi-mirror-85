"""Provide rasterization routines."""
from typing import List

import numpy as np

from fibomat.shapes.arc import Arc
from fibomat.shapes.line import Line
from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.shapes.shape import Shape
from fibomat.shapes.arc_spline import ArcSplineCompatible, ArcSpline
from fibomat import linalg
from fibomat.curve_tools.intersections import curve_intersections
from fibomat.boundingbox import BoundingBox


def _rasterize_arc_spline(curve: ArcSpline, pitch: float) -> RasterizedPoints:
    # pylint: disable=invalid-name,too-many-locals

    pitch = float(pitch)
    # n_points = int(curve.length / pitch) + 1

    points = []

    i_points = 0
    offset = 0.
    for segment in curve.segments:
        if isinstance(segment, Arc):
            arc: Arc = segment

            offset_angle = offset / arc.radius
            pitch_angle = pitch / arc.radius

            if offset_angle <= arc.theta:
                points_on_arc = int((arc.theta - offset_angle) / pitch_angle) + 1

                if np.isclose((arc.theta - offset_angle) / pitch_angle - points_on_arc - 1, 0.):
                    points_on_arc += 1

                if not arc.sweep_dir:
                    pitch_angle *= -1.
                    arc_start_angle = arc.start_angle - offset_angle
                else:
                    arc_start_angle = arc.start_angle + offset_angle

                center = np.array(arc.center)
                theta = pitch_angle*np.arange(points_on_arc)

                points.append(
                    center + arc.radius * np.column_stack(
                        (np.cos(theta + arc_start_angle), np.sin(theta + arc_start_angle))
                    )
                )

                i_points += points_on_arc
                offset = pitch - (arc.length - offset - (len(theta)-1) * pitch)
            else:
                offset -= arc.length

        elif isinstance(segment, Line):
            line: Line = segment
            if offset <= line.length:
                direction = (line.end - line.start).normalized()

                start = line.start + direction * offset

                points_on_line = int((line.length-offset) / pitch) + 1

                direction = np.array(direction)
                start = np.array(start)

                t = pitch * np.arange(points_on_line)
                # points[i_points:i_points+points_on_line, :2] = start + np.repeat(t[None, :], 2, axis=0).T * direction
                points.append(start + np.repeat(t[None, :], 2, axis=0).T * direction)
                # points[i_points:i_points+points_on_line, 2] = 1.

                i_points += points_on_line
                offset = pitch - (line.length - t[-1] - offset)
            else:
                offset -= line.length
        else:
            raise RuntimeError(f'Cannot rasterize segment type {segment.__class__.__name__}')

    # assert i_points == n_points
    dwell_points = np.ones(shape=(i_points, 3))
    dwell_points[:, :2] = np.concatenate(points)

    return RasterizedPoints(dwell_points, curve.is_closed)


def rasterize(curve: Shape, pitch: float) -> RasterizedPoints:
    """Rasterize the outline of a Shape with a given pitch uniformly.

    For this, the shape must be convertible to an ArcSpline or must have a `rasterize` method expecting the pitch as
    input.

    Args:
        curve (Shape): curve
        pitch (float): pitch (spacing of points)

    Returns:
        RasterizedPoints

    Raises:
        ValueError: Raised if curve is no ArcSpline, ArcSplineCompatible or not have a `rasterize` method.
    """
    if isinstance(curve, ArcSpline):
        return _rasterize_arc_spline(curve, pitch)

    if raster_method := getattr(curve, 'rasterize', None):
        return raster_method(curve, pitch)

    if isinstance(curve, ArcSplineCompatible):
        return _rasterize_arc_spline(curve.to_arc_spline(), pitch)

    raise ValueError(f'Cannot rasterize the passed object of type {curve.__class__}.')


def fill_with_lines(curve: ArcSpline, pitch: float, angle: float) -> List[ArcSpline]:
    """Fill a closed shape with lines which are rotated by `angle`-

    Args:
        curve (ArcSpline): closed curve to be filled.
        pitch (float): distance between lines.
        angle (float): rotation angle of lines with respect to x-axis.

    Returns:
        List[ArcSpline]

    Raises:
        ValueError: Raised if angle < 0 or angle > pi.
        NotImplementedError: Raised if some kind of singularities occur. This can be fixed (probably) if the shape is
                             rotated.
    """
    # pylint: disable=invalid-name,too-many-locals

    if not (0 <= angle <= np.pi):
        raise ValueError('angle < 0 or angle > pi')

    center = curve.center

    # we apply a random shift to minimize some of the problems below (hopefully)
    # is it a solution? NO!
    # TODO: find a way to get rid of intersection-calculation glitches
    # random_shift = np.random.uniform(-1, 1, size=2)
    random_shift = (0, 0)

    if angle <= np.pi/2:
        curve = curve.transformed(
            linalg.translate(-center) | linalg.rotate(-angle) | linalg.translate(random_shift)
        )
    else:
        curve = curve.transformed(
            linalg.translate(-center) | linalg.rotate(np.pi-angle) | linalg.translate(random_shift)
        )

    extend = 2.1 * pitch

    bbox_curve = curve.bounding_box

    bbox = BoundingBox(bbox_curve.lower_left - (extend, extend), bbox_curve.upper_right + (extend, extend))

    bbox_left = bbox.lower_left.x
    bbox_right = bbox.upper_right.x
    bbox_top = bbox.upper_right.y
    # bbox_bottom = bbox.center.y - bbox.height / 2

    y = np.arange(-bbox.height / 2, bbox.height / 2, pitch)

    ny = len(y)

    # it's not properly working for
    # circle = Curve([Circle(r=1)])
    # _, mask2 = make_raster(circle, 0.2, 0.2, 0., 2)
    # mask2.print()
    # because of numreics.
    # TODO: find a solution
    line = ArcSpline([(bbox_left, bbox_top, 0), (bbox_right, bbox_top, 0)], False)

    fill_lines = []

    for _ in range(ny):
        cl_inter = curve_intersections(curve, line)

        # TODO: handle case, if cl_inter contains more than one coincidence
        assert len(cl_inter['coincidences']) < 2

        if len(cl_inter['intersections']) > 1:
            if len(cl_inter['intersections']) % 2 != 0:
                # this could be the case if:
                #          x           x
                #        xxxxx       xxxx
                #      xxxxxxxx   xxxxxxxxx
                #     xxxxxxxxxx xxxxxxxxxxxx
                # ----xxxxxxxxxxPxxxxxxxxxxxx-------
                #    xxxxxxxxxxxxxxxxxxxxxxxxxx
                # Problem is caused by P.
                # TODO: fixit
                raise NotImplementedError

            # if len(cl_inter['intersections']) == 2, it could the the case that the intersection points are singular
            # and do not enclose an inner part
            # -----x-----------x------    <- problem
            #    xxxxx       xxxx
            #  xxxxxxxx   xxxxxxxxx
            # xxxxxxxxxxxxxxxxxxxxxxx
            # TODO: fix it

            # Another problem:
            # len(cl_inter['intersections']) % 2 == True but all also middle segment is in curve included.
            #
            #            xxxxx       xxxx       xxxxx
            #          xxxxxxxx   xxxxxxxxx   xxxxxxxx
            #         xxxxxxxxxx xxxxxxxxxxx xxxxxxxxxx
            # --------xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx---------- <- problem
            # TODO: fixit

            cl_inter_x = [inter['pos'][0] for inter in cl_inter['intersections']]
            cl_inter_y = [inter['pos'][1] for inter in cl_inter['intersections']]

            assert np.allclose(cl_inter_y, cl_inter_y[0])

            cl_inter_x.sort()

            const_y = cl_inter_y[0]
            for i in range(0, len(cl_inter_x), 2):
                fill_line = ArcSpline([(cl_inter_x[i], const_y, 0.), (cl_inter_x[i+1], const_y, 0.)], False)
                # fill_line.rotate(angle, origin=center).translate(center)
                fill_lines.append(
                    fill_line.transformed(
                        linalg.translate(center-random_shift) | linalg.rotate(angle, origin=center)
                    )
                )

        line = line.translated((0, -pitch))

    return fill_lines
