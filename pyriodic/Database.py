import pickle
import pkg_resources
import sqlite3

sqlite3.register_converter('PICKLE', pickle.loads)

class Database:
    def __init__(self):
        self._connection = sqlite3.connect(
            ':memory:', detect_types=sqlite3.PARSE_DECLTYPES)

        self._initialize_db()

    def _initialize_db(self):
        with self._connection as c:
            c.execute(
                'CREATE TABLE IF NOT EXISTS unit_cells( '
                'name STRING, space_group INTEGER, '
                'size INTEGER, structure PICKLE )')

    @property
    def connection(self):
        return self._connection

    def insert(self, name, space_group, structure, cursor=None):
        cursor = cursor or self._connection

        assert isinstance(space_group, int)

        encoded_structure = pickle.dumps(structure)
        size = len(structure.positions)

        cursor.execute(
            'INSERT INTO unit_cells VALUES (?, ?, ?, ?)',
            (name, space_group, size, encoded_structure))

    def query(self, query):
        for row in self._connection.execute(query):
            yield row

    @classmethod
    def make_standard(cls):
        result = cls()

        for entry_point in pkg_resources.iter_entry_points('pyriodic_sources'):
            callback = entry_point.load()
            callback(result)

        return result
