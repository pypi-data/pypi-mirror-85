from typing import Dict, List, Any, Optional, Union
import enum

import numpy as np
import bokeh.palettes as bp
import bokeh.colors as bc

from fibomat import pattern
from fibomat import units
from fibomat import mill
from fibomat import linalg
from fibomat import shapes
from fibomat import curve_tools
# import fibomat.raster_styles as raster_styles


# @enum.unique
# enum.Enum
class ShapeType:
    SPOT = 'spot'
    NON_FILLED_CURVE = 'non_filled_curve'
    FILLED_CURVE = 'filled_curve'
    SITE = 'site'


_i_color_cycle = 0


class BokehSite:
    # plot_data_keys: List[str] = {
    #     'x', 'y',
    #     'left', 'right', 'top', 'bottom',
    #     'width', 'height', 'angle',
    #     'r', 'a', 'b',
    #     'start_angle', 'end_angle',
    #     'site', 'glyph_type',
    #     'color', 'fill_alpha', 'hatch_pattern',
    #     'mill', 'raster_style', 'description', 'label'
    # }

    plot_data_keys: List[str] = {
        'x', 'y', 'x_hole', 'y_hole',
        'site_id', 'shape_type', 'shape_prop', 'raster_style', 'mill',
        'color', 'fill_alpha', 'hatch_pattern', 'description'
    }

    def __init__(
            self,
            site_index: int,
            plot_unit: units.UnitType,
            center: linalg.Vector,
            site_unit: units.UnitType,
            rasterize_pitch: units.QuantityType,
            cycle_colors: Optional[bool] = False,
            fov: Optional[linalg.Vector] = None,
            description: Optional[str] = None,
    ):
        self._plot_data: Dict[str, List[Any]] = {key: [] for key in self.plot_data_keys}

        s = units.scale_factor(plot_unit, site_unit)

        self._plot_unit: units.UnitType = plot_unit
        self._center: linalg.Vector = s*center
        self._fov: linalg.Vector = s*fov if fov else None

        self._rasterize_pitch = rasterize_pitch # units.Q_('.0001 µm')

        # self._side_index = site_index
        if cycle_colors:
            global _i_color_cycle
            print(_i_color_cycle)
            self._colors = {
                'shape': bp.YlGnBu9[_i_color_cycle % len(bp.YlGnBu9)],
                'shape_alpha': .25,
                'site': bp.all_palettes['Colorblind'][4][0],
                'site_alpha': 0.25 / 2,
                'other': bp.all_palettes['Colorblind'][4][2],
                'other_alpha': .25
            }

            _i_color_cycle += 1
        else:
            self._colors = {
                'shape': bp.all_palettes['Colorblind'][4][1],
                'shape_alpha': .25,
                'site': bp.all_palettes['Colorblind'][4][0],
                'site_alpha': 0.25 / 2,
                'other': bp.all_palettes['Colorblind'][4][2],
                'other_alpha': .25
            }

        if self._fov is not None:
            self._site_description: str = f'Site {site_index}, fov=({self._fov.x}, {self._fov.y}) {self._plot_unit:~P}'
            self._site_description += (', ' + str(description)) if description else ''
            self._label: str = self._site_description

            points = np.array(shapes.Rect(width=self._fov.x, height=self._fov.y, theta=0, center=self._center).corners)

            self._add_plot_data(
                # x=list(points[:, 0]), y=list(points[:, 1]),
                x=[[list(points[:, 0])]], y=[[list(points[:, 1])]],
                site_id=str(self._label), shape_type=ShapeType.SITE, shape_prop='Site',
                raster_style='', mill='',
                color=self._colors['site'], fill_alpha=self._colors['site_alpha'],
                description=self._site_description
            )

            # self._add_plot_data(
            #     x=self._center.x, y=self._center.y,
            #     width=self._fov.x, height=self._fov.y, angle=0.,
            #     glyph_type='site_rect',
            #     color=self._colors['site'], fill_alpha=self._colors['site_alpha'],
            #     description=self._site_description, label=self._label
            # )
        else:
            # it's a annotation layer
            self._site_description = 'Annotations'
            self._label: str = self._site_description
            self._colors['shape'] = bp.all_palettes['Colorblind'][4][3]

    def _add_plot_data(self, **kwargs):
        # data = locals()
        #for key in self.plot_data_keys:
        #    self._plot_data[key].append(data[key])
        # x = None, y = None,
        # left = None, right = None, top = None, bottom = None,
        # width = None, height = None, angle = None,
        # r = None, a = None, b = None,
        # start_angle = None, end_angle = None,
        # site = None, glyph_type = None,
        # color = None, fill_alpha = None, hatch_pattern = None,
        # mill = None, description = None, label = None
        for key in self.plot_data_keys:
            # if key not in self.plot_data_keys:
            #     raise KeyError('unknonw plot data key')
            try:
                self._plot_data[key].append(kwargs[key])
            except KeyError:
                self._plot_data[key].append(None)

    @property
    def plot_data(self) -> Dict[str, List[Any]]:
        return self._plot_data

    def spot(self, ptn: pattern.Pattern[shapes.Spot]) -> None:
        s = units.scale_factor(self._plot_unit, ptn.dim_shape.unit)
        shape: shapes.Spot = ptn.dim_shape.obj

        self._add_plot_data(
            x=self._center.x + s * shape.center.x, y=self._center.y + s * shape.center.y,
            site_id=str(self._label), shape_type=ShapeType.SPOT, shape_prop=str(ptn.dim_shape.obj),
            raster_style=str(ptn.raster_style), mill=str(ptn.shape_mill),
            color=self._colors['shape'],
            description=f'Pattern: {ptn.description} | Shape: {ptn.dim_shape.obj.description}',
        )

        # self._add_plot_data(
        #     x=self._center.x + s * shape.center.x, y=self._center.y + s * shape.center.y,
        #     site=self._label, glyph_type='spot',
        #     color=self._colors['shape'],
        #     mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
        # )

    def _segmentize_pattern(self, ptn: pattern.Pattern) -> np.ndarray:
        curve = shapes.ArcSpline.from_shape(ptn.dim_shape.obj)
        s = units.scale_factor(self._plot_unit, ptn.dim_shape.unit)

        points = []

        for segment in curve.segments:
            if isinstance(segment, shapes.Line):
                segment: shapes.Line
                points.append([np.asarray(segment.start)])
            elif isinstance(segment, shapes.Arc):
                segment: shapes.Arc
                arc_points = curve_tools.rasterize(
                    shapes.ArcSpline.from_shape(segment), units.scale_to(ptn.dim_shape.unit, self._rasterize_pitch)
                ).dwell_points[:, :2]
                points.append(arc_points)
            else:
                raise RuntimeError

        if curve.segments:
            points.append([np.asarray(curve.segments[-1].end)])

            # if curve.is_closed:
            #     points.append([np.asarray(curve.segments[0].start)])

        points = np.concatenate(points).reshape(-1, 2)
        points *= s
        points += self._center

        return np.concatenate(points).reshape(-1, 2)

    def non_filled_curve(self, ptn: pattern.Pattern):
        points = self._segmentize_pattern(ptn)

        self._add_plot_data(
            x=list(points[:, 0]), y=list(points[:, 1]),
            site_id=str(self._label), shape_type=ShapeType.NON_FILLED_CURVE, shape_prop=str(ptn.dim_shape.obj),
            raster_style=str(ptn.raster_style), mill=str(ptn.shape_mill),
            color=self._colors['shape'],
            description=f'Pattern: {ptn.description} | Shape: {ptn.dim_shape.obj.description}',
        )

    def filled_curve(self, ptn: pattern.Pattern):
        points = self._segmentize_pattern(ptn)

        self._add_plot_data(
            # x=list(points[:, 0]), y=list(points[:, 1]),
            x=[[list(points[:, 0])]], y=[[list(points[:, 1])]],
            site_id=str(self._label), shape_type=ShapeType.FILLED_CURVE, shape_prop=str(ptn.dim_shape.obj),
            raster_style=str(ptn.raster_style), mill=str(ptn.shape_mill),
            color=self._colors['shape'], fill_alpha=self._colors['shape_alpha'],
            description=f'Pattern: {ptn.description} | Shape: {ptn.dim_shape.obj.description}',
        )


    # def line(self, ptn: pattern.Pattern[shapes.Line]) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Line = ptn.dim_shape[0]
    #
    #     x_start = shape.start.x * s + self._center.x
    #     y_start = shape.start.y * s + self._center.y
    #     x_end = shape.end.x * s + self._center.x
    #     y_end = shape.end.y * s + self._center.y
    #
    #     self._add_plot_data(
    #         x=[x_start, x_end], y=[y_start, y_end],
    #         site=self._label, glyph_type='line',
    #         color=self._colors['shape'],
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # def polyline(self, ptn: pattern.Pattern[shapes.Polyline]) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Polyline = ptn.dim_shape[0]
    #
    #     points = shape.points * s + self._center
    #     points = np.array(points)
    #
    #     self._add_plot_data(
    #         x=points[:, 0], y=points[:, 1],
    #         site=self._label, glyph_type='polyline',
    #         color=self._colors['shape'],
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # # def arc(self, pattern: pattern.Pattern[shapes.Arc, mill.CurveMill]) -> None:
    # #     s = units.scale_factor(self._plot_unit, pattern.shape_unit)
    # #     shape: shapes.Arc = pattern.shape
    # #
    # #     if pattern.shape.sweep_dir:
    # #         start_angle = shape.start_angle
    # #         end_angle = shape.end_angle
    # #     else:
    # #         start_angle = shape.end_angle
    # #         end_angle = shape.start_angle
    # #
    # #     self._add_plot_data(
    # #         x=shape.center.x * s + self._center.x, y=shape.center.y * s + self._center.y,
    # #         r=shape.r * s, start_angle=start_angle, end_angle=end_angle,
    # #         site=self._label, glyph_type='arc',
    # #         color=self._colors['shape'],
    # #         mill=str(pattern.mill), label=self._label
    # #     )
    #
    # def polygon(self, ptn: pattern.Pattern[shapes.Polygon]) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Polygon = ptn.dim_shape[0]
    #
    #     points = shape.points*s+self._center
    #     points = np.array(points)
    #     points = np.append(points, np.asarray([points[0]]), axis=0)
    #
    #     self._add_plot_data(
    #         x=[[points[:, 0] + self._center.x]], y=[[points[:, 1] + self._center.y]],
    #         site=self._label, glyph_type='polygon',
    #         color=self._colors['shape'], fill_alpha=self._colors['shape_alpha'] if isinstance(ptn.raster_style, raster_styles.AreaStyle) else 0.,
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # # TODO: simplify polygon/polyline for plotting!
    #
    # def rasterized_curve_open(
    #         self,
    #         ptn: pattern.Pattern[rasterizing.RasterizedPoints],
    #         glyph_type
    # ) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: rasterizing.RasterizedPoints = ptn.dim_shape[0]
    #
    #     points = shape.dwell_points[:, :2] * s
    #
    #     self._add_plot_data(
    #         x=points[:, 0] + self._center.x, y=points[:, 1] + self._center.y,
    #         site=self._label, glyph_type=glyph_type,
    #         color=self._colors['shape'],
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # def rasterized_curve_closed(
    #         self,
    #         ptn: pattern.Pattern[rasterizing.RasterizedPoints],
    #         glyph_type: str
    # ) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: rasterizing.RasterizedPoints = ptn.dim_shape[0]
    #
    #     points = shape.dwell_points[:, :2] * s
    #
    #     points = np.append(points, np.asarray([points[0]]), axis=0)
    #     self._add_plot_data(
    #         x=[[points[:, 0] + self._center.x]], y=[[points[:, 1] + self._center.y]],
    #         site=self._label, glyph_type=glyph_type,
    #         color=self._colors['shape'], fill_alpha=self._colors['shape_alpha'] if isinstance(ptn.raster_style, raster_styles.AreaStyle) else 0.,
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # def rect(self,ptn: pattern.Pattern[shapes.Rect]) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Rect = ptn.dim_shape[0]
    #
    #     self._add_plot_data(
    #         x=self._center.x + s * shape.center.x, y=self._center.y + s * shape.center.y,
    #         width=s * shape.width, height=s * shape.height, angle=shape.theta,
    #         site=self._label, glyph_type='rect',
    #         color=self._colors['shape'],
    #         fill_alpha=self._colors['shape_alpha'] if isinstance(ptn.raster_style, raster_styles.AreaStyle) else 0.,
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # def quad(self, ptn: pattern.Pattern[shapes.Rect]) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Rect = ptn.dim_shape[0]
    #
    #     left = self._center.x + (shape.center[0] - shape.width/2) * s
    #     right = self._center.x + (shape.center[0] + shape.width/2) * s
    #
    #     top = self._center.y + (shape.center[1] + shape.height/2) * s
    #     bottom = self._center.y + (shape.center[1] - shape.height/2) * s
    #
    #     self._add_plot_data(
    #         left=left , right=right,top=top, bottom=bottom,
    #         site=self._label, glyph_type='quad',
    #         color=self._colors['shape'], hatch_pattern='x',
    #         fill_alpha=self._colors['shape_alpha'] if isinstance(ptn.raster_style, raster_styles.AreaStyle) else 0.,
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
    #
    # def ellipse(
    #         self,
    #         ptn: pattern.Pattern[shapes.Ellipse],
    #         glyph_type: str
    # ) -> None:
    #     s = units.scale_factor(self._plot_unit, ptn.dim_shape[1])
    #     shape: shapes.Ellipse = ptn.dim_shape[0]
    #
    #     self._add_plot_data(
    #         x=self._center.x + s * shape.center.x, y=self._center.y + s * shape.center.y,
    #         a=s * shape.a, b=s * shape.b, angle=shape.theta,
    #         site=self._label, glyph_type=glyph_type,
    #         color=self._colors['shape'], fill_alpha=self._colors['shape_alpha'] if isinstance(ptn.raster_style, raster_styles.AreaStyle) else 0.,
    #         mill=str(ptn.shape_mill), label=self._label, raster_style=str(ptn.raster_style)
    #     )
