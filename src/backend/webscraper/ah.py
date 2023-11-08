from typing import List, TypedDict
import requests
import json

class Item(TypedDict):
    name: str
    store_id: int
    unit: str # "kilo" | "liter" | "stuk" 
    price: int
    url: str 
    taxomonies: List[str] # taxemony ids

class Taxomony(TypedDict):
    id: int
    name: str

class Store(TypedDict):
    id: int
    name: str
    url: str


def fetch_data():
  headers = {
      'authority': 'www.ah.nl',
      'accept': 'application/json',
      'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
      'content-type': 'application/json',
      'dnt': '1',
      'referer': 'https://www.ah.nl/producten/aardappel-groente-fruit?page=1',
      'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
  }

  all_products = []

  for i in range(2):
    params = {
        'page': i,
        'size': '1000',
        'taxonomySlug': 'aardappel-groente-fruit',
    }

    response = requests.get('https://www.ah.nl/zoeken/api/products/search', params=params, headers=headers)
    products = response.json()["cards"]
    all_products.extend(products)

  with open('../../../cache/ah.json', 'w') as f:
    json.dump(all_products, f)  

  return all_products


def fetch_data_cache(path:str):
    with open(path, 'r') as f:
        return json.load(f)

def parseTaxonomies(cards) -> List[Taxomony]:
    taxonomies:List[Taxomony] = []
    for products in cards:
        for product in products["products"]:
            for taxonomy in product["taxonomies"]:
                new_tax:Taxomony = {"name": taxonomy["name"], "id": taxonomy["id"]}
                if new_tax not in taxonomies:
                    taxonomies.append({"name": taxonomy["name"], "id": taxonomy["id"]})
    return taxonomies

def parseProducts(cards) -> List[Item]:
    new_products:List[Item] = []
    for products in cards:
        for product in products["products"]:
            taxonomies = []
            for taxonomy in product["taxonomies"]:
                taxonomies.append(str(taxonomy["id"]))
            
            unit_size = "stuk"
            price = product["price"]["now"]

            if "unitInfo" in product["price"]:
                unit_size = product["price"]["unitInfo"]["description"]
                price = product["price"]["unitInfo"]["price"]



            new_product:Item = {
                "name": product["title"],
                "store_id": 1,
                "price": price,
                "unit": unit_size, 
                "url": 'https://www.ah.nl' + product["link"],
                "taxomonies": taxonomies
            }

            if new_product not in new_products:
                new_products.append(new_product)

    return new_products
