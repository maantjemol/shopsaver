import webscraper.ah as ah
import webscraper.jumbo as jumbo
import webscraper.hoogvliet as hoogvliet

def buildCache():
    path = "../../cache/"
    print("Building cache...")
    print("Fetching data from AH")
    try:
        ah.fetch_data("../../cache/ah.json")
    except:
        print("Error fetching data from AH")
    print("Fetching data from Jumbo")
    try:
        jumbo.fetch_data("../../cache/jumbo.json")
    except:
        print("Error fetching data from Jumbo")
    print("Fetching data from Hoogvliet")
    try:
        hoogvliet.fetch_data("../../cache/hoogvliet.json")
    except:
        print("Error fetching data from Hoogvliet")
    print("Done building cache")

if __name__ == "__main__":
    buildCache()