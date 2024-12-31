from typing import List
from pydantic import BaseModel

from routers.grades.types import WidgetClass


class WidgetContentBodyDTO(BaseModel):
    email: str
    password: str
    token: str


class WidgetContentDTO(BaseModel):
    classes: List[WidgetClass]
    unweightedGPA: float
    weightedGPA: float
