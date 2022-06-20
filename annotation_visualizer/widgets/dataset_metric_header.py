from rich.align import Align
from rich.panel import Panel
from textual.widget import Widget

from annotation_visualizer import styles


class DatasetMetricHeader(Widget):
    def __init__(self, metric: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metric = metric

    def render(self) -> Panel:
        if metrics := self.app.dataset_metrics.get(self.metric):
            # TODO: Add topic_info
            topic_info = ''
            pass
        else:
            topic_info = Align.center("This metric is not calculated in you dataset.", vertical="middle")

        return Panel(
            topic_info,
            title=f"[bold]Intertagger agreement:[/] [yellow]{self.metric}[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
