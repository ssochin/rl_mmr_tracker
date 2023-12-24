from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium import webdriver
import json
import sys

DOUBLES_PLAYLIST_ID = 11
STANDARD_PLAYLIST_ID = 13
RUMBLE_PLAYLST_ID = 27

def main(id_dict):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # runs without opening a window for the browser
    driver = uc.Chrome(options=options, executable_path = "./chromedriver.exe")

    for name in id_dict.keys():
        steamid = id_dict[name]
        url = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/{steamid}'

        try:
            driver.get(url)
        except:
            print("HTML GET failed, check the API URL.")
            driver.quit()
            return

        # get html source
        html = driver.page_source

        # use bs4 to parse html because i'm lazy
        parsed_html = BeautifulSoup(html, 'html.parser')

        # json-ify text from "pre" section of html (where all the json info is)
        try:
            profile_json = json.loads(parsed_html.pre.get_text())
        except:
            print("JSON parsing error, check the API URL.")
            driver.quit()
            return

        # get each mmr value based on the playlist ID
        for playlist in profile_json['data']['segments']:

            # skip overview segment, parse playlists only
            if (playlist['type'] == 'overview'):
                continue

            if playlist['attributes']['playlistId'] == DOUBLES_PLAYLIST_ID:
                doubles_mmr = playlist['stats']['rating']['value']
            elif playlist['attributes']['playlistId'] == STANDARD_PLAYLIST_ID:
                standard_mmr = playlist['stats']['rating']['value']
            elif playlist['attributes']['playlistId'] == RUMBLE_PLAYLST_ID:
                rumble_mmr = playlist['stats']['rating']['value']

        print(f'\n{name} mmr list\n----------------\n{doubles_mmr = }\n{standard_mmr = }\n{rumble_mmr = }\n')

    driver.quit()

if __name__ == '__main__':
    steamid_dict = {
        'cooper': '76561198095486223',
        'spencer': '76561198028329488',
        'louis': '76561198127916225',
    }
    
    main(steamid_dict)