import logging
import os

import ipywidgets as widgets
import numpy as np
from IPython.display import display

logger = logging.getLogger(__name__)


class LatexWidget:
    def __init__(
            self,
            df,
            git_commit_ids,
            row_ids=None,
            output_file=None,
            include_index=False,
            float_format='{:,.3f}',
            use_multirow=True,
            use_multicolumn=True,
            column_names=None,
            column_includes=None,
            column_formats=None,
            overwrite_output_file=False,
            highlight_max_per_column=False,
            escape=False,
            index_column_format='l',
            na_rep='-',
    ):
        self.df = df
        self.output = widgets.Output()
        self.latex_out = widgets.Output(layout={'border': '1px solid grey'})
        self.w_file_log_output = widgets.Output()
        self.w_include_index = widgets.Checkbox(
            description='include index', value=include_index
        )
        self.w_index_column_format = widgets.Text(
            description='index col. format',
            value=index_column_format,
            disabled=not include_index,
        )
        self.w_include_index.observe(self._update_index_column_format)
        self.w_float_format = widgets.Text(
            description='float format', value=float_format)
        self.w_na_rep = widgets.Text(
            description='NaN repr.', value=na_rep)
        self.w_use_multirow = widgets.Checkbox(
            description='use multirows', value=use_multirow)
        self.w_use_multicolumn = widgets.Checkbox(
            description='use multicolumns', value=use_multicolumn)
        self.w_highlight_max_per_column = widgets.Checkbox(
            description='print the max value of each column in bold',
            value=highlight_max_per_column)
        self.w_escape = widgets.Checkbox(description='Escape Latex',
                                         value=escape)
        self.w_output_file = widgets.Text(description='output file',
                                          value=output_file)
        self.w_draw_table_button = widgets.Button(
            description='draw latex table')
        self.w_write_file_button = widgets.Button(
            description='write to .tex file')
        self.w_overwrite_output_file = widgets.Checkbox(
            description='overwrite', value=overwrite_output_file
        )
        self.w_cols = {}
        self.output_widgets = []

        self.git_commit_ids = git_commit_ids
        self.row_ids = row_ids

        if column_names is None:
            column_names = df.columns
        if len(column_names) != len(df.columns):
            logger.error(
                "column_names doesn't have the correct length of "
                f'{len(df.columns)}'
            )
            return

        if column_includes is None:
            column_includes = [True] * len(column_names)
        if len(column_includes) != len(df.columns):
            logger.error(
                "column_includes doesn't have the correct length of "
                f'{len(df.columns)}'
            )
            return

        if column_formats is None:
            column_formats = ['c'] * len(column_names)
        if len(column_formats) != len(df.columns):
            logger.error(
                "column_formats doesn't have the correct length of "
                f'{len(df.columns)}'
            )
            return

        for i, column in enumerate(self.df.columns):
            self.w_cols[column] = {
                'name': widgets.Text(
                    value=str(column_names[i] if column_names[i] else column),
                    layout=widgets.Layout(width='140px'),
                ),
                'sort_up': widgets.Button(
                    icon='arrow-up',
                    tooltip=str(column),
                    layout=widgets.Layout(width='30px'),
                ),
                'sort_down': widgets.Button(
                    icon='arrow-down',
                    tooltip=str(column),
                    layout=widgets.Layout(width='30px'),
                ),
                'export': widgets.Checkbox(
                    value=column_includes[i],
                    layout=widgets.Layout(width='140px')
                ),
                'format': widgets.Text(
                    value=column_formats[i],
                    layout=widgets.Layout(width='30px')
                ),
            }
            self.output_widgets.append(
                widgets.HBox(
                    [
                        widgets.Label(
                            layout=widgets.Layout(min_width='140px'),
                            value=str(column)
                        ),
                        self.w_cols[column]['export'],
                        self.w_cols[column]['name'],
                        self.w_cols[column]['sort_up'],
                        self.w_cols[column]['sort_down'],
                        self.w_cols[column]['format'],
                    ]
                )
            )

            self.w_cols[column]['sort_up'].on_click(self._sort_up)
            self.w_cols[column]['sort_down'].on_click(self._sort_down)

        self.w_draw_table_button.on_click(self._draw_table)
        self.w_write_file_button.on_click(self._write_file)
        self._redraw()
        self.display()

    def _sort_up(self, button):
        cols = list(self.df.columns)
        old = cols.index(button.tooltip)
        if old == 0:
            return
        new = old - 1
        cols[new], cols[old] = cols[old], cols[new]
        self.output_widgets[new], self.output_widgets[old] = (
            self.output_widgets[old],
            self.output_widgets[new],
        )
        self.df = self.df[cols]
        self._redraw()

    def _sort_down(self, button):
        cols = list(self.df.columns)
        old = cols.index(button.tooltip)
        if old == len(cols) - 1:
            return
        new = old + 1
        cols[new], cols[old] = cols[old], cols[new]
        self.output_widgets[new], self.output_widgets[old] = (
            self.output_widgets[old],
            self.output_widgets[new],
        )
        self.df = self.df[cols]
        self._redraw()

    def _get_table_content(self):
        _columns = [
            c for c in self.df.columns if self.w_cols[c]['export'].value
        ]
        selected_names = [self.w_cols[c]['name'].value for c in
                          _columns]
        _formats = ''.join(
            [self.w_cols[c]['format'].value for c in _columns]
        )
        if self.w_include_index.value:
            _formats = self.w_index_column_format.value + _formats
        result = ''

        if self.git_commit_ids is not None:
            result += '% This table was made with results from commit: '
            result += str(self.git_commit_ids) + '\n'
        formatters = self._generate_formatters()

        if self.row_ids:
            r_min, r_max = min(self.row_ids), max(self.row_ids)
            result += '% This table contains results from rows:'
            result += '% ' + str(self.row_ids) + '\n'

        result += self.df.to_latex(
            columns=_columns,
            header=selected_names,
            column_format=_formats,
            index=self.w_include_index.value,
            float_format=self.nan_safe_float,
            multirow=self.w_use_multirow.value,
            multicolumn=self.w_use_multicolumn.value,
            formatters=formatters,
            escape=self.w_escape.value,
        )
        return result

    def nan_safe_float(self, x):
        if np.isnan(x):
            return self.w_na_rep.value
        return self.w_float_format.value.format(x)

    def _generate_formatters(self):
        if self.w_highlight_max_per_column.value:
            return [self._generate_max_formatter(column)
                    for column in self.df.columns]
        return None

    def _generate_max_formatter(self, column):
        def formatter(value):
            try:
                value = float(value)
            except ValueError:
                return value
            other_values = []
            for ov in self.df[column].values:
                try:
                    other_values.append(float(ov))
                except ValueError:
                    pass
            formatted_value = self.nan_safe_float(value)
            if value == max(other_values):
                return f'\\textbf{{ {formatted_value} }} '
            return formatted_value

        return formatter

    def _write_file(self, button=None):
        with self.w_file_log_output:
            self._draw_table()  # make sure the user sees what is written
            path = self.w_output_file.value
            if os.path.isfile(path) and not self.w_overwrite_output_file.value:
                logger.error(f'not overwriting existing file: {path}')
                return
            with open(path, 'w') as o_fh:
                o_fh.write(self._get_table_content())
                self.w_file_log_output.clear_output()
                print(f'content written to {path}')

    def _draw_table(self, button=None):
        with self.latex_out:
            self.latex_out.clear_output()
            print(self._get_table_content())

    def _redraw(self):
        with self.output:
            self.output.clear_output()
            display(widgets.VBox(self.output_widgets))
            self._draw_table()

    def _update_index_column_format(self, event):
        self.w_index_column_format.disabled = not self.w_include_index.value

    def display(self):
        display(self.get_output())

    def get_output(self):
        return widgets.VBox(
            [
                self.output,
                widgets.HBox(
                    [self.w_include_index, self.w_index_column_format]),
                self.w_use_multirow,
                self.w_use_multicolumn,
                self.w_highlight_max_per_column,
                self.w_escape,
                self.w_float_format,
                self.w_na_rep,
                self.w_draw_table_button,
                self.latex_out,
                widgets.HBox(
                    [
                        self.w_output_file,
                        self.w_overwrite_output_file,
                        self.w_write_file_button,
                    ]
                ),
                self.w_file_log_output,
            ]
        )
