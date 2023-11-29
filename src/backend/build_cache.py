import webscraper.ah as ah
import webscraper.jumbo as jumbo
import webscraper.hoogvliet as hoogvliet

def buildCache():
    path = "../../cache/"
    print("Building cache...")
    print("Fetching data from AH")
    ah.fetch_data()
    print("Fetching data from Jumbo")
    jumbo.fetch_data()
    print("Fetching data from Hoogvliet")
    hoogvliet.fetch_data()
