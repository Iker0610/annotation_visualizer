from rich.console import RichCast, Group
from rich.table import Table

from annotation_visualizer.model.model import FileMetrics


class FileMetricInfo(RichCast):
    def __init__(self, metrics: FileMetrics) -> None:
        self.metrics: FileMetrics = metrics

    def __rich__(self) -> Group:
        content = []
        for index, metric in enumerate(self.metrics, start=1):
            second_metric = 'S' if 'S' in metric['metrics'] else 'B2'

            table = Table(box=None, expand=False, show_header=False, show_edge=False)
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")
            table.add_column(style="bright_magenta bold")
            table.add_column(style="yellow bold")

            table.add_row(
                "B:", str(round(metric['metrics']['B'] * 100, 2)),
                f"{second_metric}:", str(round(metric['metrics'][second_metric] * 100, 2))
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
                f"[bold]Annotator Pair:[/] [yellow]{', '.join(metric['annotators'])}[/]",
                table,
            ]

            if index != len(self.metrics):
                content.append('\n')

        return Group(*content)
