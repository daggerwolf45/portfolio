from starlette.templating import _TemplateResponse

from app.cache import ResourceManager
from app.config import conf
from app.md import RenderedMarkdown
from app.router.deps import std_dep
from app.router.response.jinja import template_response, templates



async def page_response(common: std_dep, path: str, get_page_data: bool = True, *, title:str, **kw, ) -> _TemplateResponse:
    if get_page_data:
        page_data = ResourceManager.get_page_data(path)
        if page_data is not None:
            kw['page'] = page_data.get('data', None)
            if page_data.get('mods', None) is not None:
                kw.update(page_data['mods'])

    kw['share_title'] = kw.get('share_title', title)
    real_path = common.request.url.path[:-1] + common.request.url.path[-1].replace('/','')
    canonical_url = conf.proxy_base + real_path

    return await template_response(
          request=common.request,
          path=path,
          title=title,
          latest_blogs=common.blogs,
          last_blog_published_time=common.last_blog,
          pageUrl=str(common.request.url),
          canonical_url=canonical_url,
          **kw
    )


async def blog_response(common: std_dep,  markdown: RenderedMarkdown, **kw) -> _TemplateResponse:
    return await page_response(
          common,
          "blog_base",
          md_content=markdown.html,
          md_toc=markdown.toc,
          **markdown.meta.__dict__,
          **kw
    )
