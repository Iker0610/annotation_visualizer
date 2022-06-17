import os
import sys
from typing import Optional, Type

from textual.app import App
from textual.driver import Driver
from textual.widgets import ScrollView

from annotation_visualizer.model.model import GroupedAnnotatedDataset, load_grouped_annotated_dataset, AnnotatedText
from annotation_visualizer.widgets.dataset_file_list import DatasetFileList
from annotation_visualizer.widgets.file_view import FileView


class CorpusTui(App):
    __selected_file: Optional[str] = None
    __selected_annotator: Optional[str] = None
    __selected_annotated_text: Optional[AnnotatedText] = None

    # Properties
    @property
    def selected_file(self) -> Optional[str]:
        return self.__selected_file

    @selected_file.setter
    def selected_file(self, file: Optional[str]):
        self.__selected_file = file
        self.dataset_file_list_widget.refresh()
        self.selected_annotator = next(iter(self.dataset[file].keys()))

    @property
    def selected_annotator(self) -> Optional[str]:
        return self.__selected_annotator

    @selected_annotator.setter
    def selected_annotator(self, annotator: Optional[str]):
        self.__selected_annotator = annotator
        self.selected_annotated_text = self.dataset[self.selected_file][self.selected_annotator]

    @property
    def selected_annotated_text(self) -> Optional[AnnotatedText]:
        return self.__selected_annotated_text

    @selected_annotated_text.setter
    def selected_annotated_text(self, annotated_text: Optional[AnnotatedText]):
        self.__selected_annotated_text = annotated_text
        self.dataset_file_list_widget.refresh()
        self.body.refresh()

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
        self.body = FileView()

    async def on_load(self) -> None:
        """Sent before going in to application mode."""
        # Bind our basic keys
        await self.bind("f", "view.toggle('file_list')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""
        await self.view.dock(self.dataset_file_list_widget, edge='left', size=48, name='file_list')
        await self.view.dock(ScrollView(self.body), edge='right')
