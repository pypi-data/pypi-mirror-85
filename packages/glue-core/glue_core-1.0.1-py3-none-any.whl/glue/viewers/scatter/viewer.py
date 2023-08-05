from glue.core.subset import roi_to_subset_state
from glue.core.util import update_ticks
from glue.core.roi_pretransforms import ProjectionMplTransform

from glue.utils import mpl_to_datetime64
from glue.viewers.scatter.compat import update_scatter_viewer_state
from glue.viewers.matplotlib.mpl_axes import init_mpl


__all__ = ['MatplotlibScatterMixin']


class MatplotlibScatterMixin(object):

    def setup_callbacks(self):
        self.state.add_callback('x_att', self._update_axes)
        self.state.add_callback('y_att', self._update_axes)
        self.state.add_callback('x_log', self._update_axes)
        self.state.add_callback('y_log', self._update_axes)
        self.state.add_callback('plot_mode', self._update_projection)
        self._update_axes()

    def _update_axes(self, *args):

        if self.state.x_att is not None:

            # Update ticks, which sets the labels to categories if components are categorical
            update_ticks(self.axes, 'x', self.state.x_kinds, self.state.x_log,
                         self.state.x_categories, projection=self.state.plot_mode)

            if self.state.x_log:
                self.state.x_axislabel = 'Log ' + self.state.x_att.label
            else:
                self.state.x_axislabel = self.state.x_att.label

        if self.state.y_att is not None:

            # Update ticks, which sets the labels to categories if components are categorical
            update_ticks(self.axes, 'y', self.state.y_kinds, self.state.y_log,
                         self.state.y_categories, projection=self.state.plot_mode)

            if self.state.y_log:
                self.state.y_axislabel = 'Log ' + self.state.y_att.label
            else:
                self.state.y_axislabel = self.state.y_att.label

        self.axes.figure.canvas.draw_idle()

    def _update_projection(self, *args):

        self.figure.delaxes(self.axes)
        _, self.axes = init_mpl(self.figure, projection=self.state.plot_mode)
        for layer in self.layers:
            layer._set_axes(self.axes)
            layer.state.vector_mode = 'Cartesian'
            layer.update()
        self.axes.callbacks.connect('xlim_changed', self.limits_from_mpl)
        self.axes.callbacks.connect('ylim_changed', self.limits_from_mpl)
        self.removeToolBar(self.toolbar)
        self.initialize_toolbar()
        self.update_x_axislabel()
        self.update_y_axislabel()
        self.update_x_ticklabel()
        self.update_y_ticklabel()

        # Reset and roundtrip the limits to have reasonable and synced limits when changing
        self.state.x_log = self.state.y_log = False
        self.state.reset_limits()
        self.limits_to_mpl()
        self.limits_from_mpl()

        self.figure.canvas.draw_idle()

    def apply_roi(self, roi, override_mode=None):

        # Force redraw to get rid of ROI. We do this because applying the
        # subset state below might end up not having an effect on the viewer,
        # for example there may not be any layers, or the active subset may not
        # be one of the layers. So we just explicitly redraw here to make sure
        # a redraw will happen after this method is called.
        self.redraw()

        if len(self.layers) == 0:
            return

        x_date = 'datetime' in self.state.x_kinds
        y_date = 'datetime' in self.state.y_kinds

        if x_date or y_date:
            roi = roi.transformed(xfunc=mpl_to_datetime64 if x_date else None,
                                  yfunc=mpl_to_datetime64 if y_date else None)

        use_transform = self.state.plot_mode != 'rectilinear'
        subset_state = roi_to_subset_state(roi,
                                           x_att=self.state.x_att, x_categories=self.state.x_categories,
                                           y_att=self.state.y_att, y_categories=self.state.y_categories,
                                           use_pretransform=use_transform)
        if use_transform:
            subset_state.pretransform = ProjectionMplTransform(self.state.plot_mode,
                                                               self.axes.get_xlim(),
                                                               self.axes.get_ylim(),
                                                               self.axes.get_xscale(),
                                                               self.axes.get_yscale())

        self.apply_subset_state(subset_state, override_mode=override_mode)

    @staticmethod
    def update_viewer_state(rec, context):
        return update_scatter_viewer_state(rec, context)
