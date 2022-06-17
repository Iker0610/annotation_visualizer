from typing import TypedDict


class AnnotationDict(TypedDict):
    id: str
    entity: str
    start_position: int
    end_position: int
    concept_category: str


class AnnotatedTextDict(TypedDict):
    note_id: int
    task_executor: str
    task_result: list[AnnotationDict]
    note_text: str
