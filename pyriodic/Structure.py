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

def replicate(box, positions, nx=1, ny=1, nz=1):
    frac_positions = np.tile(make_fractions(box, positions), (nx, ny, nz, 1, 1))
    frac_positions[:, ..., 0] += np.arange(nx)[:, np.newaxis, np.newaxis, np.newaxis]
    frac_positions[:, ..., 1] += np.arange(ny)[np.newaxis, :, np.newaxis, np.newaxis]
    frac_positions[:, ..., 2] += np.arange(nz)[np.newaxis, np.newaxis, :, np.newaxis]

    frac_positions = frac_positions.reshape((-1, 3))
    frac_positions /= (nx, ny, nz)
    frac_positions -= np.floor(frac_positions)

    box = list(box)
    box[0] *= nx
    box[1] *= ny
    box[2] *= nz

    new_positions = fractions_to_coordinates(box, frac_positions)

    return Box(*box), new_positions

def replicate_upto(box, positions, N_target):
    nbase = int(np.floor((N_target/len(positions))**(1/3)))
    start_boxdims = np.array(box[:3])
    ns = [nbase, nbase, nbase]
    while len(positions)*np.product(ns) < N_target:
        repl_boxdims = start_boxdims*ns
        ns[np.argmin(repl_boxdims)] += 1
    (nx, ny, nz) = ns

    return replicate(box, positions, nx, ny, nz)

def wrap(box, positions):
    fractions = make_fractions(box, positions)
    fractions %= 1.
    return fractions_to_coordinates(box, fractions)

class Structure:
    """Container for a single set of coordinates

    Structure objects hold all of the important quantities for a
    structural example, like coordinates and the system box.
    """
    __slots__ = ['positions', 'types', 'box']

    def __init__(self, positions, types, box):
        self.positions = np.asarray(positions)
        self.types = np.asarray(types, dtype=np.uint32)
        self.box = box

        assert len(self.positions) == len(self.types)

        if not isinstance(self.box, Box):
            self.box = Box(*self.box)

    def add_gaussian_noise(self, magnitude):
        """Add gaussian noise to each particle

        :param magnitude: Scale of the zero-mean gaussian nose
        :returns: A new :class:`Structure` with the gaussian noise applied.
        """
        noise = np.random.normal(scale=magnitude, size=self.positions.shape)
        wrapped_positions = wrap(self.box, self.positions + noise)

        return Structure(wrapped_positions, self.types, self.box)

    @property
    def fractional_coordinates(self):
        return make_fractions(self.box, self.positions)

    @classmethod
    def from_fractional_coordinates(cls, positions, types, box):
        positions = fractions_to_coordinates(box, positions)
        return cls(positions, types, box)

    def replicate(self, nx=1, ny=1, nz=1):
        """Replicate the system a given number of times in each dimension

        :param nx: Number of times to replicate in the x direction
        :param ny: Number of times to replicate in the y direction
        :param nz: Number of times to replicate in the z direction
        :returns: A new :class:`Structure` that has been replicated appropriately
        """
        (box, positions) = replicate(self.box, self.positions, nx, ny, nz)

        n_tile = len(positions)//len(self.positions)

        types = np.tile(self.types, n_tile)

        return Structure(positions, types, box)

    def replicate_upto(self, N_target):
        """Replicate the system to have at least a given number of particles

        Replicas are iteratively added in the shortest dimension of
        the box until at least `N_target` particles are present.

        :param N_target: Minimum number of particles to have in the resulting structure
        :returns: A new :class:`Structure` that has been replicated appropriately
        """
        (box, positions) = replicate_upto(self.box, self.positions, N_target)

        n_tile = len(positions)//len(self.positions)

        types = np.tile(self.types, n_tile)

        return Structure(positions, types, box)
