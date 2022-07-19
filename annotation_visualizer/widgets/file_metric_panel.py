from rich.align import Align
from rich.panel import Panel
from textual.widget import Widget

from annotation_visualizer import styles
from annotation_visualizer.model.model import FileMetrics
from annotation_visualizer.renderables.file_metric_info import FileMetricInfo


class FileMetricPanel(Widget):
    def __init__(self, metrics: FileMetrics):
        super().__init__()
        self.metrics = metrics

    def render(self) -> Panel:

        if self.metrics:
            content = FileMetricInfo(self.metrics)
        else:
            content = Align.center("There are not available metrics.", vertical="middle")
        return Panel(
            content,
            title="[bold]Pairwise File Metrics[/]",
            border_style=styles.BORDER_FOCUSED,
            box=styles.BOX,
            title_align="left",
        )
