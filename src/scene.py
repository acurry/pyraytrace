from dataclasses import dataclass, field
from yaml import safe_load

@dataclass
class Scene:
    width: int
    height: int
    max_depth: int
    ratio: float
    camera: list[int] = field(default_factory=list)
    screen: dict = field(default_factory=dict)

    def __init__(self, width: float, height: float, max_depth: int, camera: list[float]):
        self.width = width
        self.height = height
        self.max_depth = max_depth
        self.camera = camera

        self.ratio = float(width) / height
        
        self.screen = {
            'left': -1,
            'top': 1 / self.ratio,
            'right': 1,
            'bottom': -1  / self.ratio,
        }

    @staticmethod
    def init_from_file(filename: str):
        with open(filename, "r") as file:
            data = safe_load(file)
            return Scene(**data['scene'])
