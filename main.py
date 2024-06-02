from scraper import initialize_hero_lib, get_hero_guide
from converter import convert_scrape_to_guide
import json
import os

# scraping
initialize_hero_lib()
with open('data/hero_ids.json') as f:
    heroes = json.load(f)

for hero in heroes:
    get_hero_guide(heroes[hero]["hero_id"])

# converting
hero_ids = os.listdir("data")
for id in hero_ids:
    convert_scrape_to_guide(f"{id[:-5]}")
