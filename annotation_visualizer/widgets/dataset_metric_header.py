from rich.align import Align
from rich.panel import Panel
from textual.widget import Widget

from annotation_visualizer import styles
from annotation_visualizer.renderables.dataset_metric_info import DatasetMetricInfo


class DatasetMetricHeader(Widget):
    def __init__(self, metric: str):
        super().__init__()
        self.metric = metric

    def render(self) -> Panel:
        if metrics := self.app.dataset_metrics.get(self.metric):
            to_render = DatasetMetricInfo(metrics)
        else:
            to_render = Align.center("This metric is not calculated in you dataset.", vertical="middle")

        return Panel(
            to_render,
            title=f"[bold]Dataset Intertagger Agreement:[/] [yellow]{self.metric}[/]",
            border_style=styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )
