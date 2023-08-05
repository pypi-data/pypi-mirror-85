from typing import List, Optional, Tuple
import itertools
import pathlib

# from fibomat.default_backends import measure_band  # needed so measure_band is registered and available

import pandas as pd

import bokeh.models as bm
import bokeh.colors as bc
import bokeh.plotting as bp
from bokeh import events
import bokeh.palettes as bpal
from bokeh.core import properties as bokeh_prop
from bokeh.util import compiler as bokeh_comp

from fibomat import pattern
from fibomat import backend
from fibomat import units
from fibomat import site
from fibomat import utils
from fibomat import linalg
from fibomat import curve_tools
from fibomat.default_backends import _bokeh_site
from fibomat import shapes
from fibomat.dimensioned_object import DimObjLike, DimObj

from typing import Tuple, Sequence


from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, scale_to, scale_factor
from fibomat.dimensioned_object import DimObjLike, DimObj
from fibomat.shapes import Shape
from fibomat.mill import Mill

_ts_file_path = pathlib.Path(__file__).parent.absolute().joinpath('measure_band.ts')
_ts_file = ''.join(open(_ts_file_path).readlines())


class StubAreaStyle(RasterStyle):
    def __init__(self, dimension: int):
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def rasterize(
        self,
        dim_shape: DimObjLike[Shape, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:
        pass

    # def explode(
    #     self,
    #     dim_shape: DimObjLike[Shape, LengthUnit],
    #     repeats: int,
    #     mill: Mill,
    #     out_length_unit: LengthUnit,
    #     out_time_unit: TimeUnit
    # ) -> Sequence[Tuple[Shape, RasterStyle]]:
    #     pass


class BokehBackend(backend.BackendBase):
    """
    The default backend for plotting projects, based on the bokeh library.
    All shapes defined in fibomat library are supported.

    .. note:: :class:`~fibomat.shapes.arc.shapes.Arc` and :class:`~fibomat.shapes.curve.shapes.Curve` are rasterized during plotting
              due to lack of supported of the HoverTool for this shapes in the bokeh library. The pitch can be defined
              via the `rasterize_pitch` parameter.
    """
    name = 'bokeh'

    def __init__(
            self, *,
            unit: Optional[units.UnitType] = None,
            title: Optional[str] = None,
            hide_sites: bool = False,
            rasterize_pitch: Optional[units.QuantityType] = None,
            fullscreen: bool = True,
            legend: bool = True,
            cycle_colors: bool = False,
            **kwargs
    ):
        """
        Args:
            unit (units.UnitType, optional): used unit for plotting, default to units.U_('µm')
            title (str, optional): title of plot, default to ''
            hide_sites (bool, optional): if true, sides' outlines are not shown, default to false
            rasterize_pitch (units.QuantityType. optional): curve_tools.rasterize pitch for shapes.Arc, ... and shapes.Curve, default to units.Q_('0.01 µm')
            fullscreen (bool, optional): if true, plot will be take the whole page, default to True
            cycle_colors (bool): if True, different sites get different colors.
        """

        if unit:
            if unit.dimensionality != '[length]':
                raise ValueError('unit\'s dimension must by [length].')
            self._unit = unit
        else:
            self._unit = units.U_('µm')

        if title:
            self._title = str(title)
        else:
            self._title = ''

        self._hide_sites = bool(hide_sites)

        if rasterize_pitch:
            if rasterize_pitch.dimensionality != '[length]':
                raise ValueError('rasterize_pitch\'s dimension must by [length].')
            self._rasterize_pitch = rasterize_pitch
        else:
            self._rasterize_pitch = units.Q_('0.01 µm')

        self._fullscreen = bool(fullscreen)
        self._legend = bool(legend)

        super().__init__(**kwargs)

        self._cycle_colors = cycle_colors

        self._bokeh_sites: List[_bokeh_site.BokehSite] = []
        self._annotation_site: _bokeh_site.BokehSite = _bokeh_site.BokehSite(
            -1, self._unit, linalg.Vector(0, 0), self._unit, self._rasterize_pitch, False, None, 'Annotations'
        )
        self.fig: Optional[bp.Figure] = None

    def process_site(self, site_: site.Site):

        fov_scale = units.scale_factor(self._unit, site_.fov.unit)
        fov = fov_scale * site_.fov.obj

        self._bokeh_sites.append(
            _bokeh_site.BokehSite(len(self._bokeh_sites), self._unit, site_.center, site_.unit, self._rasterize_pitch, self._cycle_colors, fov, site_.description)
        )
        super().process_site(site_)

    def process_pattern(self, ptn: pattern.Pattern) -> None:
        super().process_pattern(ptn)

    def process_unknown(self, ptn: pattern.Pattern) -> None:
        bbox = ptn.dim_shape[0].bounding_box
        bbox_ptn = pattern.Pattern(
            dim_shape=(shapes.Rect(bbox.width, bbox.height, 0, bbox.center), ptn.dim_shape[1]),
            shape_mill=ptn.shape_mill,
            raster_style=ptn.raster_style,
            **ptn.kwargs  # True if 'annotation' in ptn.kwargs else False
        )
        self._filled_curve(bbox_ptn)

    def _collect_plot_data(self):
        # https://stackoverflow.com/a/40826547
        keys = _bokeh_site.BokehSite.plot_data_keys
        data_dicts = [site.plot_data for site in self._bokeh_sites]
        data_dicts.append(self._annotation_site.plot_data)
        return {key: list(itertools.chain(*[data_dict[key] for data_dict in data_dicts])) for key in keys}

    @staticmethod
    def _plot_multi_line(fig, plot_data, shape_type):
        view = bm.CDSView(
            source=plot_data, filters=[bm.GroupFilter(column_name='shape_type', group=shape_type)]
        )

        return fig.multi_line(
            xs='x', ys='y',
            line_color='color', line_width=2,
            legend_field='site_id',
            source=plot_data, view=view
        )

    @staticmethod
    def _plot_multi_polygon(fig, plot_data, shape_type):
        view = bm.CDSView(
            source=plot_data, filters=[bm.GroupFilter(column_name='shape_type', group=shape_type)]
        )

        return fig.multi_polygons(
            xs='x', ys='y',
            line_width=2,
            fill_color='color', line_color='color', fill_alpha='fill_alpha',
            legend_field='site_id',
            source=plot_data, view=view
        )

    def plot(self):
        # it does not work, if this class is imported.
        # TODO: write bug report
        class MeasureTool(bm.Inspection):
            """
            A measure tool for bokeh plots!
            """

            __implementation__ = bokeh_comp.TypeScript(code=_ts_file)

            measure_unit = bokeh_prop.String(default='apples', help='')

            line_dash = bokeh_prop.DashPattern(default='solid', help='')

            line_color = bokeh_prop.Color(default="black", help='')

            line_width = bokeh_prop.Float(default=1, help='')

            line_alpha = bokeh_prop.Float(default=1.0, help='')

        tooltips = [
            # ('type', 'shape'),
            ('shape', '@shape_prop'),
            # ('collection_index', '@collection_index'),
            ('mill', '@mill'),
            ('raster style', '@raster_style'),
            ('site', '@site_id'),
            ('description', '@description')
            # ('mill_settings', '@mill_settings'),
        ]

        site_tooltips = [
            # ('site', '@site'),
            ('description', '@description')
        ]

        fig = bp.figure(
            title=self._title,
            x_axis_label=f'x / {self._unit:~P}', y_axis_label=f'y / {self._unit:~P}',
            match_aspect=True,
            sizing_mode='stretch_both' if self._fullscreen else 'stretch_width',
            tools="pan,wheel_zoom,reset"
            # tooltips=tooltips
        )

        fig.add_tools(
            MeasureTool(
                measure_unit=f'{self._unit:~P}', line_color=bc.groups.red.Crimson, line_width=3  # bpal.all_palettes['Colorblind'][4][3]
            )
        )

        # self._install_coord_label(fig)

        fig.add_tools(bm.BoxZoomTool(match_aspect=True))

        # plot_data = bm.ColumnDataSource(self._collect_plot_data())
        plot_data = pd.DataFrame(self._collect_plot_data())

        # shapes
        # spot

        plot_data_b = bm.ColumnDataSource(plot_data)

        spot_view = bm.CDSView(
            source=plot_data_b, filters=[
                bm.GroupFilter(column_name='shape_type', group='spot'),
            ]
        )

        spot_glyphs = fig.circle_x(
            x='x', y='y',
            fill_color='color', line_color='color', fill_alpha=.25,
            legend_field='site_id', size=10,
            source=plot_data_b, view=spot_view
        )
        # bm.ColumnDataSource(plot_data[plot_data.shape_type.eq(_bokeh_site.ShapeType.SPOT)])

        non_filled_curve_glyphs = self._plot_multi_line(
            fig,
            plot_data_b, _bokeh_site.ShapeType.NON_FILLED_CURVE
        )
        # bm.ColumnDataSource(plot_data[plot_data.shape_type.eq(_bokeh_site.ShapeType.NON_FILLED_CURVE)])

        filled_curve_glyphs = self._plot_multi_polygon(
            fig,
            plot_data_b, _bokeh_site.ShapeType.FILLED_CURVE
        )

        # layers
        # https://github.com/bokeh/bokeh/issues/9087
        if not self._hide_sites:
            site_glyphs = self._plot_multi_polygon(
                fig,
                plot_data_b, _bokeh_site.ShapeType.SITE
            )
            site_glyphs.level = 'underlay'

            site_glyphs_hover = bm.HoverTool(
              renderers=[site_glyphs],
              tooltips=site_tooltips,
              point_policy='follow_mouse'
            )
            fig.add_tools(site_glyphs_hover)

        # hover tool for shapes
        # add shape hover tool after site hovertool so it is rendered on top of the site tooltip
        shape_glyphs_hover = bm.HoverTool(
            renderers=[
                spot_glyphs, non_filled_curve_glyphs, filled_curve_glyphs
            ],
            tooltips=tooltips, point_policy='follow_mouse'
        )
        fig.add_tools(shape_glyphs_hover)

        fig.legend.visible = self._legend

        # show(fig)
        self.fig = fig

    def show(self):
        # self.save()
        bp.show(self.fig)

    def save(self, filename: utils.PathLike):
        bp.output_file(filename)
        bp.save(self.fig)

    def spot(self, ptn: pattern.Pattern[shapes.Spot]) -> None:
        if 'annotation' in ptn.kwargs:
            self._annotation_site.spot(ptn)
        else:
            self._bokeh_sites[-1].spot(ptn)

    def _non_filled_curve(self, ptn):
        if 'annotation' in ptn.kwargs:
            self._annotation_site.non_filled_curve(ptn)
        else:
            self._bokeh_sites[-1].non_filled_curve(ptn)

    def _filled_curve(self, ptn):
        if 'annotation' in ptn.kwargs:
            self._annotation_site.filled_curve(ptn)
        else:
            self._bokeh_sites[-1].filled_curve(ptn)

    def _dispatch_pattern(self, ptn):
        if not ptn.dim_shape.obj.is_closed:
            self._non_filled_curve(ptn)
        elif ptn.raster_style.dimension < 2:
            self._non_filled_curve(ptn)
        else:
            self._filled_curve(ptn)

    def line(self, ptn: pattern.Pattern[shapes.Line]) -> None:
        self._dispatch_pattern(ptn)

    def polyline(self, ptn: pattern.Pattern[shapes.Polyline]) -> None:
        self._dispatch_pattern(ptn)

    def arc(self, ptn: pattern.Pattern[shapes.Arc]) -> None:
        self._dispatch_pattern(ptn)

    def arc_spline(self, ptn: pattern.Pattern[shapes.ArcSpline]) -> None:
        self._dispatch_pattern(ptn)

    def polygon(self, ptn: pattern.Pattern[shapes.Polygon]) -> None:
        self._dispatch_pattern(ptn)

    def rect(self, ptn: pattern.Pattern[shapes.Rect]) -> None:
        self._dispatch_pattern(ptn)

    def ellipse(self, ptn: pattern.Pattern[shapes.Ellipse]) -> None:
        self._dispatch_pattern(ptn)

    def circle(self, ptn: pattern.Pattern[shapes.Circle]) -> None:
        self._dispatch_pattern(ptn)

    #
    # def polygon(self, ptn: pattern.Pattern[shapes.Polygon]) -> None:
    #     if 'annotation' in ptn.kwargs:
    #         self._annotation_site.polygon(ptn)
    #     else:
    #         self._bokeh_sites[-1].polygon(ptn)
    #
    # def _rasterized_curve_impl(self, ptn: pattern.Pattern[rasterizing.RasterizedPoints], glyph_pref) -> None:
    #     if 'annotation' in ptn.kwargs:
    #         plot_site = self._annotation_site
    #     else:
    #         plot_site = self._bokeh_sites[-1]
    #
    #     if ptn.dim_shape[0].is_closed:
    #         plot_site.rasterized_curve_closed(ptn, glyph_pref + '_closed')
    #     else:
    #         plot_site.rasterized_curve_open(ptn, glyph_pref + '_open')
    #
    # # def rasterized_curve(self, ptn: pattern.Pattern[rasterizing.RasterizedPoints]) -> None:
    # #     self._rasterized_curve_impl(ptn, 'rasterized_curve')
    #
    # def curve(self, ptn: pattern.Pattern[shapes.Curve]) -> None:
    #     ptn.dim_shape = (
    #         curve_tools.rasterize(
    #             ptn.dim_shape[0], units.scale_to(ptn.dim_shape[1], self._rasterize_pitch)
    #         ),
    #         ptn.dim_shape[1]
    #     )
    #     self._rasterized_curve_impl(ptn, 'curve')
    #
    # def rect(self, ptn: pattern.Pattern[shapes.Rect]) -> None:
    #     if 'annotation' in ptn.kwargs:
    #         self._annotation_site.rect(ptn)
    #     else:
    #         self._bokeh_sites[-1].rect(ptn)
    #
    # def ellipse(self, ptn: pattern.Pattern[shapes.Ellipse]) -> None:
    #     if 'annotation' in ptn.kwargs:
    #         self._annotation_site.ellipse(ptn)
    #     else:
    #         self._bokeh_sites[-1].ellipse(ptn)
    #
    # def circle(self, ptn: pattern.Pattern[shapes.Circle]) -> None:
    #     # super().circle(pattern)
    #     ptn.dim_shape = (shapes.Ellipse(a=2*ptn.dim_shape[0].r, b=2*ptn.dim_shape[0].r, center=ptn.dim_shape[0].center, theta=0.), ptn.dim_shape[1])
    #
    #     if 'annotation' in ptn.kwargs:
    #         self._annotation_site.ellipse(ptn)
    #     else:
    #         self._bokeh_sites[-1].ellipse(ptn)
