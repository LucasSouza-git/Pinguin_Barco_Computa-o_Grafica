from fw.object3d import Object3D


class Mesh(Object3D):
    """Geometria + material + posicao no grafo de cena."""
    def __init__(self, geometry, material, cast_shadow=True):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.cast_shadow = cast_shadow
        self.visible = True
