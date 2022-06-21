from rich.panel import Panel
from textual.widget import Widget

from annotation_visualizer import styles
from annotation_visualizer.model.model import FileMetrics
from annotation_visualizer.renderables.file_metric_info import FileMetricInfo


class FileMetricBlock(Widget):
    def __init__(self, metric: FileMetrics):
        super().__init__()
        self.metric = metric

    def render(self) -> Panel:
        topic_info = FileMetricInfo(self.metric)
        annotators = ', '.join(self.metric['annotators'])

        return Panel(
            topic_info,
            title=f"[bold]Annotator Pair:[/] [yellow]{annotators}[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
