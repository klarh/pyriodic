import unittest
import pyriodic

class TestBasic(unittest.TestCase):
    def test_any_query(self):
        structure = None
        for (structure,) in pyriodic.db.query(
                'select structure from unit_cells limit 1'):
            pass

        self.assertIsNotNone(structure)

    def test_replicate(self):
        for (structure,) in pyriodic.db.query(
                'select structure from unit_cells limit 1'):
            pass

        nx, ny, nz = 3, 5, 7
        big_structure = structure.replicate(nx, ny, nz)

        self.assertEqual(
            len(big_structure.positions), nx*ny*nz*len(structure.positions))
        self.assertEqual(
            len(big_structure.types), nx*ny*nz*len(structure.types))
        self.assertEqual(len(big_structure.positions), len(big_structure.types))

    def test_replicate_upto(self):
        for (structure,) in pyriodic.db.query(
                'select structure from unit_cells limit 1'):
            pass

        N = 17
        big_structure = structure.replicate_upto(N)

        self.assertGreaterEqual(len(big_structure.positions), N)
        self.assertGreaterEqual(len(big_structure.types), N)
        self.assertEqual(len(big_structure.positions), len(big_structure.types))

if __name__ == '__main__':
    unittest.main()
