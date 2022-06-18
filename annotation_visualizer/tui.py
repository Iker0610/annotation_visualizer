import os
import sys
from typing import Optional, Type

from textual.app import App
from textual.driver import Driver
from textual.widgets import ScrollView, Footer

from annotation_visualizer.model.model import GroupedAnnotatedDataset, load_grouped_annotated_dataset, AnnotatedText
from annotation_visualizer.widgets.annotation_labels import AnnotationLabelInfo
from annotation_visualizer.widgets.annotator_list import AnnotatorSelected, AnnotatorList
from annotation_visualizer.widgets.dataset_file_list import DatasetFileList, FileSelected
from annotation_visualizer.widgets.file_view import FileView


class CorpusTui(App):
    __selected_file: Optional[str] = None
    __selected_annotator: Optional[str] = None
    __selected_annotated_text: Optional[AnnotatedText] = None
    available_annotators: Optional[list[str]] = None

    # Properties
    @property
    def selected_file(self) -> Optional[str]:
        return self.__selected_file

    @selected_file.setter
    def selected_file(self, file: Optional[str]):
        self.__selected_file = file
        self.dataset_file_list_widget.refresh()
        self.available_annotators = list(self.dataset[file].keys())
        self.selected_annotator = self.available_annotators[0]

    @property
    def selected_annotator(self) -> Optional[str]:
        return self.__selected_annotator

    @selected_annotator.setter
    def selected_annotator(self, annotator: Optional[str]):
        self.__selected_annotator = annotator
        self.selected_annotated_text = self.dataset[self.selected_file][self.selected_annotator]
        self.annotator_list_widget.refresh()

    @property
    def selected_annotated_text(self) -> Optional[AnnotatedText]:
        return self.__selected_annotated_text

    @selected_annotated_text.setter
    def selected_annotated_text(self, annotated_text: Optional[AnnotatedText]):
        self.__selected_annotated_text = annotated_text

    # Constructor
    def __init__(
            self,
            screen: bool = True,
            driver_class: Optional[Type[Driver]] = None,
            log_verbosity: int = 1,
    ) -> None:
        super().__init__(
            screen=screen,
            driver_class=driver_class,
            log_verbosity=log_verbosity,
        )

        try:
            dataset_path = sys.argv[1]
        except IndexError:
            dataset_path = os.path.abspath(
                os.path.join(os.path.basename(__file__), "../dataset/annotations_codiesp.json")
            )

        self.dataset: GroupedAnnotatedDataset = load_grouped_annotated_dataset(dataset_path)

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

    async def handle_file_selected(self, event: FileSelected):
        await self.body.update(FileView())

    async def handle_annotator_selected(self, event: AnnotatorSelected):
        await self.body.update(FileView())

    async def action_toggle_all(self) -> None:
        await self.view.action_toggle("labels")
        await self.view.action_toggle("sidebar")
