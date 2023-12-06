import unittest
import re
from filter import removeBlacklist, getItemTaxonomies

class TestRemoveBlacklist(unittest.TestCase):
    """
    Test case for the removeBlacklist function.
    """

    def test_removeBlacklist(self):
        """
        Test case to verify the removeBlacklist function.

        This test ensures that the function correctly removes the words in the blacklist from the string.

        Returns:
            None
        """
        string = "this is a test string with forbidden words"
        blacklist = "test\nforbidden"
        result = removeBlacklist(string, blacklist)
        self.assertEqual(result, "this is a string with words")

    def test_removeBlacklist_with_numbers(self):
        """
        Test case to verify the removeBlacklist function with numbers.

        This test ensures that the function correctly removes the numbers in the blacklist from the string.

        Returns:
            None
        """
        string = "This is a test string with 1234 and 5678"
        blacklist = "1234\n5678"
        result = removeBlacklist(string, blacklist)
        self.assertEqual(result, "this is a test string with and")

    def test_removeBlacklist_with_units(self):
        """
        Test case to verify the removeBlacklist function with units.

        This test ensures that the function correctly removes the units in the blacklist from the string.

        Returns:
            None
        """
        string = "This is a test string with 1kg and 2l"
        blacklist = "1kg\n2l"
        result = removeBlacklist(string, blacklist)
        self.assertEqual(result, "this is a test string with and")

    def test_removeBlacklist_with_empty_string(self):
        """
        Test case to verify the removeBlacklist function with an empty string.

        This test ensures that the function correctly handles an empty string.

        Returns:
            None
        """
        string = ""
        blacklist = "test\nforbidden"
        result = removeBlacklist(string, blacklist)
        self.assertEqual(result, "")

    def test_removeBlacklist_with_empty_blacklist(self):
        """
        Test case to verify the removeBlacklist function with an empty blacklist.

        This test ensures that the function correctly handles an empty blacklist.

        Returns:
            None
        """
        string = "this is a test string with forbidden words"
        blacklist = ""
        result = removeBlacklist(string, blacklist)
        self.assertEqual(result, string)

class TestGetItemTaxonomies(unittest.TestCase):
    """
    Test case for the getItemTaxonomies function.
    """

    def test_getItemTaxonomies_exact_match(self):
        """
        Test case to verify the getItemTaxonomies function with exact match.

        This test ensures that the function correctly returns the taxonomy ids when there is an exact match.

        Returns:
            None
        """
        item = {"name": "test item"}
        allItems = [{"id": 1, "items": [{"name": "test item"}]}, {"id": 2, "items": [{"name": "another item"}]}]
        result = getItemTaxonomies(item, allItems) # type: ignore
        self.assertEqual(result, [1, 2])

    def test_getItemTaxonomies_no_match(self):
        """
        Test case to verify the getItemTaxonomies function with no match.

        This test ensures that the function correctly returns an empty list when there is no match.

        Returns:
            None
        """
        item = {"name": "test item"}
        allItems = [{"id": 1, "items": [{"name": "another item"}]}, {"id": 2, "items": [{"name": "yet another item"}]}]
        result = getItemTaxonomies(item, allItems) # type: ignore
        self.assertEqual(result, [1, 2])

    def test_getItemTaxonomies_partial_match(self):
        """
        Test case to verify the getItemTaxonomies function with partial match.

        This test ensures that the function correctly returns the taxonomy ids when there is a partial match.

        Returns:
            None
        """
        item = {"name": "test item"}
        allItems = [{"id": 1, "items": [{"name": "test"}]}, {"id": 2, "items": [{"name": "item"}]}]
        result = getItemTaxonomies(item, allItems) # type: ignore
        self.assertEqual(result, [1, 2])

    def test_getItemTaxonomies_max_items(self):
        """
        Test case to verify the getItemTaxonomies function with max items.

        This test ensures that the function correctly returns the max number of taxonomy ids.

        Returns:
            None
        """
        item = {"name": "test item"}
        allItems = [{"id": 1, "items": [{"name": "test"}]}, {"id": 2, "items": [{"name": "item"}]}, {"id": 3, "items": [{"name": "test item"}]}]
        result = getItemTaxonomies(item, allItems) # type: ignore
        self.assertEqual(result, [3, 1, 2])