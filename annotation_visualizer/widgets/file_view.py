from typing import Union

from rich.align import Align
from rich.console import RichCast
from rich.panel import Panel
from textual.widget import Widget
from textual.widgets import ScrollView

from .. import styles
from ..renderables.colored_annotated_text import ColoredAnnotatedText


class FileView(Widget):
    def render(self) -> Panel:

        if self.app.selected_annotated_text is not None:
            title = f"File ([blue]group[/] [yellow]{self.app.selected_file}[/])"

            to_render = ColoredAnnotatedText(self.app.selected_annotated_text)
        else:
            title = "records ([blue]group[/] [yellow]Unselected[/])"
            to_render: Union[Align, RichCast, str] = Align.center(
                "Not selected", vertical="middle"
            )

        return Panel(
            to_render,
            title=title,
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
