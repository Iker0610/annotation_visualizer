from typing import Optional, Union

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.keys import Keys
from textual.message import Message
from textual.widget import Widget

from .. import styles
from ..renderables.scrollable_list import ScrollableList


class FileSelected(Message):
    pass


class DatasetFileList(Widget):
    scrollable_list: Optional[ScrollableList[str]] = None

    def max_renderables_len(self) -> int:
        height: int = self.size.height
        return height - 2

    def render(self) -> Panel:
        to_render: Union[Align, ScrollableList[str]] = Align.center(
            "There are no datafiles", vertical="middle"
        )

        if self.app.dataset:
            self.scrollable_list = ScrollableList(
                list(self.app.dataset.keys()),
                max_len=self.max_renderables_len(),
                selected=self.app.selected_file
                if self.scrollable_list
                else None,
            )
            to_render = self.scrollable_list

        title = Text.from_markup(
            "[bold]Files[/] ([blue]total[/] [yellow]{}[/])".format(
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

    async def on_key(self, event: events.Key) -> None:
        if event.key == Keys.Up:
            self.previous()
        elif event.key == Keys.Down:
            self.next()

        await self.emit(FileSelected(self))
        self.refresh()

    async def on_mouse_scroll_up(self) -> None:
        self.next()
        await self.emit(FileSelected(self))
        self.refresh()

    async def on_mouse_scroll_down(self) -> None:
        self.previous()
        await self.emit(FileSelected(self))
        self.refresh()

    async def on_click(self, event: events.Click) -> None:
        if self.scrollable_list is not None:
            self.scrollable_list.pointer = self.scrollable_list.start_rendering + event.y - 1
            self.app.selected_file = self.scrollable_list.selected

        await self.emit(FileSelected(self))

        self.refresh()
