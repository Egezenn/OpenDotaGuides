import json
import os
import shutil
import time

from .compiler import compile_scrape_to_guide
from .opendota_api import get_hero_popularity_guide
from .utils import (
    cwd,
    data_directory,
    data_file__hero_ids,
    default_dota_itembuilds_windows_directory,
    itembuilds_directory,
    dotaconstants_directory,
    dotaconstants_heroes,
)

task_debug = 1
refresh_data = 1
remove_start_items = 1

if __name__ == "__main__":
    if refresh_data:
        if os.path.exists(data_directory):
            shutil.rmtree(data_directory)
        if os.path.exists(itembuilds_directory):
            shutil.rmtree(itembuilds_directory)
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(itembuilds_directory, exist_ok=True)

    # getting data

    if os.path.exists(dotaconstants_directory):
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
                        time.sleep(15)
                        get_hero_popularity_guide(hero)
                        call_successful = 1
                if task_debug:
                    print(f"API CALL {i}/{(len(heroes)) - 1}")
    else:
        print(f"{dotaconstants_directory} couldn't be found")
        exit()

    # compiling
    data__ids = [file.split(".")[0] for file in os.listdir(data_directory)]
    for i, id in enumerate(data__ids, start=1):
        # if id == "1.json":  # GuideFormatVersion 2 test
        #     compile_scrape_to_guide(id.split(".")[0], 1, 2)
        #     if task_debug:
        #         print(f"v2 COMPILE!! {i}/{(len(data_ids))} {id}")

        if id != data_file__hero_ids:
            compile_scrape_to_guide(id, remove_starting_items=remove_start_items)
            if task_debug:
                print(f"COMPILE {i}/{(len(data__ids))} {id}")

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
