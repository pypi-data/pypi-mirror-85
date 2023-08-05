
from typing import Union

import numpy as np

from fibomat.shapes.line import Line
from fibomat.shapes.arc import Arc
from fibomat.shapes.arc_spline import ArcSpline
from fibomat.curve_tools.intersections import curve_intersections
from fibomat.curve_tools.offset import offset_with_islands, offset
from fibomat.linalg import angle_between, Vector
from fibomat.linalg.helpers import GeomLine
from fibomat.utils.math import mod_2pi


def _vec_is_enclosed(a: Vector, x: Vector, y: Vector):
    angle_a = a.angle_about_x_axis
    angle_x = x.angle_about_x_axis
    angle_y = y.angle_about_x_axis

    for i in range(3):
        if angle_x <= angle_a <= angle_y:
            return True
        if angle_x >= angle_a >= angle_y:
            return True

        angle_a += np.pi/4
        angle_x += np.pi/4
        angle_y += np.pi/4

        angle_a = mod_2pi(angle_a)
        angle_x = mod_2pi(angle_x)
        angle_y = mod_2pi(angle_y)

    return False


# https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon
def _offset_factor(arc_1: Arc, arc_2: Arc):
    arc_1_rev_tan = -arc_1.unit_tangent_end
    sec_arc_1 = arc_1.start - arc_1.end

    arc_2_tan = arc_2.unit_tangent_start

    intersection_vec = (arc_1_rev_tan + arc_2_tan) / 2

    # if intersection_vec.angle_about_x_axis >= arc_1_rev_tan.angle_about_x_axis >= sec_arc_1.angle_about_x_axis \
    #    or intersection_vec.angle_about_x_axis <= arc_1_rev_tan.angle_about_x_axis <= sec_arc_1.angle_about_x_axis:
    if _vec_is_enclosed(arc_1_rev_tan, intersection_vec, sec_arc_1):
        if arc_1.bulge > 0:
            return -1
        else:
            return 1
    else:
        if arc_1.bulge < 0:
            return -1
        else:
            return 1


def _smoothing_arc_center(first_segment: Arc, second_segment: Arc, radius: float):
    fac = _offset_factor(first_segment, first_segment)

    assert radius > 0

    offsetted = offset(
        ArcSpline.from_segments([first_segment, second_segment]),
        _offset_factor(first_segment, first_segment) * radius, '')

    found_arc_center = False

    #try to get arc center from kinks
    # sometimes offsetting artefacts occur, so we have to loop here and  try to filter out the artifacts
    for of in offsetted:
        kinks = of.kinks()
        if len(kinks) > 1:
            raise RuntimeError
        if len(kinks) == 1:
            arc_center = of.vertices[kinks[0]][:2]
            corresponding_curve = of

            if found_arc_center:
                raise RuntimeError

            found_arc_center = True

    if not found_arc_center:
        # raise RuntimeError
        return None

    offsetted_segments = corresponding_curve.segments
    if len(offsetted_segments) != 2:
        raise NotImplementedError

    return arc_center, *offsetted_segments


def smooth(spline: ArcSpline, radius: float) -> ArcSpline:
    """Smooth out all kinks in `spline` with arcs.

    Args:
        spline (ArcSpline): spline
        radius (float): smoothing radius.

    Returns:
        ArcSpline
    """
    # def _offset_segment(segment: Union[Line, Arc]):
    #     if isinstance(segment, Line):
    #         raise NotImplementedError
    #     else:
    #         return Arc(
    #             radius=segment.radius + dir_fac * radius,
    #             start_angle=segment.start_angle,
    #             end_angle=segment.end_angle,
    #             sweep_dir=segment.sweep_dir,
    #             center=segment.center
    #         )

    kinks = spline.kinks()

    if kinks:

        vertices = []
        last_vertex_after_kink = 0

        for i_kink, kink in enumerate(kinks):
            if kink > 0:
                vertices.extend(spline.vertices[last_vertex_after_kink:kink-1])


            # WTF WITH THE POP VERTICES !? but it works ..
            first_segment, second_segment = spline.segments_at_vertex(kink)
            if kink - last_vertex_after_kink == 1:
                if not np.isclose(vertices[-1][2], 0.):
                    first_segment = Arc.from_bulge(vertices[-1][:2], spline.vertices[kink][:2], vertices[-1][2])
                    vertices.pop()
                else:
                    raise NotImplementedError
            else:
                # if vertices:
                #     vertices.pop()
                pass

            if kink == len(spline.vertices) - 1:
                if not np.isclose(vertices[0][2], 0.):
                    second_segment = Arc.from_bulge(vertices[0][:2], vertices[1][:2], vertices[0][2])
                else:
                    raise NotImplementedError


            # get offset direction

            # if not isinstance(first_segment, Arc) or not isinstance(second_segment, Arc):
            #     raise NotImplementedError
            #
            # first_segment_offsetted = _offset_segment(first_segment)
            # second_segment_offsetted = _offset_segment(second_segment)
            #
            # intersection = curve_intersections(
            #     ArcSpline.from_shape(first_segment_offsetted), ArcSpline.from_shape(second_segment_offsetted)
            # )['intersections']
            #
            # if len(intersection) != 1:
            #     # TODO: we have to include more segments around the kink and  try again
            #     raise NotImplementedError
            #
            # center_smoothing_arc = intersection[0]['pos']

            smoothing_arc_props = _smoothing_arc_center(first_segment, second_segment, radius)

            if smoothing_arc_props:

                center_smoothing_arc, first_segment_offsetted, second_segment_offsetted = smoothing_arc_props


                if isinstance(first_segment_offsetted, Arc):
                    angle = angle_between(
                        first_segment.center - first_segment.end,
                        first_segment.center - center_smoothing_arc
                    )

                    new_arcs = first_segment.split_at(first_segment.theta - angle)
                    assert len(new_arcs) == 2

                    new_first_segment = new_arcs[0]
                    start_smoothing_arc = new_first_segment.end
                else:
                    raise NotImplementedError

                if isinstance(second_segment_offsetted, Arc):
                    angle = angle_between(
                        second_segment.center - second_segment.start,
                        second_segment.center - center_smoothing_arc
                    )

                    new_arcs = second_segment.split_at(angle)
                    assert len(new_arcs) == 2

                    new_second_segment = new_arcs[1]
                    end_smoothing_arc = new_second_segment.start
                else:
                    raise NotImplementedError

                smoothing_arc = Arc.from_points_center(
                    start_smoothing_arc, end_smoothing_arc, center_smoothing_arc, sweep_dir=not first_segment.sweep_dir
                )

                new = [
                    (*new_first_segment.start, new_first_segment.bulge),
                    (*smoothing_arc.start, smoothing_arc.bulge),
                    (*new_second_segment.start, new_second_segment.bulge)
                ]

                vertices.extend(new)

            else:
                # if popped_vertex:
                #     vertices.append(popped_vertex)
                # vertices.append(spline.vertices[kink])

                # we give up here..
                return spline

            last_vertex_after_kink = kink


            # points.append()
        if kinks[-1] == len(spline) - 1:
            vertices.pop(0)
            # last_vertex = (*vertices[-1][:2], first_vertex[2])
            # vertices[-1] = last_vertex
            # vertices[0] = (*vertices[0][:2], first_vertex_bulge)

        return ArcSpline(np.array(vertices), spline.is_closed)

    return spline
