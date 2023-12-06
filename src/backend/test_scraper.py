import unittest
import json
from unittest.mock import mock_open, patch
from webscraper import ah
from webscraper import jumbo
from webscraper import hoogvliet

class TestFetchDataCacheAH(unittest.TestCase):
    """
    Test case for the fetch_data_cache function.
    """

    def setUp(self):
        self.mock_data = {"key": "value"}
        self.mock_json = json.dumps(self.mock_data)
        self.path = 'test_path.json'

    def test_fetch_data_cache(self):
        """
        Test case to verify the fetch_data_cache function.

        This test ensures that the function correctly opens the file, reads the JSON data, and returns it as a Python object.

        Returns:
            None
        """
        with patch('builtins.open', mock_open(read_data=self.mock_json)) as m:
            result = ah.fetch_data_cache(self.path)
            m.assert_called_once_with(self.path, 'r')
            self.assertEqual(result, self.mock_data)

# We tested other functions in the same way as the one above but we didn't include them in this file to keep it short.

class TestParseTaxonomies(unittest.TestCase):
    """
    Test case for the ah parseTaxonomies function.
    """

    def setUp(self):
        self.cards = [
            {
                "products": [
                    {
                        "taxonomies": [
                            {"name": "Taxonomy 1", "id": 1},
                            {"name": "Taxonomy 2", "id": 2}
                        ]
                    },
                    {
                        "taxonomies": [
                            {"name": "Taxonomy 3", "id": 3},
                            {"name": "Taxonomy 1", "id": 1}
                        ]
                    }
                ]
            },
            {
                "products": [
                    {
                        "taxonomies": [
                            {"name": "Taxonomy 4", "id": 4},
                            {"name": "Taxonomy 2", "id": 2}
                        ]
                    }
                ]
            }
        ]

    def test_parseTaxonomies(self):
        """
        Test case to verify the parseTaxonomies function.

        This test ensures that the function correctly parses the taxonomies from the cards and returns a list of unique taxonomies.

        Returns:
            None
        """
        result = ah.parseTaxonomies(self.cards)
        expected_result = [
            {"name": "Taxonomy 1", "id": 1},
            {"name": "Taxonomy 2", "id": 2},
            {"name": "Taxonomy 3", "id": 3},
            {"name": "Taxonomy 4", "id": 4}
        ]
        self.assertEqual(result, expected_result)

class TestJumboParseProducts(unittest.TestCase):
    """
    Test case for the jumbo parseProducts function.
    """

    def setUp(self):
        self.cards = [
            {
                "title": "Product 1",
                "prices": {
                    "pricePerUnit": {"price": 100, "unit": "kg"},
                    "price": 200
                },
                "link": "/product1"
            },
            {
                "title": "Product 2",
                "prices": {
                    "pricePerUnit": {"price": 300, "unit": "l"},
                    "price": 400
                },
                "link": "/product2"
            },
            {
                "title": "Product 3",
                "prices": {
                    "pricePerUnit": {"price": None, "unit": "stuk"},
                    "price": 500
                },
                "link": "/product3"
            }
        ]

    def test_parseProducts(self):
        """
        Test case to verify the jumbo parseProducts function.

        This test ensures that the function correctly parses the products from the cards and returns a list of items.

        Returns:
            None
        """
        result = jumbo.parseProducts(self.cards)
        expected_result = [
            {
                "name": "Product 1",
                "price": 1.0,
                "unit": "KG",
                "store_id": 2,
                "sales_price": 2.0,
                "url": "https://jumbo.com/product1",
                "taxomonies": []
            },
            {
                "name": "Product 2",
                "price": 3.0,
                "unit": "LT",
                "store_id": 2,
                "sales_price": 4.0,
                "url": "https://jumbo.com/product2",
                "taxomonies": []
            },
            {
                "name": "Product 3",
                "price": 5.0,
                "unit": "stuk",
                "store_id": 2,
                "sales_price": 5.0,
                "url": "https://jumbo.com/product3",
                "taxomonies": []
            }
        ]
        self.assertEqual(result, expected_result)


