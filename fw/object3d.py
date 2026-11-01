"""Object3D: no do grafo de cena (mesma ideia do capitulo 4 do livro)."""
import numpy as np


class Object3D:
    def __init__(self):
        self.transform = np.eye(4)
        self.parent = None
        self.children_list = []

    def add(self, filho):
        filho.parent = self
        self.children_list.append(filho)

    def remove(self, filho):
        self.children_list.remove(filho)
        filho.parent = None

    def get_world_matrix(self):
        m = self.transform
        p = self.parent
        while p is not None:
            m = p.transform @ m
            p = p.parent
        return m

    def get_world_position(self):
        return self.get_world_matrix()[:3, 3].copy()

    def set_position(self, pos):
        self.transform[:3, 3] = pos

    def descendants(self):
        """Lista este no e todos os descendentes (percurso em profundidade)."""
        lista, pilha = [], [self]
        while pilha:
            n = pilha.pop()
            lista.append(n)
            pilha.extend(n.children_list)
        return lista
