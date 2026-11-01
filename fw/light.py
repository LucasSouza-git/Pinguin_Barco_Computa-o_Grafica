"""Luzes: ambiente e direcional (o 'sol'; a direcao e a mesma em toda a cena)."""
import numpy as np
from fw.object3d import Object3D


class AmbientLight(Object3D):
    def __init__(self, color=(0.3, 0.3, 0.3)):
        super().__init__()
        self.color = np.array(color, float)


class DirectionalLight(Object3D):
    def __init__(self, color=(1, 1, 1), direction=(-1, -1, -1)):
        super().__init__()
        self.color = np.array(color, float)
        d = np.array(direction, float)
        self.direction = d / np.linalg.norm(d)
