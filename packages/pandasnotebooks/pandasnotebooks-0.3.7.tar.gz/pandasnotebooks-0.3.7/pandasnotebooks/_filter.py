import ipywidgets as widgets
from IPython.display import display
from dbispipeline.analytics import (
    extract_gridsearch_parameters,
)


class FilterWidget:
    def __init__(
            self,
            df,
            keep_columns=None,
            drop_columns=None,
            extract_grid_params=True,
            score_name='mean_test_score',
            auto_open=True,
    ):
        if keep_columns is not None and drop_columns is not None:
            raise ValueError(
                'only use one of either keep_columns or drop_columns')

        if keep_columns:
            kept_columns = keep_columns
        elif drop_columns:
            kept_columns = [c for c in df.columns if c not in drop_columns]
        else:
            kept_columns = df.columns

        self.original_df = df

        self.filter_widgets = {
            c: widgets.Checkbox(description=c, value=c in kept_columns) for c
            in df.columns}
        self.all_button = widgets.Button(description='All')
        self.none_button = widgets.Button(description='None')
        self.invert_button = widgets.Button(description='Invert')
        self.all_button.on_click(self.set_all)
        self.none_button.on_click(self.set_none)
        self.invert_button.on_click(self.set_invert)

        self.extract_grid_params = widgets.Checkbox(
            description='Extract GridSearch Parameters',
            value=extract_grid_params)
        self.score_name = widgets.Text(
            description='Score Name', value=score_name)
        self.filter_button = widgets.Button(description="Filter")
        self.filter_button.on_click(self.do_filter)

        if auto_open:
            display(widgets.VBox([
                widgets.HBox([
                    widgets.VBox([
                        self.all_button,
                        self.none_button,
                        self.invert_button,
                    ]),
                    widgets.VBox(list(self.filter_widgets.values())),
                ]),
                self.extract_grid_params,
                self.score_name,
                self.filter_button,
            ], layout={'border': '1px solid grey'}))

    def set_invert(self, *args):
        self._set(lambda x: not x.value)

    def set_all(self, *args):
        self._set(lambda x: True)

    def set_none(self, *args):
        self._set(lambda x: False)

    def _set(self, callback):
        for w in self.filter_widgets.values():
            w.value = callback(w)

    def do_filter(self, *args):
        selected_columns = [k for k, v in self.filter_widgets.items() if
                            v.value]
        self.df = self.original_df[selected_columns]
        if self.extract_grid_params.value:
            score_names = self.score_name.value.split(',')
            self.df = extract_gridsearch_parameters(self.df, score_names)
            print('extracted grid parameters')