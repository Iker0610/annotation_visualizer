import os
import sys
from typing import Optional

from textual import events
from textual.app import App
from textual.keys import Keys
from textual.widgets import ScrollView, Footer

from annotation_visualizer.model.model import DatasetWithMetrics, NoteWithAnnotations, load_annotations_from_json
from annotation_visualizer.widgets.annotation_labels import AnnotationLabelInfo
from annotation_visualizer.widgets.annotator_list import AnnotatorSelected, AnnotatorList
from annotation_visualizer.widgets.dataset_file_list import DatasetFileList, FileSelected
from annotation_visualizer.widgets.dataset_metric_header import DatasetMetricHeader
from annotation_visualizer.widgets.file_metric_panel import FileMetricPanel
from annotation_visualizer.widgets.file_view import FileView


class CorpusTui(App):
    __selected_file: Optional[str] = None
    __selected_annotator: Optional[str] = None
    __preferred_annotator: Optional[str] = None
    available_annotators: Optional[list[str]] = None

    # Properties
    @property
    def selected_file(self) -> Optional[str]:
        return self.__selected_file

    @selected_file.setter
    def selected_file(self, file: Optional[str]):
        self.__selected_file = file
        self.available_annotators = list(self.dataset[file]['annotator_annotations'].keys())

        if self.preferred_annotator is None:
            self.preferred_annotator = self.available_annotators[0]

        if self.preferred_annotator not in self.available_annotators:
            self.selected_annotator = self.available_annotators[0]

        else:
            self.selected_annotator = self.preferred_annotator

        self.dataset_file_list_widget.refresh()

    @property
    def selected_annotator(self) -> Optional[str]:
        return self.__selected_annotator

    @selected_annotator.setter
    def selected_annotator(self, annotator: Optional[str]):
        self.__selected_annotator = annotator
        self.annotator_list_widget.refresh()

    @property
    def preferred_annotator(self) -> Optional[str]:
        return self.__preferred_annotator

    @preferred_annotator.setter
    def preferred_annotator(self, annotator: Optional[str]):
        self.__preferred_annotator = annotator

    # Constructor
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Get dataset json file
        try:
            dataset_path = sys.argv[1]
        except IndexError:
            dataset_path = os.path.abspath(
                os.path.join(os.path.basename(__file__), "../dataset/annotations_codiesp.json")
            )

        # Load dataset
        dataset_with_metrics: DatasetWithMetrics = load_annotations_from_json(dataset_path)
        self.dataset: dict[str, NoteWithAnnotations] = dataset_with_metrics['annotated_dataset']
        self.dataset_metrics = dataset_with_metrics['dataset_metrics']

        # Generate base widgets
        self.dataset_file_list_widget = DatasetFileList()
        self.annotator_list_widget = AnnotatorList()
        self.file_metrics: ScrollView | None = None

        self.body: ScrollView | None = None

        self.selected_file = next(iter(self.dataset.keys()))

    async def on_load(self) -> None:
        """Sent before going in to application mode."""
        # Bind our basic keys
        await self.bind("A", "toggle_all", "Toggle side columns")
        await self.bind("a", "toggle_all", "Toggle side columns", show=False)

        await self.bind("F", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("f", "view.toggle('sidebar')", "Toggle sidebar", show=False)

        await self.bind("L", "view.toggle('labels')", "Toggle label info")
        await self.bind("l", "view.toggle('labels')", "Toggle label info", show=False)

        await self.bind("M", "view.toggle('metrics')", "Toggle dataset metrics")
        await self.bind("m", "view.toggle('metrics')", "Toggle dataset metrics", show=False)

        await self.bind("Q", "quit", "Quit")
        await self.bind("q", "quit", "Quit", show=False)

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""
        self.body = ScrollView(FileView())
        self.file_metrics = ScrollView()
        await self.update_file_metrics()

        await self.view.dock(Footer(), edge='bottom')

        selection_grid = await self.view.dock_grid(edge='left', size=30, name='sidebar')
        selection_grid.add_column(fraction=1, name="left", min_size=30)
        selection_grid.add_row(fraction=6, name="top", min_size=5)
        selection_grid.add_row(fraction=1, name="bottom", min_size=3)
        selection_grid.add_areas(
            file_list="left,top",
            annotator_list="left,bottom",
        )
        selection_grid.place(
            file_list=self.dataset_file_list_widget,
            annotator_list=self.annotator_list_widget,
        )

        await self.view.dock(AnnotationLabelInfo(), edge='right', size=30, name='labels')

        metrics_grid = await self.view.dock_grid(edge='bottom', size=8, name='metrics')
        metrics_grid.add_column(fraction=1, name='dataset_metrics')
        metrics_grid.add_column(fraction=1, name='file_metrics')
        metrics_grid.add_row(fraction=1, name='top')
        metrics_grid.add_row(fraction=1, name='bottom')
        metrics_grid.add_areas(
            b_metric="dataset_metrics,top",
            s_metric="dataset_metrics,bottom",
            file_metrics="file_metrics,top-start|bottom-end"
        )
        metrics_grid.place(
            b_metric=DatasetMetricHeader(metric='B'),
            s_metric=DatasetMetricHeader(metric='S'),
            file_metrics=self.file_metrics,
        )

        await self.view.dock(self.body, edge='bottom')

    async def handle_file_selected(self, _: FileSelected):
        await self.update_body()
        await self.update_file_metrics()

    async def handle_annotator_selected(self, _: AnnotatorSelected):
        await self.update_body()

    async def update_body(self):
        await self.body.update(FileView())

    async def update_file_metrics(self):
        await self.file_metrics.update(FileMetricPanel(self.dataset[self.selected_file]['metrics']))

    async def action_toggle_all(self) -> None:
        await self.view.action_toggle("labels")
        await self.view.action_toggle("sidebar")
        await self.view.action_toggle("metrics")

    async def on_key(self, event: events.Key) -> None:
        if event.key in [Keys.Up, Keys.Down]:
            await self.dataset_file_list_widget.on_key(event)
