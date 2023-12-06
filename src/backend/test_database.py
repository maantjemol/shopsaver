import sqlite3
import os
import unittest
from database.functions import add_store, initialize_database, add_item, get_items_by_taxomony, get_all_taxomonies_with_items, get_taxomony_by_id


class TestDatabaseInitialization(unittest.TestCase):
    """
    Test case for database initialization.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'

    def tearDown(self):
        self.conn.close()

    def test_initialize_database(self):
        """
        Test case to verify the initialization of the database.

        This test ensures that the necessary tables (item, taxonomy, store, item_taxonomy) are created
        in the database after calling the initialize_database function.

        It checks if each table exists in the database by executing a SELECT query on the sqlite_master table.

        Returns:
            None
        """
        initialize_database(self.path, self.conn)
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='item'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='taxomony'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='store'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='item_taxonomy'")
        self.assertIsNotNone(cursor.fetchone())

class TestAddItem(unittest.TestCase):
    """
    Test case for adding an item to the database.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'
        initialize_database(self.path, self.conn)
        self.item = {
            "name": "Test Item",
            "store_id": 1,
            "unit": "kg",
            "price": 10.0,
            "url": "http://test.com",
            "sales_price": 8.0,
            "taxomonies": [1]
        }
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO taxomony (id, name) VALUES (1, 'testtax')")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_add_item(self):
        """
        Test case to verify the addition of an item to the database.

        This test ensures that the item is correctly added to the database by calling the add_item function
        and then checking if the item exists in the database by executing a SELECT query.

        Returns:
            None
        """
        add_item(self.item, self.conn) # type: ignore
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM item WHERE name=?", (self.item["name"],))
        self.assertIsNotNone(cursor.fetchone())

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM item_taxonomy WHERE item_id=1")
        self.assertIsNotNone(cursor.fetchone())

class TestAddStore(unittest.TestCase):
    """
    Test case for adding a store to the database.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'
        initialize_database(self.path, self.conn)
        self.store = {
            "name": "Test Store",
            "url": "http://teststore.com"
        }

    def tearDown(self):
        self.conn.close()

    def test_add_store(self):
        """
        Test case to verify the addition of a store to the database.

        This test ensures that the store is correctly added to the database by calling the add_store function
        and then checking if the store exists in the database by executing a SELECT query.

        Returns:
            None
        """
        add_store(self.store, self.conn) # type: ignore
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM store WHERE name=?", (self.store["name"],))
        self.assertIsNotNone(cursor.fetchone())

class TestGetItemsByTaxomony(unittest.TestCase):
    """
    Test case for getting items by taxonomy from the database.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'
        initialize_database(self.path, self.conn)
        self.item = {
            "name": "Test Item",
            "store_id": 1,
            "unit": "kg",
            "price": 10.0,
            "url": "http://test.com",
            "sales_price": 8.0,
            "taxomonies": [1]
        }
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO taxomony (id, name) VALUES (1, 'testtax')")
        self.conn.commit()
        add_item(self.item, self.conn) # type: ignore

    def tearDown(self):
        self.conn.close()

    def test_get_items_by_taxomony(self):
        """
        Test case to verify getting items by taxonomy from the database.

        This test ensures that the items are correctly fetched from the database by calling the get_items_by_taxomony function
        and then checking if the returned items match the expected result.

        Returns:
            None
        """
        items = get_items_by_taxomony(1, self.conn) # type: ignore
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"], self.item["name"])
        self.assertEqual(items[0]["store_id"], self.item["store_id"])
        self.assertEqual(items[0]["unit"], self.item["unit"])
        self.assertEqual(items[0]["price"], self.item["price"])
        self.assertEqual(items[0]["url"], self.item["url"])
        self.assertEqual(items[0]["taxomonies"], self.item["taxomonies"])

class TestGetAllTaxomoniesWithItems(unittest.TestCase):
    """
    Test case for getting all taxonomies with their items from the database.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'
        initialize_database(self.path, self.conn)
        self.item1 = {
            "name": "Test Item 1",
            "store_id": 1,
            "unit": "kg",
            "price": 10.0,
            "url": "http://test1.com",
            "sales_price": 8.0,
            "taxomonies": [1]
        }
        self.item2 = {
            "name": "Test Item 2",
            "store_id": 1,
            "unit": "kg",
            "price": 15.0,
            "url": "http://test2.com",
            "sales_price": 12.0,
            "taxomonies": [2]
        }
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO taxomony (id, name) VALUES (1, 'testtax1')")
        cursor.execute("INSERT INTO taxomony (id, name) VALUES (2, 'testtax2')")
        self.conn.commit()
        add_item(self.item1, self.conn) # type: ignore
        add_item(self.item2, self.conn) # type: ignore

    def tearDown(self):
        self.conn.close()

    def test_get_all_taxomonies_with_items(self):
        """
        Test case to verify getting all taxonomies with their items from the database.

        This test ensures that the taxonomies and their items are correctly fetched from the database by calling the get_all_taxomonies_with_items function
        and then checking if the returned data match the expected result.

        Returns:
            None
        """
        data = get_all_taxomonies_with_items(self.conn)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(len(data[0]["items"]), 1)
        self.assertEqual(data[0]["items"][0]["name"], self.item1["name"])
        self.assertEqual(data[1]["id"], 2)
        self.assertEqual(len(data[1]["items"]), 1)
        self.assertEqual(data[1]["items"][0]["name"], self.item2["name"])

class TestGetTaxomonyById(unittest.TestCase):
    """
    Test case for getting a taxonomy by id from the database.
    """

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.path = './database/initialize.sql'
        initialize_database(self.path, self.conn)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO taxomony (id, name) VALUES (1, 'testtax')")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_get_taxomony_by_id(self):
        """
        Test case to verify getting a taxonomy by id from the database.

        This test ensures that the taxonomy is correctly fetched from the database by calling the get_taxomony_by_id function
        and then checking if the returned taxonomy matches the expected result.

        Returns:
            None
        """
        taxonomy = get_taxomony_by_id(1, self.conn)
        self.assertEqual(taxonomy["id"], 1)
        self.assertEqual(taxonomy["name"], 'testtax')

if __name__ == '__main__':
    unittest.main()