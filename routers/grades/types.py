from dataclasses import dataclass


@dataclass
class Grade:
    percentage: float | int | None
    letter: str
    projected: float


@dataclass
class Class:
    grade: Grade
    courseId: str
    name: str
    sectionId: str
    teacher: str


@dataclass
class WidgetClass:
    grade: Grade
    name: str


@dataclass
class CourseWeight:
    name: str
    weight: float | None
    teacher: str
