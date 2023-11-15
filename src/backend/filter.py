import sqlite3
from webscraper.ah import Item
from database.functions import get_all_taxomonies_with_items
import re

def getItemTaxonomies(item:Item, allItems):
    blacklist = open("blacklist.txt").read().lower()

    productTitle = removeBlacklist(item["name"].lower(), blacklist)
    
    taxomonies = []
    productTitleSet = set(productTitle.split(" "))

    MIN_SCORE = 0.05
    MAX_ITEMS = 4

    for taxomony in allItems:
        for item in taxomony["items"]:
            name = removeBlacklist(item["name"].lower(), blacklist)
            if name == productTitle and taxomony["id"] not in taxomonies:
                taxomonies.append(taxomony["id"])
    
    if len(taxomonies) >= MAX_ITEMS:
        return taxomonies
    
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
    
    suggestedTaxomonies.sort(key=lambda x: x[1], reverse=True)
    for taxomony in suggestedTaxomonies:
        if len(taxomonies) >= MAX_ITEMS:
            break
        if taxomony[0] not in taxomonies:
            taxomonies.append(taxomony[0])
    
    return taxomonies


def removeBlacklist(string:str, blacklist:str):
    string = string.lower()
    for item in blacklist.split("\n"):
        string = string.replace(item + " ", "")
        pattern = r"\b\d+(\.\d+)?\s*[kmlgKMLG]{1,2}\b"
        string = re.sub(pattern, "", string)
        if item.isdigit():
            string = string.replace(item, "")
    return string.strip()
