import os
import unittest
from io import BytesIO

from eilib.database import schemas
from eilib.database.acks import AcksDatabase
from eilib.database.items import ItemsDatabase
from eilib.database.levers import LeversDatabase
from eilib.database.perks import PerksDatabase
from eilib.database.prints import PrintsDatabase
from eilib.database.quests import QuestsDatabase
from eilib.database.spells import SpellsDatabase
from eilib.database.units import UnitsDatabase

TESTDATA_DIR = os.path.dirname(__file__)


class TestSaveLoad(unittest.TestCase):

    def _test_saveload_db(self, database_cls, schema):
        # Load
        database = database_cls()
        with open(os.path.join(TESTDATA_DIR, "data", schema["file"]), "rb") as f:
            database.load(f)
            db_size = f.tell()

        # Save
        buf = BytesIO()
        database.save(buf)

        # Reload saved db
        buf.seek(0)
        database2 = database_cls()
        database2.load(buf)
        db2_size = buf.tell()

        # Check databases are the same size
        self.assertEqual(db_size, db2_size)

        # Check databases are the same by value
        self.assertEqual(database, database2)

    def test_saveload_items(self):
        self._test_saveload_db(ItemsDatabase, schemas.ITEMS_DB_SCHEMA)

    def test_saveload_levers(self):
        self._test_saveload_db(LeversDatabase, schemas.LEVERS_DB_SCHEMA)

    def test_saveload_perks(self):
        self._test_saveload_db(PerksDatabase, schemas.PERKS_DB_SCHEMA)

    def test_saveload_spells(self):
        self._test_saveload_db(SpellsDatabase, schemas.SPELLS_DB_SCHEMA)

    def test_saveload_prints(self):
        self._test_saveload_db(PrintsDatabase, schemas.PRINTS_DB_SCHEMA)

    def test_saveload_units(self):
        self._test_saveload_db(UnitsDatabase, schemas.UNITS_DB_SCHEMA)

    def test_saveload_quests(self):
        self._test_saveload_db(QuestsDatabase, schemas.QUESTS_DB_SCHEMA)

    def test_saveload_acks(self):
        self._test_saveload_db(AcksDatabase, schemas.ACKS_DB_SCHEMA)


if __name__ == '__main__':
    unittest.main(module="test_saveload")
