from fastapi import APIRouter
from jinja2 import TemplateNotFound
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.config import conf

page_router = APIRouter()

template_dir = conf.script_directory / "resources" / "templates"
templates = Jinja2Templates(directory=template_dir)
def template_response(request:Request, name:str, *, process_name=True, **kw) -> _TemplateResponse:
    if process_name and not name.endswith('.jinja2'):
        if name.endswith('.html'):
            name = f'{name}.jinja2'
        else:
            name = f'{name}.html.jinja2'

    context = kw
    try:
        return templates.TemplateResponse(request=request, name=name, context=context)
    except TemplateNotFound as e:
        raise e

# Routes
@page_router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return template_response(request=request, name="index", title="HeyHey", ptext="Hello World!")



