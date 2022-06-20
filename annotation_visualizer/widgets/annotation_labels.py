from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget

from .. import styles
from ..renderables.colored_annotated_text import AnnotationLabelList


class AnnotationLabelInfo(Widget):
    def render(self) -> Panel:
        title = Text.from_markup("[bold]Labels[/]")

        return Panel(
            AnnotationLabelList(),
            title=title,
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
        )
