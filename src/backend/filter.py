import sqlite3
from webscraper.ah import Item
from database.functions import get_all_taxomonies_with_items
import re

def getItemTaxonomies(item:Item, allItems):
    """
    Match the products from the Jumbo and Hoogvliet to the taxonomies from the Albert Heijn. 
    The goal of this is to sort/group similar products between supermarkets. 
    
    To match items from each supermarket this function will check for each new item which taxomony fits
    the best, given the items and taxonomies of AH. 

    Parameters:
    item:(Item): Dictionary with characteristics of an item.
    allItems: a List of Dictionaries describing all items and their taxomony's

    Returns:
    A List with taxonomy id's that fits best to the item.
    
    """
    # Opens the blacklist and takes the item name to the removeBlacklist function.
    # A string without words that are on the blacklist is returned
    blacklist = open("blacklist.txt").read().lower()

    productTitle = removeBlacklist(item["name"].lower(), blacklist)
    
    taxomonies = []
    productTitleSet = set(productTitle.split(" "))

    # Validity parameters, set by trial and error. 
    MIN_SCORE = 0.05
    MAX_ITEMS = 4

    # Compare the itemnames of AH items and the new item. 
    # If the itemname's are an exact match, the new item has the same taxonomies as the AH item. 
    for taxomony in allItems:
        for item in taxomony["items"]:
            name = removeBlacklist(item["name"].lower(), blacklist)
            if name == productTitle and taxomony["id"] not in taxomonies:
                taxomonies.append(taxomony["id"])
    
    # We limit the number of taxonomies to match to a product to avoid diluting the accuracy of the taxonomies.
    # In case the exact match has given us enough taxonomies, we return the list, otherwise we continue.   
    if len(taxomonies) >= MAX_ITEMS:
        return taxomonies
    
    # Look for a close match between the names 
    # We use Jaccard Similarity to give a score to the similarity between the itemnames. 
    # The Jaccard similarity is calculated by dividing the number of observations in both sets by the number of observations in either set.
    suggestedTaxomonies = []
    for taxomony in allItems:
        taxomonyTokens = set()
        for item in taxomony["items"]:
            name = removeBlacklist(item["name"].lower(), blacklist)
            if name == productTitle:
                continue
            taxomonyTokens.update(name.split(" "))
        intersection = len(productTitleSet.intersection(taxomonyTokens))
        union = len(productTitleSet.union(taxomonyTokens))
        similarity = intersection / union if union != 0 else 0
        if similarity > MIN_SCORE:
            suggestedTaxomonies.append((taxomony["id"], similarity))
    
    # We sort the taxonomy-scores from highest to lowest and add the highest scores to the taxomonies list until we reach max. length. 
    suggestedTaxomonies.sort(key=lambda x: x[1], reverse=True)
    for taxomony in suggestedTaxomonies:
        if len(taxomonies) >= MAX_ITEMS:
            break
        if taxomony[0] not in taxomonies:
            taxomonies.append(taxomony[0])
    
    return taxomonies


def removeBlacklist(string:str, blacklist:str):
    """
    Check the string for the 'forbidden' words in the blacklist. 

    Preconditions:
    string: string length > 0
    blacklist: string length > 0

    Parameters: 
    string (str): String of a item name
    blacklist (str): string containing all brands and descriptors that could appear in the item name's.
    
    Returns:
    A string where words that are in the blacklist are replaced with " ". 
    """
    string = string.lower()
    if len(blacklist) == 0:
        return string
    for item in blacklist.split("\n"):
        string = string.replace(item + " ", "")
        pattern = r"\b\d+(\.\d+)?\s*[kmlgKMLG]{1,2}\b"
        string = re.sub(pattern, "", string)
        if item.isdigit():
            string = string.replace(item, "")
    return string.strip()
