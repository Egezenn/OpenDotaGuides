import os
from json import dump

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import data_file__hero_ids, data_directory, data_hero_ids

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.page_load_strategy = "none"


def get_soup(url, selector):
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 120)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    return soup


def initialize_hero_lib():
    if data_file__hero_ids not in os.listdir(data_directory):
        hero_selector = "tbody > tr > td > div > div > div[class=textContainer] > span"
        soup = get_soup("https://www.opendota.com/heroes", hero_selector)
        heroes = soup.select(hero_selector)

        hero_dict = {}
        for item in heroes:
            hero_name = item.text
            hero_id = item.find("a")["href"].split("/")[2]
            hero_dict[hero_name] = hero_id

        with open(data_hero_ids, "w") as json_file:
            dump(hero_dict, json_file, indent=2)


def get_hero_guide(hero_id):
    if f"{hero_id}.json" not in os.listdir(data_directory):
        start_game_selector = "tbody > tr > td:nth-of-type(1) > div"
        early_game_selector = "tbody > tr > td:nth-of-type(2) > div"
        mid_game_selector = "tbody > tr > td:nth-of-type(3) > div"
        late_game_selector = "tbody > tr > td:nth-of-type(4) > div"
        soup = get_soup(
            f"https://www.opendota.com/heroes/{hero_id}/items", late_game_selector
        )

        start_game_items = soup.select(start_game_selector)
        early_game_items = soup.select(early_game_selector)
        mid_game_selector = soup.select(mid_game_selector)
        late_game_selector = soup.select(late_game_selector)
        start_game_items_list = []
        early_game_items_list = []
        mid_game_items_list = []
        late_game_items_list = []

        for item in start_game_items:
            start_game_items_list.append(item.find("div").find("img")["src"][74:-4])

        for item in early_game_items:
            early_game_items_list.append(item.find("div").find("img")["src"][74:-4])

        for item in mid_game_selector:
            mid_game_items_list.append(item.find("div").find("img")["src"][74:-4])

        for item in late_game_selector:
            late_game_items_list.append(item.find("div").find("img")["src"][74:-4])

        hero_item_dict = {
            "start_game": start_game_items_list,
            "early_game": early_game_items_list,
            "mid_game": mid_game_items_list,
            "late_game": late_game_items_list,
        }

        with open(data_hero_ids, "w") as json_file:
            dump(hero_item_dict, json_file, indent=2)
