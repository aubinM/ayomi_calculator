from pydantic import BaseModel, Field, NonNegativeInt
from typing import Optional
from datetime import datetime as dt
from pytz import timezone as tz


class CalculatorSchema(BaseModel):
    calcul: str = Field(..., min_length=3,
                        max_length=255)  # additional validation for the inputs
    result: Optional[int]
    created_date: Optional[str] = dt.now(tz("Europe/Paris")).strftime(
        "%Y-%m-%d %H:%M")


class CalculatorDB(CalculatorSchema):
    id: int
