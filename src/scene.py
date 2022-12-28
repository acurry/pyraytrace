from dataclasses import dataclass, field
from yaml import safe_load

@dataclass
class Scene:
    width: int = 1024
    height: int = 768
    max_depth: int = 3
    ratio: float = float(width) / height

    screen_left: float = -1
    screen_top: float = 1 / ratio
    screen_right: float = 1
    screen_bottom: float = -1 / ratio

    camera_x: float = 0.0
    camera_y: float = 0.0
    camera_z: float = 1.0

    @staticmethod
    def init_from_file(filename: str):
        with open(filename, "r") as file:
            data = safe_load(file)
            return Scene(**data['scene'])
