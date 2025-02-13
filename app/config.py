import os
from pathlib import Path


class Config:
    script_directory = '..' / Path(os.path.dirname(os.path.realpath(__file__)))
    use_cache = False

    nav_menu_char_limit = 30

    works_blog_char_limit = 45
    works_blog_desc_char_limit = 180

    blog_root = '/blog/'

    template_dir = script_directory / "resources" / "templates"
    blog_dir = script_directory / "resources" / "blog"
    data_dir = script_directory / "resources" / "data"
    files_dir = script_directory / "resources" / "files"

    we_filename = "work_experience.yaml"
    skills_filename = "skill_experience.yaml"

    proxy_base = "https://samlaird.com"




conf = Config()