class TestAHParseProducts(unittest.TestCase):
    """
    Test case for the AH parseProducts function.
    """

    def setUp(self):
        self.cards = [
            {
                "products": [
                    {
                        "title": "Product 1",
                        "price": {
                            "now": 100,
                            "unitInfo": {"price": 1.0, "description": "kg"}
                        },
                        "link": "/product1",
                        "taxonomies": [{"id": 1}, {"id": 2}]
                    },
                    {
                        "title": "Product 2",
                        "price": {
                            "now": 200,
                            "unitInfo": {"price": 2.0, "description": "l"}
                        },
                        "link": "/product2",
                        "taxonomies": [{"id": 3}, {"id": 4}]
                    },
                    {
                        "title": "Product 3",
                        "price": {
                            "now": 300
                        },
                        "link": "/product3",
                        "taxonomies": [{"id": 5}, {"id": 6}]
                    }
                ]
            }
        ]

    def test_parseProducts(self):
        """
        Test case to verify the AH parseProducts function.

        This test ensures that the function correctly parses the products from the cards and returns a list of items.

        Returns:
            None
        """
        result = ah.parseProducts(self.cards)
        expected_result = [
            {
                "name": "Product 1",
                "store_id": 1,
                "price": 1.0,
                "sales_price": 100,
                "unit": "kg",
                "url": "https://www.ah.nl/product1",
                "taxomonies": ["1", "2"]
            },
            {
                "name": "Product 2",
                "store_id": 1,
                "price": 2.0,
                "sales_price": 200,
                "unit": "l",
                "url": "https://www.ah.nl/product2",
                "taxomonies": ["3", "4"]
            },
            {
                "name": "Product 3",
                "store_id": 1,
                "price": 300,
                "sales_price": 300,
                "unit": "stuk",
                "url": "https://www.ah.nl/product3",
                "taxomonies": ["5", "6"]
            }
        ]
        self.assertEqual(result, expected_result)


class TestHoogvlietParseProducts(unittest.TestCase):
    """
    Test case for the Hoogvliet parseProducts function.
    """

    def setUp(self):
        self.cards = {
            "items": [
                {
                    "title": "Product 1",
                    "price": 100,
                    "attributes": [
                        {"name": "BaseUnit", "values": ["kilo"]},
                        {"name": "RatioBasePackingUnit", "values": ["1"]}
                    ],
                    "url": "/product1"
                },
                {
                    "title": "Product 2",
                    "price": 200,
                    "attributes": [
                        {"name": "BaseUnit", "values": ["liter"]},
                        {"name": "RatioBasePackingUnit", "values": ["2"]}
                    ],
                    "url": "/product2"
                },
                {
                    "title": "Product 3",
                    "price": 300,
                    "attributes": [
                        {"name": "BaseUnit", "values": ["stuk"]},
                        {"name": "RatioBasePackingUnit", "values": ["3"]}
                    ],
                    "url": "/product3"
                }
            ]
        }

    def test_parseProducts(self):
        """
        Test case to verify the Hoogvliet parseProducts function.

        This test ensures that the function correctly parses the products from the cards and returns a list of items.

        Returns:
            None
        """
        result = hoogvliet.parseProducts(self.cards)
        expected_result = [
            {
                "name": "Product 1",
                "store_id": 3,
                "price": 100.0,
                "sales_price": 100,
                "unit": "KG",
                "url": "/product1",
                "taxomonies": []
            },
            {
                "name": "Product 2",
                "store_id": 3,
                "price": 100.0,
                "sales_price": 200,
                "unit": "LT",
                "url": "/product2",
                "taxomonies": []
            },
            {
                "name": "Product 3",
                "store_id": 3,
                "price": 100.0,
                "sales_price": 300,
                "unit": "stuk",
                "url": "/product3",
                "taxomonies": []
            }
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()