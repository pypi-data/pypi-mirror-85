from typing import Tuple, Sequence, Optional

import numpy as np

from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, scale_to, has_length_dim, QuantityType, scale_factor, LengthQuantity
from fibomat.dimensioned_object import DimObjLike, DimObj
from fibomat.shapes.arc_spline import ArcSplineCompatible, ArcSpline
from fibomat.mill import Mill
from fibomat.curve_tools import inflate, deflate, rasterize, smooth
from fibomat.optimize import optimize_curve


class ContourParallel(RasterStyle):

    _inwards = 'inwards'
    _outwards = 'outwards'

    def __init__(
        self,
        pitch: LengthQuantity,
        offset_pitch: LengthQuantity,
        offset_direction: str,
        alternate_direction: bool,
        start_direction: str,
        include_original_curve: bool,
        optimize: bool,
        *, offset_steps: Optional[int] = None, offset_distance: Optional[LengthQuantity] = None, smooth_radius: Optional[LengthQuantity] = None
    ):
        if not has_length_dim(pitch):
            raise ValueError('pitch must have [length] as dimension')
        self._pitch = pitch

        if not has_length_dim(offset_pitch):
            raise ValueError('offset_pitch must have [length] as dimension')

        if offset_pitch <= 0.:
            raise ValueError('offset_pitch <= 0.')
        self._offset_pitch = offset_pitch

        if offset_direction not in [self._inwards, self._outwards]:
            raise ValueError(f'offset_direction must be "{self._inwards}" or "{self._outwards}".')

        self._offset_direction = offset_direction
        self._offset_steps = offset_steps
        self._offset_distance = offset_distance

        if start_direction not in [self._inwards, self._outwards]:
            raise ValueError(f'start_direction must be "{self._inwards}" or "{self._outwards}".')
        self._start_direction = start_direction

        self._alternate_direction = alternate_direction
        self._include_original_curve = include_original_curve

        self._smooth_radius = smooth_radius

        self._optimize = optimize

    @property
    def dimension(self) -> int:
        return 2

    def _do_smooth(self, spline: ArcSpline, curve_unit: LengthUnit):
        if self._smooth_radius:
            return smooth(spline, self._smooth_radius.to(curve_unit).m)
        else:
            return spline

    def _gen_offset_curves(self, base_curve: ArcSpline, curve_unit: LengthUnit) -> Sequence[ArcSpline]:

        curves = []
        if self._include_original_curve:
            curves.append(base_curve)

        if self._offset_direction == self._inwards:
            curves.extend(deflate(
                base_curve,
                self._offset_pitch.to(curve_unit).m,
                n_steps=self._offset_steps,
                distance=self._offset_distance.to(curve_unit).m if self._offset_distance else None
            ))

            if self._start_direction == self._outwards:
                curves = list(reversed(curves))

        else:
            curves.extend(inflate(
                base_curve,
                self._offset_pitch.to(curve_unit).m,
                n_steps=self._offset_steps,
                distance=self._offset_distance.to(curve_unit).m if self._offset_distance else None
            ))

            if self._start_direction == self._inwards:
                curves = list(reversed(curves))

        return [self._do_smooth(curve, curve_unit) for curve in curves]

        # curves: List[shapes.Curve] = [base_curve]
        #
        # offsetted = [base_curve]
        #
        # if self._offset_direction == self._inwards and self._offset_steps == self._inf_steps:
        #     while offsetted:
        #         for curve in offsetted:
        #             offsetted = curve_tools.offset(curve, self._offset_pitch.m, self._offset_direction)
        #             curves.extend(offsetted)
        # else:
        #     for step in range(self._offset_steps):
        #         for curve in offsetted:
        #             offsetted = curve_tools.offset(curve, self._offset_pitch.m, self._offset_direction)
        #             if not offsetted:
        #                 break
        #             curves.extend(offsetted)
        # return curves

    def rasterize(
        self,
        dim_shape: DimObjLike[ArcSplineCompatible, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:

        def print_optimize_result(alpha, flux_matrix, nominal_flux):
            print('mean_alpha =', np.mean(alpha))
            print('std_alpha =', np.std(alpha))
            print('min_alpha = ', np.min(alpha))
            print('max_alpha = ', np.max(alpha))

            flux = flux_matrix @ alpha
            print('mean_flux =', np.mean(flux))
            print('std_flux =', np.std(flux))
            print('min_flux = ', np.min(flux))
            print('max_flux = ', np.max(flux))
            print('nominal_flux =', nominal_flux)

        dim_shape = DimObj.create(dim_shape)

        curves = self._gen_offset_curves(dim_shape.obj, dim_shape.unit)

        if self._optimize:
            nominal_flux = mill.beam.nominal_flux_per_spot_on_line(self._pitch).to('ions / nm**2 / µs')
            rasterized_curves = []

            hint = None

            for i_curve, curve in enumerate(curves):
                # if i_curve % 10 == 0:
                #     hint = None

                print(i_curve, '/', len(curves))

                dwell_points, hint, flux_matrix = optimize_curve((curve, dim_shape.unit), self._pitch, mill.beam, nominal_flux, hint, info=True)
                print_optimize_result(dwell_points[:, 2], flux_matrix, nominal_flux)

                # if i_curve % 10 == 0:
                #     import matplotlib.pyplot as plt
                #     plt.plot(flux_matrix @ dwell_points[:, 2], 'x')
                #     plt.show()
                #     plt.plot(dwell_points[:, 2], 'x')
                #     plt.show()

                rasterized_curves.append(RasterizedPoints(dwell_points, dim_shape.obj.is_closed))

        else:
            rasterized_curves = [rasterize(curve, self._pitch.to(dim_shape.unit).m) for curve in curves]

        points = RasterizedPoints.merged(rasterized_curves)

        points._dwell_points[:, 2] *= mill.dwell_time.to(out_time_unit).m
        points._dwell_points[:, :2] *= scale_factor(out_length_unit, dim_shape.unit)

        if mill.repeats != 1:
            if self._alternate_direction:
                # points_reversed = RasterizedPoints.merged(list(reversed(rasterized_curves)))
                points_reversed = RasterizedPoints(points._dwell_points[::-1], is_closed=points.is_closed)
                print('alternating')

                points_to_merge = []
                toggle = False
                for i in range(mill.repeats):
                    if not toggle:
                        points_to_merge.append(points)
                    else:
                        points_to_merge.append(points_reversed)

                    toggle = not toggle

                return RasterizedPoints.merged(points_to_merge)
            else:
                return RasterizedPoints.merged(rasterized_curves*mill.repeats)

        return points

    def explode(
        self,
        dim_shape: DimObjLike[ArcSplineCompatible, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> Sequence[Tuple[ArcSpline, RasterStyle]]:
        dim_shape = DimObj.create(dim_shape)

        curves = self._gen_offset_curves(dim_shape.obj, dim_shape.unit)
