import pyriodic

for entry in pyriodic.db.query('select * from unit_cells'):
    print(entry)
