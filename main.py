import json
import os
import shutil
import time

from compiler import compile_scrape_to_guide
from opendota_api import get_hero_popularity_guide
from scraper import get_hero_guide, initialize_hero_lib
from utils import (
    cwd,
    data_directory,
    data_file__hero_ids,
    data_hero_ids,
    default_dota_itembuilds_windows_directory,
    itembuilds_directory,
    dotaconstants_directory,
    dotaconstants_heroes,
)

task_debug = 1
scrape = 0
api = 1

if __name__ == "__main__":
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(itembuilds_directory, exist_ok=True)

    # getting data
    if scrape:
        initialize_hero_lib()
        with open(data_hero_ids) as f:
            heroes = json.load(f)

        for i, (hero, id) in enumerate(heroes.items(), start=1):
            if str(id) != "131":  # rubberpatch until there is data for ringmaster
                get_hero_guide(id)
                if task_debug:
                    print(f"SCRAPE {i}/{(len(heroes))} {hero}")
    elif api:
        if os.path.isdir(dotaconstants_directory):
            with open(dotaconstants_heroes) as f:
                heroes = json.load(f)

            for i, hero in enumerate(heroes, start=1):
                if hero != "131" and f"{hero}.json" not in os.listdir(
                    data_directory
                ):  # rubberpatch until there is data for ringmaster
                    call_successful = 0
                    while not call_successful:
                        try:
                            get_hero_popularity_guide(hero)
                            call_successful = 1
                        except:
                            time.sleep(60)
                            get_hero_popularity_guide(hero)
                            call_successful = 1
                    if task_debug:
                        print(f"API CALL {i}/{(len(heroes))}")

    # compiling
    data_hero_ids = os.listdir(data_directory)
    for i, id in enumerate(data_hero_ids, start=1):
        if id != data_file__hero_ids:
            compile_scrape_to_guide(id.split(".")[0])
            if task_debug:
                print(f"COMPILE {i}/{(len(data_hero_ids)) - 1} {id}")

    # copying it to steamfolder
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
