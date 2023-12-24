from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium import webdriver
import json
import sys

def main(id_dict):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options, executable_path = "./chromedriver.exe")

    # TODO: automate getting the current season for the URL

    for name in id_dict.keys():
        # TODO: don't close and re-open driver every time, use a new URL instead
        steamid = id_dict[name]
        url = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/{steamid}/segments/playlist?season=27'
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ranks_json = json.loads(soup.pre.get_text())

        for playlists in ranks_json['data']:
            if playlists['attributes']['playlistId'] == 11:
                doubles_mmr = playlists['stats']['rating']['value']
            elif playlists['attributes']['playlistId'] == 13:
                standard_mmr = playlists['stats']['rating']['value']
            elif playlists['attributes']['playlistId'] == 28:
                rumble_mmr = playlists['stats']['rating']['value']

        print(f'\n{name} mmr list\n----------------\n{doubles_mmr = }\n{standard_mmr = }\n{rumble_mmr = }\n')
    driver.quit()

if __name__ == '__main__':
    steamid_dict = {
        'cooper': '76561198095486223',
        'spencer': '76561198028329488',
        'louis': '76561198127916225',
    }
    
    main(steamid_dict)