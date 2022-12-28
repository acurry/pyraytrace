from dataclasses import dataclass, field
from yaml import safe_load
import numpy as np

@dataclass
class Shape:
    radius: float
    shininess: int
    reflection: float
    center: list[float] = field(default_factory=list)
    ambient: list[float] = field(default_factory=list)
    diffuse: list[float] = field(default_factory=list)
    specular: list[float] = field(default_factory=list)

    def __post_init__(self):
        self.center = np.array(self.center)
        self.ambient = np.array(self.ambient)
        self.diffuse = np.array(self.diffuse)
        self.specular = np.array(self.specular)

@dataclass
class Light:
    position: list[float] = field(default_factory=list)
    ambient: list[float] = field(default_factory=list)
    diffuse: list[float] = field(default_factory=list)
    specular: list[float] = field(default_factory=list)

    def __post_init__(self):
        self.position = np.array(self.position)
        self.ambient = np.array(self.ambient)
        self.diffuse = np.array(self.diffuse)
        self.specular = np.array(self.specular)

@dataclass
class Scene:
    width: int
    height: int
    max_depth: int

    light: Light = field(default_factory=Light)
    shapes: list[Shape] = field(default_factory=list[Shape])

    ratio: float = field(init=False)
    screen: dict = field(init=False)

    camera: list[float] = field(default_factory=list)
    screen: dict = field(default_factory=dict)

    def __post_init__(self):
        self.ratio = float(self.width) / self.height
        
        self.screen = {
            'left': -1,
            'top': 1 / self.ratio,
            'right': 1,
            'bottom': -1  / self.ratio,
        }

        self.camera = np.array(self.camera)

        self.shapes = [Shape(**s) for s in self.shapes]
        self.light = Light(**self.light)

    @staticmethod
    def init_from_file(filename: str):
        with open(filename, "r") as file:
            data = safe_load(file)
            return Scene(**data['scene'])
