import json
from typing import List, TypedDict
import requests
from ..database.functions import get_items_by_taxomony

class Item(TypedDict):
    name: str
    store_id: int
    unit: str # "KG" | "LT" | "stuk" 
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
    cookies = {
        'OptanonAlertBoxClosed': '2023-10-20T14:15:16.771Z',
        'country': 'NL',
        'language': 'nl_nl',
        'AKA_A2': 'A',
        'akaas_as': '2147483647~rv=68~id=9483e7cd00161134e452720d719fe618~rn=',
        'ak_bmsc': '6253D471C7C8DCA0CC5429746F7F0647~000000000000000000000000000000~YAAQlEd7XMsxequLAQAAMi+IrhW/Ky1cxCcjstt45yrqWlQ++6weBU3VrYUXnDmJNNKDNijALtSESuLMa+HiQEsr9gMCgyP9PGZgPebGYDuuWnrZyFvHygqYASawBxjveQIq/tq86OVWfSyQboCiFulW2jFBkuonJtVofqLUdPDnwzd9M1KfvTMB023BSuiz120LCMvlSfLSmn1IxNWyJ275cmPVoIl32dlxvprEBfvBgFUrQ7CAHOk7nMUGyVIQGAGGG91H+ttDxU/p0FqQfnKU5jvJDFYMOdJlQ7WXyPYdsYZTeGiF74XTiMn0dfmJI47O9XQWsynUqldMqn332Aj+KI0gD0u4MYiAMWxIOqeT23eNyki4AZVtey1i/HJ57ZgoFEGb39U=',
        'eupubconsent-v2': 'CPz8ITAPz8ITAAcABBENDeCsAP_AAAAAAAYgJugABCAEAAFAAGBwAAAAAAAGgEAEAAAAAAAAAAAAAAAAIAQAEEAAEAAAAAAAAAAAIAIAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAgAABAAAIAAAAAAAAEAAAAAAQAAAAkAAAAAIAEAAAAAAAAAQAAAAABAAAAA-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9-AAAA4JAIAAqACAAGQANAAiABMAH6AvMIACAI4AksMAEACIAEwBJYDGRAAQAIgATAElgMZFAAgAmAEcGAAgAmAEcHQCgAKgAgABkADQAIgATABMAD9AIsAvMcAHACaAIAAhABHAElgJiAXsQgAgBMIAAwAmgEcAXsSgBgBEACYAvMkADACaARwBexSAQABUAEAANAAiABMAH6ARYBeZQAMADIAJoBHAC6gJLATE.f_gAAAAAAAAA',
        'sid': 'IM_p1gepGZqM1WLiRrwrY2SjPq9sWxnJpUJEiqcU',
        'pgid-Jumbo-Grocery-Site': 'Il616KOBfZlSRpBGa9CSWGBm000048Nsq35F',
        'SecureSessionID-DFMKYx4XUhUAAAFISx4r3jVo': '70215037cb2be3b938dc3f95df1f75f93e7de3ac81d37d20deccc20d050f747a',
        'user-session': 'bbabaed0-7e23-11ee-91e5-bb56fbd7526e',
        'authentication-token': '"encryption0@PBEWithMD5AndTripleDES:wnpRoB8bc7Q=|A4W/ilNi30PVzTEMSasQ5IBfvwR0Q4PjvLRB/HjcsvsYtQ1ArV6Hcw=="',
        'bm_mi': '414FF933D1ED8929C9514D29AEFAF283~YAAQr1ozuBv7TaWLAQAAfZOMrhVOP+lpbKyYcHdKV71upYq6KcAxjXWwDW1xD/Ma+P3+NOMnyRKidrPPIbnPnM1LVBqYXK+vwhiVCx0tEqQN+/1zISQBXgYwTuLxVjRhczMtZNBb3877kfKlkGWabYa4pymecxzWijpMUf1wgmkp5t6zhBflxP48Nh9JmVMSa2Ol4VhPO/BvNPSWos0ecDgwusrJPPi+St3uvUUxcvicoue/863vHogc20cgSUCjUF4U4yePBs3V9NQrelYnb79z5isepnQNwVEXR3pqPeOeEgowLaYFrcQojEAObjHdYyny3hVDSx9wAIUKMDRaCGsHEojZ3qxUEQbPzrdDLVVvHApIsg==~1',
        'bm_sv': 'E83A27E0045C0686B5444E3FCA713CCD~YAAQr1ozuKv/TaWLAQAAD9mMrhUrn3bTluYYWhEUSuKc0FuHfZ7w0PbKU6mC5kQNT8q6XzBQS3xABTqJ6eviNbZqibtKUURGEoygR35bCa+MHovRBI0SfWpcnHMTJhMEqMma67TMB7S3W+p9Ebyl7xitWj3gs+t7bV/FUCxtQMNJV3rNyejxzYv2z68+uG1EgYjqmD9Yg7wsejsN+ULWpAg9IGD2LGW41Bhi8zL+LKXCMFL+wG5o0kfkfDTWyv7Z~1',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Nov+08+2023+11%3A50%3A32+GMT%2B0100+(Central+European+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f359bde2-1f28-4f6c-8318-229a9d146260&interactionCount=1&landingPath=NotLandingPage&groups=J1000%3A1%2CJ2000%3A1%2CBG41%3A1&geolocation=NL%3BZH&AwaitingReconsent=false',
        '_dd_s': 'logs=1&id=c99d2c49-111e-4a2d-aebb-2f3005b3c142&created=1699440243017&expire=1699441552698',
    }

    headers = {
        'authority': 'www.jumbo.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.jumbo.com',
        'referer': 'https://www.jumbo.com/producten/aardappelen,-groente-en-fruit/?offSet=24',
        'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    all_data = []

    for i in range(28):
        json_data = {
            'operationName': 'SearchProducts',
            'variables': {
                'input': {
                    'searchType': 'category',
                    'searchTerms': 'producten',
                    'friendlyUrl': 'aardappelen,-groente-en-fruit/?offSet=24',
                    'offSet': 24 * i,
                    'currentUrl': 'https://www.jumbo.com/producten/aardappelen,-groente-en-fruit/',
                    'previousUrl': 'https://www.jumbo.com/producten/aardappelen,-groente-en-fruit/',
                    'bloomreachCookieId': '',
                },
                'shelfTextInput': {
                    'searchType': 'category',
                    'friendlyUrl': 'aardappelen,-groente-en-fruit/?offSet=24',
                },
            },
            'query': 'query SearchProducts($input: ProductSearchInput!, $shelfTextInput: ShelfTextInput!) {\n  searchProducts(input: $input) {\n    redirectUrl\n    removeAllAction {\n      friendlyUrl\n      __typename\n    }\n    pageHeader {\n      headerText\n      count\n      __typename\n    }\n    start\n    count\n    sortOptions {\n      text\n      friendlyUrl\n      selected\n      __typename\n    }\n    categoryTiles {\n      count\n      catId\n      name\n      friendlyUrl\n      imageLink\n      displayOrder\n      __typename\n    }\n    facets {\n      key\n      displayName\n      multiSelect\n      tooltip {\n        linkTarget\n        linkText\n        text\n        __typename\n      }\n      values {\n        ...FacetDetails\n        children {\n          ...FacetDetails\n          children {\n            ...FacetDetails\n            children {\n              ...FacetDetails\n              children {\n                ...FacetDetails\n                children {\n                  ...FacetDetails\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products {\n      ...ProductDetails\n      crossSells {\n        sku\n        __typename\n      }\n      retailSetProducts {\n        ...ProductDetails\n        __typename\n      }\n      __typename\n    }\n    textMessage {\n      header\n      linkText\n      longBody\n      messageType\n      shortBody\n      targetUrl\n      __typename\n    }\n    socialLists {\n      author\n      authorVerified\n      followers\n      id\n      labels\n      productImages\n      thumbnail\n      title\n      __typename\n    }\n    selectedFacets {\n      values {\n        name\n        count\n        friendlyUrl\n        __typename\n      }\n      __typename\n    }\n    breadcrumbs {\n      text\n      friendlyUrl\n      __typename\n    }\n    seo {\n      title\n      description\n      canonicalLink\n      __typename\n    }\n    categoryId\n    shelfDescription\n    __typename\n  }\n  getCategoryShelfText(input: $shelfTextInput) {\n    shelfText\n    __typename\n  }\n}\n\nfragment ProductDetails on Product {\n  id: sku\n  brand\n  category: rootCategory\n  subtitle: packSizeDisplay\n  title\n  image\n  inAssortment\n  availability {\n    availability\n    isAvailable\n    label\n    stockLimit\n    __typename\n  }\n  sponsored\n  auctionId\n  link\n  retailSet\n  prices: price {\n    price\n    promoPrice\n    pricePerUnit {\n      price\n      unit\n      __typename\n    }\n    __typename\n  }\n  quantityDetails {\n    maxAmount\n    minAmount\n    stepAmount\n    defaultAmount\n    __typename\n  }\n  primaryBadge: primaryProductBadges {\n    alt\n    image\n    __typename\n  }\n  secondaryBadges: secondaryProductBadges {\n    alt\n    image\n    __typename\n  }\n  badgeDescription\n  customerAllergies {\n    short\n    __typename\n  }\n  promotions {\n    id\n    group\n    isKiesAndMix\n    image\n    tags {\n      text\n      inverse\n      __typename\n    }\n    start {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    end {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    attachments {\n      type\n      path\n      __typename\n    }\n    primaryBadge: primaryBadges {\n      alt\n      image\n      __typename\n    }\n    __typename\n  }\n  surcharges {\n    type\n    value {\n      amount\n      currency\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FacetDetails on Facet {\n  id\n  count\n  name\n  parent\n  friendlyUrl\n  selected\n  thematicAisle\n  __typename\n}\n',
        }

        response = requests.post('https://www.jumbo.com/api/graphql', cookies=cookies, headers=headers, json=json_data)
        data = response.json()["data"]["searchProducts"]["products"]
        print("progress: " + str(i) + "/" + str(27))
        all_data.extend(data)
    with open('../../../cache/jumbo.json', 'w') as f:
        json.dump(all_data, f)  

    return all_data

def fetch_data_cache(path:str):
    with open(path, 'r') as f:
        return json.load(f)

def parseProducts(cards) -> List[Item]:
    new_products:List[Item] = []
    for product in cards:
        # price per unit = pieces
        unit = "stuk"
        if product["prices"]["pricePerUnit"]["unit"] == "kg":
            unit = "KG"
        if product["prices"]["pricePerUnit"]["unit"] == "l":
            unit = "LT"

        new_product:Item = {
            "name": product["title"],
            "price": product["prices"]["pricePerUnit"]["price"],
            "unit": unit,
            'store_id': 2,
            "url": "https://jumbo.com" + product["link"],
            'taxomonies': []
        }
        new_products.append(new_product)
    return new_products


if __name__ == "__main__":
    response = fetch_data_cache('../../../cache/jumbo.json')
    products = parseProducts(response)
    print(products)

