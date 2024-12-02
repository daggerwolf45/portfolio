from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Company(BaseModel):
    name: str
    url: HttpUrl


class Description(BaseModel):
    text: str


class NestedDescription(Description):
    sub_detail: Optional[list["NestedDescription"]] = Field(default=None)


class Job(BaseModel):
    company: Company
    role: str
    start_date: str
    end_date: str = Field(default="Present")
    details: list[NestedDescription]


