from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Company(BaseModel):
    name: str
    url: Optional[HttpUrl] = Field(default=None)


class Description(BaseModel):
    text: str


class NestedDescription(Description):
    sub_detail: Optional[list["NestedDescription"]] = Field(default=None)


class Role(BaseModel):
    title: str
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    details: list[NestedDescription]


class Job(BaseModel):
    company: Company
    start_date: str
    end_date: str = Field(default="Present")
    roles: list[Role]
    has_roles: bool

    @classmethod
    def from_yaml(cls, data: dict) -> "Job":
        # Determine if single or multi/role job
        if data.get("roles", False):
            if len(data["roles"]) > 1:  #Multi-role
                data['has_roles'] = True

                # Assign primary date if missing
                if data.get("start_date", None) is None and data["roles"][0].get("start_date", False):
                    data["start_date"] = data["roles"][0]["start_date"]
                if data.get("end_date", None) is None and data["roles"][0].get("end_date", False):
                    data["end_date"] = data["roles"][0]["end_date"]
            else:   # Single-Role
                data['has_roles'] = False
        else:
            # this might be completely unnecessary... TBD
            data['has_roles'] = False
            if (data.get("role", data.get('title', False))) and data.get("start_date", False) and data.get("end_date", False) and data.get("details", False):
                data['roles'] = [
                    Role(
                          title=data.get("role", data['title']),
                          start_date=data['start_date'],
                          end_date=data['end_date'],
                          details=data['details']
                    )
                ]

        return cls.model_validate(data)



