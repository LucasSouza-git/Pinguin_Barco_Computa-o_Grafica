"""Camera em perspectiva e MovementRig (controle por teclado, sempre com tempo REAL)."""
import math
import numpy as np
from fw.object3d import Object3D
from fw.matrix import compor


def perspectiva(fov_graus, aspecto, near, far):
    f = 1.0 / math.tan(math.radians(fov_graus) / 2)
    m = np.zeros((4, 4))
    m[0, 0], m[1, 1] = f / aspecto, f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = 2 * far * near / (near - far)
    m[3, 2] = -1
    return m


def ortografica(l, r, b, t, n, f):
    m = np.eye(4)
    m[0, 0], m[1, 1], m[2, 2] = 2 / (r - l), 2 / (t - b), -2 / (f - n)
    m[0, 3], m[1, 3], m[2, 3] = -(r + l) / (r - l), -(t + b) / (t - b), -(f + n) / (f - n)
    return m


def olhar_para(olho, alvo, cima=(0, 1, 0)):
    """Matriz de visao (look-at)."""
    olho, alvo, cima = (np.asarray(v, float) for v in (olho, alvo, cima))
    f = alvo - olho
    f /= np.linalg.norm(f)
    s = np.cross(f, cima)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    m = np.eye(4)
    m[0, :3], m[1, :3], m[2, :3] = s, u, -f
    m[:3, 3] = -m[:3, :3] @ olho
    return m


class Camera(Object3D):
    def __init__(self, angle_of_view=60, aspect_ratio=1.5, near=0.1, far=200):
        super().__init__()
        self.projection = perspectiva(angle_of_view, aspect_ratio, near, far)

    def view_matrix(self):
        return np.linalg.inv(self.get_world_matrix())


class MovementRig(Object3D):
    """WASD move, R/F sobe/desce, Q/E gira, T/G inclina o olhar."""
    def __init__(self, vel=7.0, vel_giro=1.6):
        super().__init__()
        self.look_attachment = Object3D()
        Object3D.add(self, self.look_attachment)
        self.pos = np.zeros(3)
        self.yaw = 0.0
        self.pitch = 0.0
        self.vel, self.vel_giro = vel, vel_giro

    def add(self, filho):                # a camera fica pendurada no pivo de inclinacao
        self.look_attachment.add(filho)

    def set_position(self, pos):
        self.pos = np.array(pos, float)
        self._aplicar()

    def _aplicar(self):
        self.transform = compor(self.pos, ry=self.yaw)
        self.look_attachment.transform = compor(rx=self.pitch)

    def update(self, entrada, dt):
        frente = np.array([-math.sin(self.yaw), 0, -math.cos(self.yaw)])
        direita = np.array([math.cos(self.yaw), 0, -math.sin(self.yaw)])
        k = entrada.is_key_down
        d = self.vel * dt
        if k("w"): self.pos += frente * d
        if k("s"): self.pos -= frente * d
        if k("d"): self.pos += direita * d
        if k("a"): self.pos -= direita * d
        if k("r"): self.pos[1] += d
        if k("f"): self.pos[1] -= d
        if k("q"): self.yaw += self.vel_giro * dt
        if k("e"): self.yaw -= self.vel_giro * dt
        if k("t"): self.pitch = min(1.4, self.pitch + self.vel_giro * dt)
        if k("g"): self.pitch = max(-1.4, self.pitch - self.vel_giro * dt)
        self._aplicar()
