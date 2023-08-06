import ipywidgets as widgets
from IPython.display import display
from dbispipeline.analytics import (
    rows_to_dataframe,
)
from dbispipeline.db import DbModel, DB

valid_input_filters = {}


class LoaderWidget:
    def __init__(
            self,
            row_ids=None,
            git_ids=None,
            project_name=None,
            plan_file=None,
            allow_dirty_rows=False,
            allow_multiple_git_ids=False,
            auto_open=True,
    ):
        layout = widgets.Layout(width='70%')
        s = {'description_width': '140px'}
        self.filter_widgets = {
            'id': widgets.Text(
                description='row ID(s)', value=row_ids, layout=layout,
                style=s),
            'git_commit_id': widgets.Text(
                description='git commit ID(s)', value=git_ids, layout=layout,
                style=s),
            'project_name': widgets.Text(
                description='project name(s)', value=project_name,
                layout=layout, style=s),
            'sourcefile': widgets.Text(
                description='plan file(s)', value=plan_file, layout=layout,
                style=s),
        }
        self.allow_dirty_rows = widgets.Checkbox(
                description='Allow dirty GIT rows', value=allow_dirty_rows)
        self.allow_multiple_git_ids = widgets.Checkbox(
                description='Allow multiple GIT commit ids',
                value=allow_multiple_git_ids)
        self.load_rows_button = widgets.Button(description="load")
        self.load_rows_button.on_click(self.load)
        if auto_open:
            display(
                widgets.VBox([
                    widgets.VBox(list(self.filter_widgets.values())),
                    self.allow_dirty_rows,
                    self.allow_multiple_git_ids,
                    self.load_rows_button,
                ], layout={'border': '1px solid grey'})
            )
        self.df = None

    def load(self, *args):
        session = DB.session()
        query = session.query(DbModel)
        for field, widget in self.filter_widgets.items():
            if not widget.value:
                continue
            val = widget.value
            if field == 'id':
                if '-' in val:
                    min_val, max_val = val.split('-')
                    query = query.filter(DbModel.id >= min_val)
                    if max_val != '*':
                        query = query.filter(DbModel.id <= max_val)
                elif ',' in val:
                    query = query.filter(DbModel.id.in_(val.split(',')))
                else:
                    query = query.filter(DbModel.id == val)
            else:
                if ',' in val:
                    query = query.filter(
                        getattr(DbModel, field).in_(val.split(',')))
                else:
                    query = query.filter(
                        getattr(DbModel, field) == val)
        self.df = rows_to_dataframe(
            query,
            allow_git_dirty_rows=self.allow_dirty_rows.value,
            allow_git_different_rows=self.allow_multiple_git_ids.value)
        print(f'df loaded with shape {self.df.shape}')
