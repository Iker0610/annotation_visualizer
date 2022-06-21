from rich.console import RichCast, Group
from rich.table import Table

from annotation_visualizer.model.model import FileMetrics


class FileMetricInfo(RichCast):
    def __init__(self, metrics: FileMetrics) -> None:
        self.metrics: FileMetrics = metrics

    def __rich__(self) -> Group:
        content = []
        for metric in self.metrics:
            table = Table(box=None, expand=False, show_header=False, show_edge=False)
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")

            table.add_row(
                "B:", str(metric['metrics']['B']),
                "S:", str(metric['metrics']['S'])
            )
            table.add_row(
                "PBs:", str(metric['stats']['pbs']),
                "Edits:", str(metric['stats']['count_edits']),
            )
            table.add_row(
                "Additions:", str(len(metric['stats']['additions'])),
                "Substitutions:", str(len(metric['stats']['substitutions'])),
            )
            table.add_row(
                "Transpositions:", str(len(metric['stats']['transpositions'])),
                "", "",
            )

            content += [
                f"[bold]Annotator Pair:[/] [yellow]{', '.join(metric['annotators'])}[/]\n",
                table
            ]

        return Group(*content)
