from rich.console import RichCast
from rich.text import Text

from ..model.model import AnnotatedText

style_mapper = {
    "RAZON_CONSULTA": "black on #98c379",
    "ANTECEDENTES_PERSONALES": "black on #d9d9d9",
    "ANTECEDENTES_FAMILIARES": "black on #94aa6d",
    "EXPLORACION": "black on #9496fb",
    "TRATAMIENTO": "black on #9ef8fb",
    "EVOLUCION": "black on #6d9eeb",
    "DIAGNOSTICO_FINAL": "black on #f68989",
    "DIAGNOSTICO_DIFERENCIAL": "black on #f1aacb",
    "DERIVACION_DE/A": "black on #f9da55",
}

class AnnotationLabelList(RichCast):
    def __rich__(self):
        content = Text(overflow="ellipsis", no_wrap=True)
        for label, style in style_mapper.items():
            content.append(label, style)
            content.append('\n\n')

        return content

class ColoredAnnotatedText(RichCast):
    def __init__(self, text: AnnotatedText):
        self.annotated_text = text

    def __rich__(self):
        content = Text(self.annotated_text.note_text)
        for annotation in self.annotated_text.task_result:
            content.stylize(style_mapper[annotation.label], annotation.start_position, annotation.end_position)
        return content
