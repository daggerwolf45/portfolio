from typing import Annotated, Optional

import humanize
from fastapi import Depends
from starlette.requests import Request

from app.cache import ResourceManager
from app.config import conf
from app.utils import truncate


#########
# Classes
#
class std_dep:
    request: Request
    blogs: list[tuple[str, str]]  #name, path
    last_blog: str

    def __init__(self, request: Request, blogs=Depends(ResourceManager.latest_blogs, use_cache=False)):
        self.request = request

        self.blogs = [(truncate(b.title, conf.nav_menu_char_limit), b.name) for b in blogs]
        self.last_blog = humanize.naturaltime(blogs[0].date)


class TestAdvDep:
    def __call__(self, path:str = None) -> Optional[dict]:
        if path is None:
            print('No path!')
            return None
        print('<dep> Searching for:', path)
        return ResourceManager.get_page_data(path)


##############
# Annotations
#
adv_dep = TestAdvDep()

standard_dep = Annotated[std_dep, Depends()]
use_page_data = Annotated[Optional[dict], Depends(adv_dep)]
