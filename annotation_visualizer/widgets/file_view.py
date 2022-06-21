from typing import Union

from rich.align import Align
from rich.console import RichCast
from rich.panel import Panel
from textual.widget import Widget

from .. import styles
from ..renderables.colored_annotated_text import ColoredAnnotatedText


class FileView(Widget):
    def render(self) -> Panel:

        if self.app.selected_file is not None and self.app.selected_annotator is not None:
            title = f"File ([blue]id:[/] [yellow]{self.app.selected_file}[/] - [blue]annotator:[/] [yellow]{self.app.selected_annotator}[/])"

            to_render = ColoredAnnotatedText(
                self.app.dataset[self.app.selected_file]['note_text'],
                self.app.dataset[self.app.selected_file]['annotator_annotations'][self.app.selected_annotator]['annotations']
            )
        else:
            title = "File ([blue]id:[/] [yellow]Unselected[/] - [blue]annotator:[/] [yellow]Unselected[/])"
            to_render: Union[Align, RichCast, str] = Align.center(
                "Not selected", vertical="middle"
            )

        return Panel(
            to_render,
            title=title,
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
            padding=(1, 1, 0, 1)
        )
