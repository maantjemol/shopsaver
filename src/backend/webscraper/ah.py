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
    sales_price: int

class Taxomony(TypedDict):
    id: int
    name: str

class Store(TypedDict):
    id: int
    name: str
    url: str


def fetch_data():
    cookies = {
        'uuid': 'CFE9508F-8743-4C6E-9102-3F6BFFC9E863',
        'SSLB': '1',
        'SSOD': 'AC1pAAAAJADqkwAAAgAAABJ7OmXdB0FlAAC_egAADQAAAGN7OmXkc0NlAAAAAA',
        '_csrf': '-vvZDZkapYQcvnS5i5giXcu8',
        'i18next': 'nl-nl',
        'Ahonlnl-Prd-01-DigitalDev-B2': '!3u1OvB5Klx16X+Exv2qJuN1Jd/CM19xfVJfnruoEWp/LmpEnLeE/lZV28B0tLeJF4jhgf0ABt38xIw==',
        'Ahonlnl-Prd-01-DigitalDev-F1': '!LcParI/YYXKqaiOP0amA6Yq9WtZV0cyQ14dQ7n/9Cc8+fEsvaHA2aHHloAdFppe2iGNqIllLyXph7Jo=',
        'SSID': 'CQB-rR0qABgAAACLrgFlldTBAIuuAWUMAAAAAAAAAAAA5tVdZQBUmscKAAGh0QAA5tVdZQEA5goAAYvSAADm1V1lAQDiCgABedIAAObVXWUBAKcKAAAEBwAA2woAANQKAABGCQAAzAoAAA',
        'SSSC': '4.G7278290384843822229.12|2759.53665:2786.53881:2790.53899',
        'ak_bmsc': 'ED88E3B7157D00403ED6D78F2AD0B21B~000000000000000000000000000000~YAAQo/1IF6dFYN+LAQAAFZGL9hW9UeX3SRrnC2kw/6fwU4LaBvmGnPXzhStrQSq2YTK0/JbnSW7dtedVM4QjoAh5VNBZnSjWIsWyXZ2jGR2J/NkfbLnyH83vVpjJUiAQ+Y39TaeLgO8BX3P3UpqNZU5lo2OoAPd9e+fT1zjrhqTp7ZKMdLkB8fW/N3tdQRDhXku0lvWHRjH+vJBZIJ0i07wKh6vin8/lZtjYVE135GNI0/BOhMVwuweGeyfiZKzW2fzrcx/Eg/rq6x7NE4vqQX8aYlwThH+I45aE8lKoLUqumLyxLfkOFIjmitz46OSO1oroo8CbAXSnhLFB3CDDNlzW3Ap+z9sm7S+uo36ALSQWxsGnlBazAA9uaeKtHni0L6Iwysm3N6M=',
        'bm_sz': '7A44579634F8EA770D67CD8EF514B85F~YAAQo/1IF6lFYN+LAQAAFZGL9hXDc7Cdw+5aXPIg+uhobS4505/cLreFd2UdkQVPWtznW3sQ/PThG/STV+h0Oozi/hl1LmTS+J/fUBUInye1fuS3G6P/C+yaNzmiNVpdbEA4xTvf10LcPZAosEtSFBhF1QirMn0iVvulMmh3G9bWN8gl7PiVsEJ+025ZjUVU6sNXvDFNOu1PwnsbiHgtf5wj6UP+/JJjZRVBSFmY5cYZWWrAoUwZ/lEcAduK+dW7uGAY/PU7WecjzTaoLUI3fgaJsNtCgv6qr6R9qvtTznoA9Q==~4404294~3158320',
        '_abck': 'A877B95C3EF28C5E5394B0C64590F9E8~0~YAAQo/1IF9BFYN+LAQAAypKL9goMkajSQR0t+5J/t+7kRhOsJpFAwNs5+kLA2pT3Aj3JLfRUCvTXYmpxKnt5zNo83f88g2uOK4dJ8N4oPmzxHHZJrGLSyOgYS5u4Hk/jLiPAfkpmR95UaAf3RRH0iUCgP/oiD32QJM7q2GmUbltmrXFn/rbHvbaQZvmQptf0Vo2JFrZtdpD/PpDvmMooMaD1tZEhIwS9S1fNjktbnKjnaxvW0paZ8Kl/QRVKHKoJZYeXFeLdb7AzkP9V09A2457ev0JK1g9H52OwBV6qKiGekiuBg93RbUQwCRELQKqaSQMK660JPOP3l/GJO3T201B2z2Gk4LExQrzrtgLGs2C6Rnk6/wXEpDbQMfSpvS+tGauAmfoLxnLEQ6M164YSB2TTb6i8YLo=~-1~-1~1700651950',
        'SSRT': 'WtddZQABAA',
        'SSPV': 'JgMAAAAAAAAAAwAAAAAAAAAAAAQAAAAAAAAAAAAA',
        'bm_mi': '0FDD2E06D6402514CC619892EC8E1567~YAAQo/1IF3ncYN+LAQAAHDqR9hXMfIi8tds0H1t2201gv4GjFuDnnTTJH6VV50eYXHr9EljBvPU4livlUpvIaMoybNrhtKT+o7yK8B66KNSmoqxOjn4RqFRAMaigLjgeG+FPzVd/AUeWqFMi3Uw+8EQzfPFGwbTC+fO6qfwETFiJL2xRDUVmOwG6W8jnZTwQyEdc01PmIlIE+ifd6Ak0vg+eMN1kbJ0gF80IwOY4kLQnzWjb6kY5pO6MFq8CDYK9xxtpRttt78XjdyjBABCc8y6DoINSKQSSaG3UptlTOgtjYu0wFVoQq25WgwKQpt3aLB5wSr+CLe5iDNdUcVaaVZHnsr/Y7EgCy1HmbO4=~1',
        'bm_sv': 'B0C1AF8EC6E221BA47B59B3347625D26~YAAQo/1IFwzdYN+LAQAAgz2R9hX1CWb0JZBB2rRQ2yaKsnXhqd5ppg2xHtigNxXwLY9j//QJJPHZw1pQYgylJNGS+yRYMVOBznN4oBNFbMVNM/zopHQG3m+nRn7ElVkZzoLIjqrf7P1swXfwnsXYrf0y/87/oT3o2j2RiZj6EuJXZztZoeSGlhg78zHQLbUsxmyHV2Vg+N0KANGlu4pyAlfwYvRPxP34PCebW6gERpsQVfXsNyxEgT1hTdxpuTU=~1',
    }

    headers = {
        'authority': 'www.ah.nl',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
        'content-type': 'application/json',
        # 'cookie': 'uuid=CFE9508F-8743-4C6E-9102-3F6BFFC9E863; SSLB=1; SSOD=AC1pAAAAJADqkwAAAgAAABJ7OmXdB0FlAAC_egAADQAAAGN7OmXkc0NlAAAAAA; _csrf=-vvZDZkapYQcvnS5i5giXcu8; i18next=nl-nl; Ahonlnl-Prd-01-DigitalDev-B2=!3u1OvB5Klx16X+Exv2qJuN1Jd/CM19xfVJfnruoEWp/LmpEnLeE/lZV28B0tLeJF4jhgf0ABt38xIw==; Ahonlnl-Prd-01-DigitalDev-F1=!LcParI/YYXKqaiOP0amA6Yq9WtZV0cyQ14dQ7n/9Cc8+fEsvaHA2aHHloAdFppe2iGNqIllLyXph7Jo=; SSID=CQB-rR0qABgAAACLrgFlldTBAIuuAWUMAAAAAAAAAAAA5tVdZQBUmscKAAGh0QAA5tVdZQEA5goAAYvSAADm1V1lAQDiCgABedIAAObVXWUBAKcKAAAEBwAA2woAANQKAABGCQAAzAoAAA; SSSC=4.G7278290384843822229.12|2759.53665:2786.53881:2790.53899; ak_bmsc=ED88E3B7157D00403ED6D78F2AD0B21B~000000000000000000000000000000~YAAQo/1IF6dFYN+LAQAAFZGL9hW9UeX3SRrnC2kw/6fwU4LaBvmGnPXzhStrQSq2YTK0/JbnSW7dtedVM4QjoAh5VNBZnSjWIsWyXZ2jGR2J/NkfbLnyH83vVpjJUiAQ+Y39TaeLgO8BX3P3UpqNZU5lo2OoAPd9e+fT1zjrhqTp7ZKMdLkB8fW/N3tdQRDhXku0lvWHRjH+vJBZIJ0i07wKh6vin8/lZtjYVE135GNI0/BOhMVwuweGeyfiZKzW2fzrcx/Eg/rq6x7NE4vqQX8aYlwThH+I45aE8lKoLUqumLyxLfkOFIjmitz46OSO1oroo8CbAXSnhLFB3CDDNlzW3Ap+z9sm7S+uo36ALSQWxsGnlBazAA9uaeKtHni0L6Iwysm3N6M=; bm_sz=7A44579634F8EA770D67CD8EF514B85F~YAAQo/1IF6lFYN+LAQAAFZGL9hXDc7Cdw+5aXPIg+uhobS4505/cLreFd2UdkQVPWtznW3sQ/PThG/STV+h0Oozi/hl1LmTS+J/fUBUInye1fuS3G6P/C+yaNzmiNVpdbEA4xTvf10LcPZAosEtSFBhF1QirMn0iVvulMmh3G9bWN8gl7PiVsEJ+025ZjUVU6sNXvDFNOu1PwnsbiHgtf5wj6UP+/JJjZRVBSFmY5cYZWWrAoUwZ/lEcAduK+dW7uGAY/PU7WecjzTaoLUI3fgaJsNtCgv6qr6R9qvtTznoA9Q==~4404294~3158320; _abck=A877B95C3EF28C5E5394B0C64590F9E8~0~YAAQo/1IF9BFYN+LAQAAypKL9goMkajSQR0t+5J/t+7kRhOsJpFAwNs5+kLA2pT3Aj3JLfRUCvTXYmpxKnt5zNo83f88g2uOK4dJ8N4oPmzxHHZJrGLSyOgYS5u4Hk/jLiPAfkpmR95UaAf3RRH0iUCgP/oiD32QJM7q2GmUbltmrXFn/rbHvbaQZvmQptf0Vo2JFrZtdpD/PpDvmMooMaD1tZEhIwS9S1fNjktbnKjnaxvW0paZ8Kl/QRVKHKoJZYeXFeLdb7AzkP9V09A2457ev0JK1g9H52OwBV6qKiGekiuBg93RbUQwCRELQKqaSQMK660JPOP3l/GJO3T201B2z2Gk4LExQrzrtgLGs2C6Rnk6/wXEpDbQMfSpvS+tGauAmfoLxnLEQ6M164YSB2TTb6i8YLo=~-1~-1~1700651950; SSRT=WtddZQABAA; SSPV=JgMAAAAAAAAAAwAAAAAAAAAAAAQAAAAAAAAAAAAA; bm_mi=0FDD2E06D6402514CC619892EC8E1567~YAAQo/1IF3ncYN+LAQAAHDqR9hXMfIi8tds0H1t2201gv4GjFuDnnTTJH6VV50eYXHr9EljBvPU4livlUpvIaMoybNrhtKT+o7yK8B66KNSmoqxOjn4RqFRAMaigLjgeG+FPzVd/AUeWqFMi3Uw+8EQzfPFGwbTC+fO6qfwETFiJL2xRDUVmOwG6W8jnZTwQyEdc01PmIlIE+ifd6Ak0vg+eMN1kbJ0gF80IwOY4kLQnzWjb6kY5pO6MFq8CDYK9xxtpRttt78XjdyjBABCc8y6DoINSKQSSaG3UptlTOgtjYu0wFVoQq25WgwKQpt3aLB5wSr+CLe5iDNdUcVaaVZHnsr/Y7EgCy1HmbO4=~1; bm_sv=B0C1AF8EC6E221BA47B59B3347625D26~YAAQo/1IFwzdYN+LAQAAgz2R9hX1CWb0JZBB2rRQ2yaKsnXhqd5ppg2xHtigNxXwLY9j//QJJPHZw1pQYgylJNGS+yRYMVOBznN4oBNFbMVNM/zopHQG3m+nRn7ElVkZzoLIjqrf7P1swXfwnsXYrf0y/87/oT3o2j2RiZj6EuJXZztZoeSGlhg78zHQLbUsxmyHV2Vg+N0KANGlu4pyAlfwYvRPxP34PCebW6gERpsQVfXsNyxEgT1hTdxpuTU=~1',
        'dnt': '1',
        'referer': 'https://www.ah.nl/producten/aardappel-groente-fruit?page=1',
        'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
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
                "sales_price": product["price"]["now"],
                "unit": unit_size, 
                "url": 'https://www.ah.nl' + product["link"],
                "taxomonies": taxonomies
            }

            if new_product not in new_products:
                new_products.append(new_product)

    return new_products
