from rich.console import RichCast
from rich.table import Table

from annotation_visualizer.model.model import FileMetrics


class FileMetricInfo(RichCast):
    def __init__(self, metrics: FileMetrics) -> None:
        self.metrics: FileMetrics = metrics

    def __rich__(self) -> Table:
        table = Table(box=None, expand=False, show_header=False, show_edge=False)
        table.add_column(style="bright_magenta bold")
        table.add_column(style="yellow bold")
        table.add_column(style="bright_magenta bold")
        table.add_column(style="yellow bold")

        table.add_row(
            "B:", str(self.metrics['metrics']['B']),
            "S:", str(self.metrics['metrics']['S'])
        )
        table.add_row(
            "PBs:", str(self.metrics['stats']['pbs']),
            "Edits:", str(self.metrics['stats']['count_edits']),
        )
        table.add_row(
            "Additions:", str(len(self.metrics['stats']['additions'])),
            "Substitutions:", str(len(self.metrics['stats']['transpositions'])),
        )
        table.add_row(
            "Transpositions:", str(len(self.metrics['stats']['pbs'])),
            "", "",
        )

        return table
