from rich.console import RichCast
from rich.table import Table

from annotation_visualizer.model.model import DatasetMetrics


class DatasetMetricInfo(RichCast):
    def __init__(self, metrics: DatasetMetrics) -> None:
        self.metrics: DatasetMetrics = metrics

    def __rich__(self) -> Table:
        if 'KAPPA' in self.metrics:
            table = Table(box=None, expand=False, show_header=False, show_edge=False)
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")

            table.add_row(
                "KAPPA:", str(round(self.metrics['KAPPA'] * 100, 2)),
                "Agreement:", str(round(self.metrics['Agreement'] * 100, 2))
            )
            table.add_row(
                "PI:", str(round(self.metrics['PI'] * 100, 2)),
                "BIAS:", str(round(self.metrics['BIAS'] * 100, 2))
            )
        else:
            table = Table(box=None, expand=False, show_header=False, show_edge=False)
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")
            table.add_row("Mean:", str(round(self.metrics['arithmetic_mean'] * 100, 2)))
            table.add_row("Standar Deviation:", str(round(self.metrics['standard_deviation'] * 100, 2)))

        return table
