import csv
import os
import shutil
import time
from argparse import ArgumentParser

from .compiler import compile_scrape_to_guide
from .opendota_api import (
    create_constant_heroes_csv,
    create_constant_items_csv,
    get_hero_popularity_guide,
)
from .utils import (
    constants_heroes,
    constants_items,
    csv_match_string_for_relevant_column,
    cwd,
    data_directory,
    data_file__hero_ids,
    default_dota_itembuilds_windows_directory,
    itembuilds_directory,
)

parser = ArgumentParser(
    prog="OpenDotaGuides",
    description="Making Dota2 guides actually useful & maintainerless",
    epilog="Release options are: -r -c -s",
)

parser.add_argument("-v", action="store_true", help="Prints debug output")
parser.add_argument(
    "-r", action="store_true", help="Refreshes the data pulled from the API"
)
parser.add_argument("-c", action="store_true", help="Recreates the constants")
parser.add_argument("-s", action="store_true", help="Removes start items")
args = parser.parse_args()
task_debug = args.v
refresh_data = args.r
recreate_constants = args.c
remove_start_items = args.s

if __name__ == "__main__":
    if recreate_constants:
        if os.path.exists(constants_heroes):
            os.remove(constants_heroes)
        if os.path.exists(constants_items):
            os.remove(constants_items)
        create_constant_heroes_csv()
        create_constant_items_csv()

    if refresh_data:
        if os.path.exists(data_directory):
            shutil.rmtree(data_directory)
        if os.path.exists(itembuilds_directory):
            shutil.rmtree(itembuilds_directory)
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(itembuilds_directory, exist_ok=True)

    if not os.path.exists(constants_heroes):
        create_constant_heroes_csv()

    with open(constants_heroes) as heroes_csv:
        reader = csv.reader(heroes_csv)
        rows = list(reader)[1:]

    for i, row in enumerate(rows, start=1):
        if row[0] != "131" and f"{row[0]}.json" not in os.listdir(
            data_directory
        ):  # rubberpatch until there is data for ringmaster
            call_successful = 0
            while not call_successful:
                try:
                    get_hero_popularity_guide(row[0])
                    call_successful = 1
                except:
                    if task_debug:
                        print("Waiting for API rate limit")
                    time.sleep(15)
                    get_hero_popularity_guide(row[0])
                    call_successful = 1
            if task_debug:
                print(f"API CALL {i}/{(len(rows)) - 1} {row[1]}")

    data__ids = [file.split(".")[0] for file in os.listdir(data_directory)]
    for i, id in enumerate(data__ids, start=1):
        # if id == "1.json":  # GuideFormatVersion 2 test
        #     compile_scrape_to_guide(id.split(".")[0], 1, 2)
        #     if task_debug:
        #         print(f"v2 COMPILE!! {i}/{(len(data_ids))} {id}")

        if id != data_file__hero_ids:
            compile_scrape_to_guide(id, remove_starting_items=remove_start_items)
            if task_debug:
                print(
                    f"COMPILE {i}/{(len(data__ids))} {csv_match_string_for_relevant_column(constants_heroes,id,1)}"
                )

    if os.path.exists(default_dota_itembuilds_windows_directory):
        build_amt = len(os.listdir(itembuilds_directory))
        for i, itembuild in enumerate(os.listdir(itembuilds_directory), start=1):
            shutil.copy(
                os.path.join(cwd, itembuilds_directory, itembuild),
                os.path.join(default_dota_itembuilds_windows_directory, itembuild),
            )
            if task_debug:
                print(
                    f"MOVE {i}/{build_amt} {csv_match_string_for_relevant_column(constants_heroes,itembuild[:-4],1)}"
                )
    else:
        print(
            "Couldn't find steam installation path, manually replace itembuilds folder."
        )
