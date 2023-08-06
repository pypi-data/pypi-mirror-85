"""
Submodule that handles visualization.
"""
import seaborn as sns
import pandas as pd
import numpy as np
import bokeh
from wasabi import msg as logger
from bokeh.models import CustomJS, ColumnDataSource
from matplotlib import pyplot as plt
from matplotlib import animation
from abc import ABC, abstractmethod
from copy import deepcopy
from hover import module_params
from hover.future.core.explorer import BokehForLabeledText


def static_heatmap(value_array, keys=None, **kwargs):
    """
    Display a heatmap optionally with keyed index, e.g. for a confusion matrix.
    :param value_array: the array of values.
    :type value_array: numpy.ndarray
    :param keys: labels whose indices match the indices of the value array.
    :type keys: list of str
    """
    df = pd.DataFrame(value_array)
    if keys:
        assert len(keys) == value_array.shape[0]
        df.columns = keys
        df.index = keys
    ax = sns.heatmap(df, **kwargs)
    return ax


def animated_heatmap(
    value_array_list,
    keys=None,
    heatmap_kwargs={"cmap": "Blues", "cbar": False},
    animation_kwargs={"interval": 500},
):
    """
    Display an animated heatmap optionally with keyed index, e.g. for an evolving confusion matrix.
    :param value_array: the array of values.
    :type value_array: numpy.ndarray
    :param keys: labels whose indices match the indices of the value array.
    :type keys: list of str
    """
    fig = plt.figure()
    anim = animation.FuncAnimation(
        fig,
        lambda arr: static_heatmap(arr, keys=keys, **heatmap_kwargs),
        frames=value_array_list,
        **animation_kwargs,
    )
    return anim


class BokehSliderAnimation(BokehForLabeledText):
    """
    Use a 'step' slider to view an interactive animation.
    Restricted to 2D.
    """

    def __init__(self, num_steps, **kwargs):
        from bokeh.models import Slider

        assert isinstance(num_steps, int)
        self.num_steps = num_steps
        self.slider = Slider(
            start=0, end=self.num_steps - 1, value=0, step=1, title="Step"
        )
        super().__init__(**kwargs)

    def setup_widgets(self):
        self.widgets.append(self.slider)
        super().setup_widgets()

    def label_steps(self, step_labels):
        from bokeh.models import Label

        assert (
            len(step_labels) == self.num_steps
        ), f"Expected {self.num_steps} annotations, got {len(step_labels)}"
        slider_label = Label(
            x=20,
            y=20,
            x_units="screen",
            y_units="screen",
            text=step_labels[0],
            render_mode="css",
            border_line_color="black",
            border_line_alpha=1.0,
            background_fill_color="white",
            background_fill_alpha=1.0,
        )
        slider_callback = CustomJS(
            args={
                "label": slider_label,
                "step": self.slider,
                "step_labels": step_labels,
            },
            code="""
            const S = Math.round(step.value);
            label.text = step_labels[S];
            label.change.emit();
        """,
        )

        self.slider.js_on_change("value", slider_callback)
        self.figure.add_layout(slider_label)

    def plot(self, traj_arr, attribute_data, method, **kwargs):
        """
        Add a plot to the figure.
        :param traj_arr: steps-by-point-by-dim array.
        :type traj_arr: numpy.ndarray with shape (self.slider.end, num_data_point, 2)
        :param attribute_data: {column->list} mapping, e.g. 'list' orientation of a Pandas DataFrame.
        :type attribute_data: dict
        :param method: the name of the plotting method to call.
        :type method: str, e.g. 'circle', 'square'
        """
        num_steps, num_data_point, num_dim = traj_arr.shape
        assert (
            num_steps == self.num_steps
        ), f"Expected {self.num_steps} steps, got {num_steps}"

        # require text and label attributes to be present
        assert "text" in attribute_data
        assert "label" in attribute_data

        # make a copy of attributes
        data_dict = attribute_data.copy()
        for _key, _value in data_dict.items():
            assert (
                len(_value) == num_data_point
            ), f"Length mismatch: {len(_value)} vs. num_data_point"

        coords_dict = {
            "x": traj_arr[0, :, 0],
            "y": traj_arr[0, :, 1],
            "xt": traj_arr[:, :, 0].flatten(),
            "yt": traj_arr[:, :, 1].flatten(),
        }
        data_dict.update(coords_dict)

        source = ColumnDataSource(data=data_dict)
        self.activate_search(source, kwargs)

        scatter = getattr(self.figure, method)
        scatter("x", "y", source=source, **kwargs)

        slider_callback = CustomJS(
            args={"source": source, "step": self.slider},
            code="""
            const data = source.data;
            const S = Math.round(step.value);
            var x = data['x'];
            var y = data['y'];
            for (var i = 0; i < x.length; i++) {
                x[i] = data['xt'][S * x.length + i];
                y[i] = data['yt'][S * x.length + i];
            }
            source.change.emit();
        """,
        )

        self.slider.js_on_change("value", slider_callback)
