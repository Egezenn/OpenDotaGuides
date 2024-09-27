import json
import os
import shutil

from converter import convert_scrape_to_guide
from scraper import get_hero_guide, initialize_hero_lib

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs("itembuilds", exist_ok=True)
    # scraping
    initialize_hero_lib()
    with open("data/hero_ids.json") as f:
        heroes = json.load(f)

    for i, (hero, id) in enumerate(heroes.items(), start=1):
        if str(id) != "131":  # rubberpatch until there is data for ringmaster
            get_hero_guide(id)
            print(f"SCRAPE {i}/{(len(heroes))} {hero}")

    # converting
    hero_ids = os.listdir("data")
    for i, id in enumerate(hero_ids, start=1):
        if id == "hero_ids.json":
            pass
        else:
            convert_scrape_to_guide(id[:-5])
            print(f"CONVERT {i}/{(len(hero_ids)) - 1} {id}")

    # copy it to steamfolder
    cwd = os.getcwd()
    if os.path.exists(
        f"C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/itembuilds/"
    ):
        build_amt = len(os.listdir("itembuilds"))
        for i, itembuild in enumerate(os.listdir("itembuilds"), start=1):
            shutil.copy(
                f"{cwd}/itembuilds/{itembuild}",
                f"C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/itembuilds/{itembuild}",
            )
            print(f"MOVE {i}/{build_amt} {itembuild}")
