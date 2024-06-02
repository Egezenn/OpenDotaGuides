from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from json import dump
import time

def get_soup(url):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def initialize_hero_lib():
    soup = get_soup("https://www.opendota.com/heroes")
    hero_selector = "tbody > tr > td > div > div > div[class=textContainer] > span"
    heroes = soup.select(hero_selector)

    hero_dict = {}
    for item in heroes:
        hero_name = item.text
        hero_id = item.find("a")["href"].split("/")[2]
        hero_dict[hero_name] = {
            "hero_id": hero_id
        }

    with open("data\hero_ids.json", "w") as json_file:
        dump(hero_dict, json_file, indent=2)

def get_hero_guide(hero_id):
    soup = get_soup(f"https://www.opendota.com/heroes/{hero_id}/items")
    start_game_selector = "tbody > tr > td:nth-of-type(1) > div"
    early_game_selector = "tbody > tr > td:nth-of-type(2) > div"
    mid_game_selector = "tbody > tr > td:nth-of-type(3) > div"
    late_game_selector = "tbody > tr > td:nth-of-type(4) > div"

    start_game_items = soup.select(start_game_selector)
    early_game_items = soup.select(early_game_selector)
    mid_game_selector = soup.select(mid_game_selector)
    late_game_selector = soup.select(late_game_selector)
    start_game_items_list = []
    early_game_items_list = []
    mid_game_items_list = []
    late_game_items_list = []

    for item in start_game_items:
        start_game_items_list.append(item.find("div").find("object")["data"][74:-4])

    for item in early_game_items:
        early_game_items_list.append(item.find("div").find("object")["data"][74:-4])

    for item in mid_game_selector:
        mid_game_items_list.append(item.find("div").find("object")["data"][74:-4])

    for item in late_game_selector:
        late_game_items_list.append(item.find("div").find("object")["data"][74:-4])

    hero_item_dict = {
        "start_game": start_game_items_list,
        "early_game": early_game_items_list,
        "mid_game": mid_game_items_list,
        "late_game": late_game_items_list
    }

    with open(f"data\\{hero_id}.json", "w") as json_file:
        dump(hero_item_dict, json_file, indent=2)
