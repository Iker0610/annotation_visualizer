from rich.console import RichCast
from rich.text import Text

from ..model.model import AnnotatedText

style_mapper = {
    "RAZON_CONSULTA": "black on #98c379",
    "ANTECEDENTES_PERSONALES": "black on #d9d9d9",
    "ANTECEDENTES_FAMILIARES": "black on #94aa6d",
    "EXPLORACION": "black on #c9c5ff",
    "TRATAMIENTO": "black on #cfe2f3",
    "EVOLUCION": "black on #6d9eeb",
    "DIAGNOSTICO_FINAL": "black on #ea9999",
    "DIAGNOSTICO_DIFERENCIAL": "black on #f5c9de",
    "DERIVACION_DE/A": "black on #f5c9de",
}


class ColoredAnnotatedText(RichCast):
    def __init__(self, text: AnnotatedText):
        self.annotated_text = text

    def __rich__(self):
        content = Text(self.annotated_text.note_text)
        for annotation in self.annotated_text.task_result:
            content.stylize(style_mapper[annotation.label], annotation.start_position, annotation.end_position)
        return content
