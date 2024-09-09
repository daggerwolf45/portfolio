from fastapi import APIRouter
from jinja2 import TemplateNotFound
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.config import conf
from app.md import RenderedMarkdown

page_router = APIRouter()

template_dir = conf.script_directory / "resources" / "templates"
blog_dir = conf.script_directory / "resources" / "blog"

templates = Jinja2Templates(directory=template_dir)
async def template_response(request: Request, path:str, *, process_name=True, **kw) -> _TemplateResponse:
    if process_name and not path.endswith('.jinja2'):
        if path.endswith('.html'):
            path = f'{path}.jinja2'
        else:
            path = f'{path}.html.jinja2'

    context = kw
    try:
        return templates.TemplateResponse(request=request, name=path, context=context)
    except TemplateNotFound as e:
        raise e


async def blog_response(request: Request,  markdown: RenderedMarkdown, **kw) -> _TemplateResponse:

    return await template_response(
          request,
          "blog_base",
          md_content=markdown.html,
          md_toc=markdown.toc,
          **markdown.meta.__dict__,
          **kw
    )


# Routes
@page_router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return await template_response(request, "index", title="Sam Laird", ptext="Hello World!")


@page_router.get('/blog/{blog_id}', response_class=HTMLResponse)
async def get_blog(request: Request, blog_id: str):
    blog_path = blog_dir / (blog_id.lower() + ".md")

    markdown = RenderedMarkdown(path=blog_path)

    return await blog_response(request, markdown)

