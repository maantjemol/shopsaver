import json
from typing import List, TypedDict
from urllib import response
import requests

class Item(TypedDict):
    name: str
    store_id: int
    unit: str # "KG" | "LT" | "stuk" 
    price: int
    sales_price: int
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
    burp0_url = "https://navigator-group1.tweakwise.com:443/navigation/ed681b01?tn_q=&tn_p=0&tn_ps=1000&tn_sort=Relevantie&tn_cid=999999-100&CatalogPermalink=producten&format=json"
    burp0_headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"104\"", "Accept": "*/*", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://www.hoogvliet.com", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.hoogvliet.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
    resp = requests.post(burp0_url, headers=burp0_headers)
    data = resp.json()

    with open('../../../cache/hoogvliet.json', 'w') as f:
        json.dump(data, f)  

    return data

def fetch_data_cache(path:str):
    with open(path, 'r') as f:
        return json.load(f)

def parseProducts(cards) -> List[Item]:
    items = cards['items']
    products = []
    for item in items:
        attributes = item['attributes']
        unit = ''
        price = item['price']
        for attribute in attributes:
            if attribute['name'] == 'BaseUnit':
                unit = attribute['values'][0]
                if unit == 'stuk' or unit == 'stuks':
                    unit = 'stuk'
                elif unit == 'gram':
                    unit = 'KG'
                    price = price * 1000
                elif unit == 'kilo':
                    unit = 'KG'
                elif unit == 'liter':
                    unit = 'LT'
                elif unit == 'milliliter':
                    unit = 'LT'
                    price = price * 1000
            if attribute['name'] == 'RatioBasePackingUnit':
                price = price / float(attribute['values'][0])

        
        product = {
            'name': item['title'],
            'sales_price': item['price'],
            'store_id': 3,
            'unit': unit,
            'price': round(price, 2),
            'url': item['url'],
            'taxomonies': []
        }
        products.append(product)

    return products


if __name__ == "__main__":
    response = fetch_data_cache('../../../cache/hoogvliet.json')
    products = parseProducts(response)
    print(products)

