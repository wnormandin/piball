from datetime import datetime
from pydantic import BaseModel
from typing import Union


class ElementModel(BaseModel):
    id: int
    created_at: Union[datetime, None]
    type: str
    label: str
    location: str
    input: bool
    output: bool
    relay_signal: Union[str, None]
    input_label: str
    output_label: Union[str, None]
    input_gpio_pin: int
    output_gpio_pin: Union[int, None]

    class Config:
        from_attributes = True
