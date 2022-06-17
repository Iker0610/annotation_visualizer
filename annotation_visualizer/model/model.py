import json

from .json_types import AnnotationDict, AnnotatedTextDict


# Data classes
class Annotation:
    def __init__(self, annotation: AnnotationDict):
        self.label: str = annotation['concept_category']
        self.start_position: int = annotation['start_position']
        self.end_position: int = annotation['end_position']


class AnnotatedText:
    def __init__(self, annotated_text: AnnotatedTextDict):
        self.note_id: str = str(annotated_text['note_id'])
        self.annotator: str = annotated_text['task_executor']
        self.task_result: list[Annotation] = [Annotation(annotation) for annotation in annotated_text['task_result']]
        self.note_text: str = annotated_text['note_text']


# Types
GroupedAnnotatedDataset = dict[str, dict[str, AnnotatedText]]


# Functions
def load_annotations_from_json(json_path: str) -> list[AnnotatedTextDict]:
    with open(json_path, encoding='utf-8') as json_file:
        return json.load(json_file)


def load_grouped_annotated_dataset(json_path: str) -> GroupedAnnotatedDataset:
    dataset: GroupedAnnotatedDataset = dict()
    for annotated_text_dict in load_annotations_from_json(json_path):
        annotated_text = AnnotatedText(annotated_text_dict)
        dataset.setdefault(annotated_text.note_id, dict())[annotated_text.annotator] = annotated_text

    return dataset
