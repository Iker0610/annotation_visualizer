from typing import Optional, Union

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.keys import Keys
from textual.widget import Widget

from app import styles
from app.model.model import GroupedAnnotatedDataset
from app.renderables.scrollable_list import ScrollableList


class DatasetFileList(Widget):
    scrollable_list: Optional[ScrollableList[GroupedAnnotatedDataset]] = None

    def max_renderables_len(self) -> int:
        height: int = self.size.height
        return height - 2

    def render(self) -> Panel:
        to_render: Union[Align, ScrollableList[GroupedAnnotatedDataset]] = Align.center(
            "There are no datafiles", vertical="middle"
        )

        if self.app.dataset:
            self.scrollable_list = ScrollableList(
                list(self.app.dataset.keys()),
                max_len=self.max_renderables_len(),
                selected=self.scrollable_list.selected
                if self.scrollable_list
                else None,
            )
            to_render = self.scrollable_list

        title = Text.from_markup(
            "[bold]files[/] ([blue]total[/] [yellow]{}[/])".format(
                len(self.app.dataset)
            )
        )
        return Panel(
            to_render,
            title=title,
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
        )

    def next(self) -> None:
        if self.scrollable_list is None:
            return

        self.scrollable_list.next()
        self.app.selected_file = self.scrollable_list.selected

    def previous(self) -> None:
        if self.scrollable_list is None:
            return

        self.scrollable_list.previous()
        self.app.selected_file = self.scrollable_list.selected

    def on_key(self, event: events.Key) -> None:
        if event.key == Keys.Up:
            self.previous()
        elif event.key == Keys.Down:
            self.next()

        self.refresh()

    async def on_click(self, event: events.Click) -> None:
        if self.scrollable_list is not None:
            self.scrollable_list.pointer = event.y - 1
            self.app.selected_file = self.scrollable_list.selected

        self.refresh()
