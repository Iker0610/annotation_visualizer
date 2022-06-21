import json
from typing import TypedDict


class DatasetMetrics(TypedDict):
    Agreement: float
    BIAS: float
    KAPPA: float
    PI: float


class PairWiseFileMetrics(TypedDict):
    annotators: list[str]
    stats: dict[str, int | list]
    metrics: dict[str, float]


FileMetrics = list[PairWiseFileMetrics]


class Annotation(TypedDict):
    id: str
    entity: str
    start_position: int
    end_position: int
    label: str


class NoteAnnotations(TypedDict):
    annotator: str
    annotations: list[Annotation]


class NoteWithAnnotations(TypedDict):
    note_id: int
    filename: str
    note_text: str
    metrics: FileMetrics
    annotator_annotations: dict[str, NoteAnnotations]


GroupedAnnotatedDataset = dict[str, NoteWithAnnotations]


class DatasetWithMetrics(TypedDict):
    dataset_metrics: dict[str, DatasetMetrics]
    annotated_dataset: GroupedAnnotatedDataset


# Functions
def load_annotations_from_json(json_path: str) -> DatasetWithMetrics:
    with open(json_path, encoding='utf-8') as json_file:
        return json.load(json_file)
