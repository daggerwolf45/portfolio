import glob
from datetime import datetime
from os import PathLike

import yaml
from app.config import conf
from app.md import RenderedMarkdown
from app.models import Job, LangExperience, ProgLang, SkillCategory


class blog_stub:
    filename: str
    title: str
    name: str
    date: datetime
    author: str
    description: str

    def __init__(self, filename: str, name: str, title: str = None, date: datetime = None, author: str = None, desc: str = None):
        self.filename = filename
        self.title = title or name
        self.name = name
        self.date = date or datetime.fromtimestamp(0)
        self.author = author or ''
        self.description = desc or ''

    def __iter__(self):
        return iter(self.__dict__.values())



class ResourceManager:
    _instance: 'ResourceManager' = None

    _blogs: dict[str, blog_stub] = {}
    _blog_list: list[blog_stub]
    _work_experience: list[Job]
    _lang_experience: list[LangExperience]
    _skills_list: list[SkillCategory]


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance.reload_cache()
            #Interface.start()
            print("ResourceManager loaded..")


    @classmethod
    def reload_cache(cls):
        cls.generate_blogs()
        cls.generate_we()
        cls.generate_skills()
        return


    @classmethod
    def _load_blog(cls, *, path: PathLike = None, name: str = None) -> blog_stub:
        if name:
            filename = name + '.md'
            path = conf.blog_dir / filename
        else: # Using path
            filename = f"{path}".split('/')[-1]
            name = filename.split('.')[0]

        blog = RenderedMarkdown(path=path)
        stub = blog_stub(filename, name,blog.meta.title, blog.meta.timestamp, blog.meta.author, blog.meta.description)

        return stub

    @classmethod
    def generate_blogs(cls):
        blogs = {}
        for filename in glob.glob('*.md', root_dir=conf.blog_dir):
            stub = cls._load_blog(path=conf.blog_dir / filename)
            blogs[stub.name] = stub

        ordered_blogs = sorted(blogs.values(), key=lambda b: b.date, reverse=True)

        cls._blogs = blogs
        cls._blog_list = ordered_blogs


    @classmethod
    def generate_we(cls):
        exp = []
        with open(conf.data_dir / conf.we_filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)

        for job in data['jobs']:
            exp.append(Job.from_yaml(job))

        cls._work_experience = exp

    @classmethod
    def generate_skills(cls):
        skills = []
        with open(conf.data_dir / conf.skills_filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)

        # Langs
        langs = LangExperience.from_yaml(data['lang'])

        # Skills
        for skill in data['tk']:
            skills.append(SkillCategory.from_yaml(skill))

        cls._lang_experience = langs
        cls._skills_list = skills


    @classmethod
    def _sort_blogs(cls, blogs: list[blog_stub]) -> list[blog_stub]:
        return sorted(blogs, key=lambda b: b.date, reverse=True)


    ######
    @classmethod
    def get_blog(cls, blog: str) -> blog_stub:
        """
        Fetches blog from cache
        :return: Path to blog
        :rtype: str
        """

        if blog in cls._blogs:
            return cls._blogs[blog]
        else:
            stub = cls._load_blog(name=blog)
            cls._blogs[blog] = stub

            cls._blog_list.append(stub)
            cls._blog_list = cls._sort_blogs(cls._blog_list)

            return stub

    @classmethod
    def latest_blogs(cls, count: int = 5) -> list[blog_stub]:
        if len(cls._blog_list) < count:
            return cls._blog_list
        else:
            return cls._blog_list[:count]


    @classmethod
    def get_we(cls) -> list[Job]:
        return cls._work_experience

    @classmethod
    def get_skills(cls) -> list[SkillCategory]:
        return cls._skills_list

    @classmethod
    def get_lang_levels(cls) -> list["LangExperience"]:
        return cls._lang_experience


    @classmethod
    def get_all_exp(cls):
        #TODO DISABLE AFTER TESTING
        cls.reload_cache()

        all = {
            "work": cls._work_experience,
            "lang": cls._lang_experience,
            "skills": cls._skills_list,
        }
        return all


