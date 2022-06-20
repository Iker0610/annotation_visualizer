import os
import sys
from typing import Optional

from textual.app import App
from textual.widgets import ScrollView, Footer

from annotation_visualizer.model.model import DatasetWithMetrics, NoteWithAnnotations, load_annotations_from_json
from annotation_visualizer.widgets.annotation_labels import AnnotationLabelInfo
from annotation_visualizer.widgets.annotator_list import AnnotatorSelected, AnnotatorList
from annotation_visualizer.widgets.dataset_file_list import DatasetFileList, FileSelected
from annotation_visualizer.widgets.file_view import FileView


class CorpusTui(App):
    __selected_file: Optional[str] = None
    __selected_annotator: Optional[str] = None
    available_annotators: Optional[list[str]] = None

    # Properties
    @property
    def selected_file(self) -> Optional[str]:
        return self.__selected_file

    @selected_file.setter
    def selected_file(self, file: Optional[str]):
        self.__selected_file = file
        self.dataset_file_list_widget.refresh()
        self.available_annotators = list(self.dataset[file]['annotator_annotations'].keys())

        if self.selected_annotator not in self.available_annotators:
            self.selected_annotator = self.available_annotators[0]
        else:
            self.annotator_list_widget.refresh()

        self.dataset_file_list_widget.refresh()

    @property
    def selected_annotator(self) -> Optional[str]:
        return self.__selected_annotator

    @selected_annotator.setter
    def selected_annotator(self, annotator: Optional[str]):
        self.__selected_annotator = annotator
        self.annotator_list_widget.refresh()

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

        await self.bind("Q", "quit", "Quit")
        await self.bind("q", "quit", "Quit", show=False)

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""
        self.body = ScrollView(FileView())

        await self.view.dock(Footer(), edge='bottom')
        grid = await self.view.dock_grid(edge='left', size=30, name='sidebar')
        grid.add_column(fraction=1, name="left", min_size=30)
        grid.add_row(fraction=6, name="top", min_size=5)
        grid.add_row(fraction=1, name="bottom", min_size=3)
        grid.add_areas(
            file_list="left,top",
            annotator_list="left,bottom",
        )
        grid.place(
            file_list=self.dataset_file_list_widget,
            annotator_list=self.annotator_list_widget,
        )

        await self.view.dock(AnnotationLabelInfo(), edge='right', size=30, name='labels')
        await self.view.dock(self.body, edge='top')

    async def handle_file_selected(self, _: FileSelected):
        await self.body.update(FileView())

    async def handle_annotator_selected(self, _: AnnotatorSelected):
        await self.body.update(FileView())

    async def action_toggle_all(self) -> None:
        await self.view.action_toggle("labels")
        await self.view.action_toggle("sidebar")
