import logging
import os

import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

plt.rcParams['figure.figsize'] = (20, 10)
logger = logging.getLogger(__name__)


def plot_multi_scores(
        df,
        group_keys=None,
        filter_key=None,
        filter_values=None,
        method='max',
        output_file=None,
        transpose=True,
        score_names=None):
    result_widgets = {}
    tab_outputs = []
    tab = widgets.Tab()
    for i, score_name in enumerate(score_names):
        output = widgets.Output()
        tab_outputs.append(output)
        tab.set_title(i, score_name)
        with output:
            sub_df = df[score_name]
            widget = PlotWidget(sub_df, group_keys, filter_key, filter_values,
                                method, output_file, transpose)
            result_widgets[score_name] = widget
    tab.children = tab_outputs
    display(tab)
    return result_widgets


class PlotWidget:
    def __init__(
            self,
            df,
            group_keys=None,
            filter_key=None,
            filter_values=None,
            method='max',
            output_file=None,
            transpose=True,
    ):
        self.df = df
        self.filtered_df = df

        index_names = sorted(df.index.names)

        self.w_parameters = widgets.SelectMultiple(
            options=index_names,
            value=group_keys if group_keys is not None else [index_names[0]],
            description='Group By',
        )
        valid_methods = ['min', 'max', 'mean', 'box']
        self.w_method = widgets.RadioButtons(
            options=valid_methods,
            value=method if method in valid_methods else 'max'
        )
        self.w_transpose = widgets.Checkbox(description='transpose',
                                            value=transpose)
        self.w_filter_key = widgets.Select(
            options=[''] + index_names[:],
            description='Filter field',
            value=filter_key if filter_key is not None else '',
        )
        self.w_filter_value = widgets.SelectMultiple(
            options=[], description='Filter value'
        )
        self.update_possible_filter_values(None)
        if filter_values is not None:
            self.w_filter_value.value = filter_values

        self.w_file_name = widgets.Text(
            value=output_file if output_file is not None else '',
            description='output CSV Path',
        )
        self.w_overwrite = widgets.Checkbox(
            description='allows overwriting output files'
        )
        self.w_output_button = widgets.Button(description='Generate CSV')
        self.w_export_output = widgets.Output()

        self.w_filter_key.observe(self.update_possible_filter_values)
        self.w_output_button.on_click(self.csv_callback)
        self.display()

    def update_possible_filter_values(self, x):
        value = self.w_filter_key.value
        if len(value.strip()):
            self.w_filter_value.options = [''] + sorted(
                self.df.index.unique(level=value)
            )
        else:
            self.w_filter_value.options = []

    def plot_callback(self, parameter, method, filter_key, filter_value,
                      transpose):
        if filter_key and filter_value:
            df = self.df[
                self.df.index.get_level_values(filter_key).isin(filter_value)]
        else:
            df = self.df
        print(parameter)
        group = df.groupby(list(parameter))
        if method == 'box':
            group.boxplot(subplots=False, rot=90, figsize=(20, 5))
            self.filtered_df = df
            if transpose:
                self.filtered_df = self.filtered_df.T
        else:
            if method == 'min':
                self.filtered_df = group.min()
            elif method == 'max':
                self.filtered_df = group.max()
            elif method == 'mean':
                self.filtered_df = group.mean()
            if transpose:
                self.filtered_df = self.filtered_df.T
            self.filtered_df.plot.bar()

    def csv_callback(self, click_event):
        path = self.w_file_name.value
        if os.path.isfile(path) and not self.w_overwrite.value:
            logger.warn('not overwriting existing file: {path}')
            return
        with self.w_export_output:
            self.w_export_output.clear_output()
            self.filtered_df.reset_index().to_csv(path, index=False)
            print(f'wrote output to {path}')

    def get_output(self):
        return widgets.VBox(
            [
                widgets.HBox(
                    [self.w_parameters, self.w_method, self.w_transpose]),
                widgets.HBox([self.w_filter_key, self.w_filter_value]),
                widgets.VBox(
                    [
                        widgets.HBox(
                            [self.w_file_name, self.w_output_button,
                             self.w_overwrite]
                        ),
                        self.w_export_output,
                    ]
                ),
                widgets.interactive_output(
                    self.plot_callback,
                    {
                        'parameter': self.w_parameters,
                        'method': self.w_method,
                        'filter_key': self.w_filter_key,
                        'filter_value': self.w_filter_value,
                        'transpose': self.w_transpose,
                    },
                ),
            ]
        )

    def display(self):
        display(self.get_output())
