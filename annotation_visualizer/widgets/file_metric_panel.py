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
        return Panel(
            FileMetricInfo(self.metrics),
            title="[bold]Pairwise File Metrics[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
        )
