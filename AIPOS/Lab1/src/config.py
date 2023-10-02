import pathlib
from dataclasses import dataclass


@dataclass
class Directories:
    static: str
    templates: str
    test_data: str


def get_directories() -> Directories:
    root_dir = pathlib.Path(__file__).parent

    return Directories(
        static=str(root_dir / "static"),
        templates=str(root_dir / "templates"),
        test_data=str(root_dir / "test_data"),
    )
