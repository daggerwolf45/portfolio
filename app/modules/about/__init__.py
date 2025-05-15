import pathlib
import yaml

namespace = "ab_widget"


def page_data():
    data_dir = pathlib.Path(__file__).parent / 'data'
    path = data_dir / 'ab-widget.yaml'
    with open(path, 'r') as f:
        page_data: dict = yaml.load(f, Loader=yaml.Loader)
    return page_data

