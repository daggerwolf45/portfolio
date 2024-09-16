import os
from pathlib import Path


class Config:
    script_directory = '..' / Path(os.path.dirname(os.path.realpath(__file__)))
    use_cache = False

    nav_menu_char_limit=30

    blog_root = '/blog/'

    template_dir = script_directory / "resources" / "templates"
    blog_dir = script_directory / "resources" / "blog"


conf = Config()
