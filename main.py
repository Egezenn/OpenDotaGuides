import json
import os
import shutil

from compiler import compile_scrape_to_guide
from scraper import get_hero_guide, initialize_hero_lib
from utils import (
    data_directory,
    data_hero_ids,
    cwd,
    itembuilds_directory,
    default_dota_itembuilds_windows_directory,
    data_file__hero_ids,
)

task_debug = 1

if __name__ == "__main__":
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(itembuilds_directory, exist_ok=True)

    # scraping
    initialize_hero_lib()
    with open(data_hero_ids) as f:
        heroes = json.load(f)

    for i, (hero, id) in enumerate(heroes.items(), start=1):
        if str(id) != "131":  # rubberpatch until there is data for ringmaster
            get_hero_guide(id)
            if task_debug:
                print(f"SCRAPE {i}/{(len(heroes))} {hero}")

    # converting
    data_hero_ids = os.listdir(data_directory)
    for i, id in enumerate(data_hero_ids, start=1):
        if id != data_file__hero_ids:
            compile_scrape_to_guide(id.split(".")[0])
            if task_debug:
                print(f"CONVERT {i}/{(len(data_hero_ids)) - 1} {id}")

    # copy it to steamfolder
    if os.path.exists(default_dota_itembuilds_windows_directory):
        build_amt = len(os.listdir(itembuilds_directory))
        for i, itembuild in enumerate(os.listdir(itembuilds_directory), start=1):
            shutil.copy(
                os.path.join(cwd, itembuilds_directory, itembuild),
                os.path.join(default_dota_itembuilds_windows_directory, itembuild),
            )
            if task_debug:
                print(f"MOVE {i}/{build_amt} {itembuild}")
    else:
        print(
            "Couldn't find steam installation path, manually replace itembuilds folder."
        )
