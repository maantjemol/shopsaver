import sqlite3
from webscraper.ah import Item
from database.functions import get_all_taxomonies_with_items



def getItemTaxonomies(item:Item):
    connection = sqlite3.connect("../../database/main.sqlite")
    allItems = get_all_taxomonies_with_items(connection)

    productTitle = item["name"].lower()
    
    taxomonies = []

    for taxomony in allItems:
        for item in taxomony["items"]:
            name = removeBlacklist(item["name"].lower())
            if name == removeBlacklist(productTitle):
                taxomonies.append(taxomony["id"])
    
    for taxomony in allItems:
        taxomonyTokens = []
        nameTokens = set(productTitle.split(" "))
        for item in taxomony["items"]:
            name = removeBlacklist(item["name"].lower())
            if taxomony["id"] == 4979:
                print(name)
            if name == removeBlacklist(productTitle):
                continue
            taxomonyTokens.extend(name.split(" "))
        taxomonyTokensSet = set(taxomonyTokens)
        intersection = len(nameTokens.intersection(taxomonyTokensSet))
        union = len(nameTokens.union(taxomonyTokensSet))
        similarity = intersection / union if union != 0 else 0
        if similarity > 0:
            print(similarity, taxomony["id"])
    return taxomonies


def removeBlacklist(string:str):
    blacklist = open("blacklist.txt").read().lower()
    for item in blacklist.split("\n"):
        string = string.replace(item + " ", "")
    return string




if __name__ == "__main__":
    product:Item = {
        'name': 'AH komkommer', 
        'store_id': 1, 
        'unit': 'KG', 
        'price': "8.26", 
        'url': 'https://www.ah.nl/producten/product/wi443204/ah-pompoen-lasagneblad', 
        'taxomonies': []
    }

    print(getItemTaxonomies(product))