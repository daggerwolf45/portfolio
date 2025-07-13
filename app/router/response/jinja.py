from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from starlette.requests import Request
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.config import conf

###
# Engine
#
jinja_loader = FileSystemLoader(conf.template_dir)
#jinja_ext = ['jinja2.ext.i18n.trimmed']
jinja_env = Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True, loader=jinja_loader, enable_async=False)

template_engine = Jinja2Templates(env=jinja_env)

jinja_stub_loader = FileSystemLoader(conf.stub_dir)
stub_env = Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True, loader=jinja_stub_loader, enable_async=False)

stub_engine = Jinja2Templates(env=stub_env)


###
# Responses
#
async def template_response(request: Request, path:str, *, process_name=True, **kw) -> _TemplateResponse:
    if process_name and not path.endswith('.jinja2'):
        if path.endswith('.html'):
            path = f'{path}.jinja2'
        else:
            path = f'{path}.html.jinja2'

    context = kw
    try:
        return template_engine.TemplateResponse(request=request, name=path, context=context)
    except TemplateNotFound as e:
        raise e


async def stub_response(request: Request, path:str, **kw) -> _TemplateResponse:
    try:
        return stub_engine.TemplateResponse(request=request, name=path, context=kw)
    except TemplateNotFound as e:
        raise e
