from datetime import datetime
from os import PathLike
from typing import IO, Optional

import markdown


class MarkdownMeta:
    title: Optional[str] = ""
    author: Optional[str] = ""
    date: Optional[str] = ""  #TODO Make datetime

    extra: dict

    def __init__(self, markdown_meta: dict):
        if 'title' in markdown_meta:
            self.title = markdown_meta.pop('title')[0]
        if 'author' in markdown_meta:
            self.author = markdown_meta.pop('author')[0]
        if 'date' in markdown_meta:
            self.date = markdown_meta.pop('date')[0]

        self.extra = markdown_meta

class RenderedMarkdown:
    _html: str
    _meta: MarkdownMeta
    _toc: str

    def __init__(self, *, text: str = None, path: PathLike = None, extensions: list[str] = []):
        md = markdown.Markdown(
              output_format='html', extensions=[
                                               "extra",
                                               "smarty",
                                               "sane_lists",
                                               "wikilinks",
                                               "meta",
                                               "toc"
                                           ] + extensions)

        if path is not None:
            with open(path, 'r') as f:
                text = f.read()

        try:
            self._html = md.convert(text)
        except:
            raise AttributeError("Could not parse provided text.")

        self._toc = md.toc
        self._meta = MarkdownMeta(md.Meta)


    @property
    def html(self):
        return self._html

    @property
    def meta(self):
        return self._meta

    @property
    def toc(self):
        return self._toc




async def render_markdown(path: PathLike) -> RenderedMarkdown:
    with open(path, "r", encoding="utf-8") as markdown_file:
        text = markdown_file.read()
        if len(text) <= 1:
            raise IOError  #TODO Raise proper exception

    return RenderedMarkdown(text)
