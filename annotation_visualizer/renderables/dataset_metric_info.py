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
                "KAPPA:", str(self.metrics['KAPPA']),
                "Agreement:", str(self.metrics['Agreement'])
            )
            table.add_row(
                "PI:", str(self.metrics['PI']),
                "BIAS:", str(self.metrics['BIAS'])
            )
        else:
            table = Table(box=None, expand=False, show_header=False, show_edge=False)
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")
            table.add_row("Mean:", str(self.metrics['arithmetic_mean']))
            table.add_row("Standar Deviation:", str(self.metrics['standard_deviation']))

        return table
