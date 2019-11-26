import collections
import numpy as np

Box = collections.namedtuple('Box', ['Lx', 'Ly', 'Lz', 'xy', 'xz', 'yz'])

def box_to_matrix(box):
    """Converts a box tuple (in [Lx, Ly, Lz, xy, xz, yz] order with HOOMD
    meanings) into a box matrix"""
    (Lx, Ly, Lz, xy, xz, yz) = box
    return np.array([[Lx, xy*Ly, xz*Lz],
                     [0,     Ly, yz*Lz],
                     [0,      0,    Lz]], dtype=np.float64)

def make_fractions(box, positions):
    """Converts a box tuple and positions array into a set of box
    fractions for each position"""
    box = list(box)
    if box[2] == 0:
        box[2] == 1
    boxmat = box_to_matrix(box)
    invbox = np.linalg.inv(boxmat)

    return np.dot(invbox, positions.T).T + .5

def fractions_to_coordinates(box, fractions):
    """Converts a box tuple and fraction array into a position for each
    given fraction"""
    boxmat = box_to_matrix(box)
    fractions = np.asarray(fractions) - .5

    coordinates = np.sum(
        fractions[:, np.newaxis, :]*boxmat[np.newaxis, :, :], axis=2)
    return coordinates

class Structure:
    __slots__ = ['positions', 'types', 'box']

    def __init__(self, positions, types, box):
        self.positions = positions
        self.types = types
        self.box = box

    @property
    def fractional_coordinates(self):
        return make_fractions(self.box, self.positions)

    @classmethod
    def from_fractional_coordinates(cls, positions, types, box):
        positions = fractions_to_coordinates(box, positions)
        return cls(positions, types, box)
