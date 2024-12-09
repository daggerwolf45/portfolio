from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, HttpUrl


######
#   Work Experience
####

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


######
#   Programming Languages
####
class Proficiency(str, Enum):
    strong = 'Strong Experience'
    moderate = 'Moderate Experience'
    light = 'Light Experience'


class ProgLang(BaseModel):
    name: str
    icon_url: Optional[str] = Field(default=None)


class LangExperience(BaseModel):
    name: Annotated[str, Proficiency]
    langs: list[ProgLang]

    @classmethod
    def from_yaml(cls, data: dict) -> list["LangExperience"]:
        levels = []
        for strength in data:
            key = list(strength.keys())[0]
            lis = []
            for lang in strength[key]:
                lis.append(ProgLang.model_validate(lang))
            levels.append(LangExperience(name=Proficiency[key], langs=lis))
        return levels


######
#   Skills
####
class Skill(BaseModel):
    name: str
    hint: Optional[str] = Field(default=None)
    link: Optional[HttpUrl] = Field(default=None)


class SkillCategory(BaseModel):
    name: Optional[str] = Field(default=None)
    items: Optional[list[Skill]] = Field(default=None)
    subtypes: Optional[list['SkillCategory']] = None

    @classmethod
    def from_yaml(cls, data: dict) -> "SkillCategory":
        if not data.get("subtypes", False):
            data['subtypes'] = []

        if data.get("items", False):
            default_subtype = cls(items=data['items'])
            data['subtypes'].append(default_subtype)
            data['items'] = None

        return cls.model_validate(data)
