from pydantic import BaseModel
from typing import Sequence, Dict


class Delta(BaseModel):
    confirmed: int
    deceased: int
    recovered: int


class District(BaseModel):
    notes: str
    active: int
    confirmed: int
    migratedother: int
    deceased: int
    recovered: int
    delta: Delta


class State(BaseModel):
    districtData: Dict[str, District]


class StateSearchResults(BaseModel):
    results: Dict[str, District]
