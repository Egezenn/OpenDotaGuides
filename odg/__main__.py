from argparse import ArgumentParser
import csv
import logging
import os
import shutil
import time

import compiler
import opendota_api
import utils


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="OpenDotaGuides",
        description="Making Dota2 guides actually useful & maintainerless",
        epilog="Release options are: -r -c",
    )

    parser.add_argument(
        "-v", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="WARNING", help="Set the logging level"
    )
    parser.add_argument("-r", action="store_true", help="Refreshes the data pulled from the API")
    parser.add_argument("-c", action="store_true", help="Recreates the constants")
    parser.add_argument("-k", action="store_true", help="Keep start items")
    args = parser.parse_args()
    verbosity = args.v
    refresh_data = args.r
    recreate_constants = args.c
    keep_start_items = args.k

    if os.path.exists(utils.logfile):
        os.remove(utils.logfile)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=verbosity, filename=utils.logfile)
    logger.debug(
        f"Got CLI args as:\n\tv(verbosity): {args.v}\n\tr(refresh_data): {args.r}\n\tc(create_constants): {args.c}\n\tk(keep_start_items): {args.k}"
    )

    if recreate_constants or not os.path.exists(utils.constants_heroes):
        logger.debug(f"Creating/overwriting file {utils.constants_heroes}..")
        opendota_api.create_constant_heroes_csv()

    if recreate_constants or not os.path.exists(utils.constants_items):
        logger.debug(f"Creating/overwriting file {utils.constants_items}..")
        opendota_api.create_constant_items_csv()

    if refresh_data:
        logger.debug(f"Refreshing the data..")
        if os.path.exists(utils.data_directory):
            logger.debug(f"Directory {utils.data_directory} exists, deleting..")
            shutil.rmtree(utils.data_directory)
        if os.path.exists(utils.itembuilds_directory):
            logger.debug(f"Directory {utils.itembuilds_directory} exists, deleting..")
            shutil.rmtree(utils.itembuilds_directory)
    os.makedirs(utils.data_directory, exist_ok=True)
    logger.debug(f"Creating {utils.data_directory} directory..")
    os.makedirs(utils.itembuilds_directory, exist_ok=True)
    logger.debug(f"Creating {utils.itembuilds_directory} directory..")

    with open(utils.constants_heroes) as heroes_csv:
        reader = csv.reader(heroes_csv)
        rows = list(reader)[1:]

    if refresh_data:
        for i, row in enumerate(rows, start=1):
            call_successful = 0
            logger.info(f"Doing API call {i}/{(len(rows)) - 1} {row[1]}")
            # could recurse with limits if paralleled, fine for now
            while not call_successful:
                try:
                    opendota_api.get_hero_popularity_guide(row[0])
                    call_successful = 1
                except:
                    logger.info(f"Waiting for API rate limit..")
                    time.sleep(15)
                    opendota_api.get_hero_popularity_guide(row[0])
                    call_successful = 1

    data__ids = [file.split(".")[0] for file in os.listdir(utils.data_directory)]
    for i, id in enumerate(data__ids, start=1):
        logger.info(
            f"Compiling file {i}/{(len(data__ids))} {utils.csv_match_string_for_relevant_column(utils.constants_heroes, id, 1)}"
        )
        compiler.compile_scrape_to_guide_vdf(id, keep_starting_items=keep_start_items)

    if os.path.exists(utils.default_dota_itembuilds_windows_directory):
        build_amt = len(os.listdir(utils.itembuilds_directory))
        for i, itembuild in enumerate(os.listdir(utils.itembuilds_directory), start=1):
            logger.info(
                f"Moving file {i}/{build_amt} {utils.csv_match_string_for_relevant_column(utils.constants_heroes, itembuild[:-4], 1)}"
            )
            shutil.copy(
                os.path.join(utils.itembuilds_directory, itembuild),
                os.path.join(utils.default_dota_itembuilds_windows_directory, itembuild),
            )
    else:
        logger.error("Couldn't find steam installation path, manually replace itembuilds folder.")
