import os
from pathlib import Path


class Config:
    script_directory = '..' / Path(os.path.dirname(os.path.realpath(__file__)))


conf = Config()
