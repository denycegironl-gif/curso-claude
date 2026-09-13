from pydantic import BaseModel


class StateOut(BaseModel):
    id: int
    code: str
