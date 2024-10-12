import csv
import logging
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
    logfile,
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="OpenDotaGuides",
        description="Making Dota2 guides actually useful & maintainerless",
        epilog="Release options are: -r -c -s",
    )

    parser.add_argument(
        "-v",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level",
    )
    parser.add_argument(
        "-r", action="store_true", help="Refreshes the data pulled from the API"
    )
    parser.add_argument("-c", action="store_true", help="Recreates the constants")
    parser.add_argument("-s", action="store_true", help="Remove start items")
    args = parser.parse_args()
    verbosity = args.v
    refresh_data = args.r
    recreate_constants = args.c
    remove_start_items = args.s

    if os.path.exists(logfile):
        os.remove(logfile)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=verbosity,
        filename=logfile,
    )
    logger.debug(
        f"Got CLI args as:\n\tv(verbosity): {args.v}\n\tr(refresh_data): {args.r}\n\tc(create_constants): {args.c}\n\ts(remove_start_items): {args.s}"
    )

    if recreate_constants:
        logger.debug(f"Recreating constants..")
        if os.path.exists(constants_heroes):
            logger.debug(f"File {constants_heroes} exists, deleting..")
            os.remove(constants_heroes)
        if os.path.exists(constants_items):
            logger.debug(f"File {constants_items} exists, deleting..")
            os.remove(constants_items)
        logger.debug(f"Creating file {constants_heroes}..")
        create_constant_heroes_csv()
        logger.debug(f"Creating file {constants_items}..")
        create_constant_items_csv()

    if refresh_data:
        logger.debug(f"Refreshing the data..")
        if os.path.exists(data_directory):
            logger.debug(f"Directory {data_directory} exists, deleting..")
            shutil.rmtree(data_directory)
        if os.path.exists(itembuilds_directory):
            logger.debug(f"Directory {itembuilds_directory} exists, deleting..")
            shutil.rmtree(itembuilds_directory)
    os.makedirs(data_directory, exist_ok=True)
    logger.debug(f"Creating {data_directory} directory..")
    os.makedirs(itembuilds_directory, exist_ok=True)
    logger.debug(f"Creating {itembuilds_directory} directory..")

    if not os.path.exists(constants_heroes):
        logger.warning(
            f"{constants_heroes} doesn't exist! Creating {constants_heroes}.."
        )
        create_constant_heroes_csv()

    with open(constants_heroes) as heroes_csv:
        reader = csv.reader(heroes_csv)
        rows = list(reader)[1:]

    for i, row in enumerate(rows, start=1):
        if row[0] != "131" and f"{row[0]}.json" not in os.listdir(
            data_directory
        ):  # rubberpatch until there is data for ringmaster
            call_successful = 0
            logger.info(f"Doing API call {i}/{(len(rows)) - 1} {row[1]}")
            while not call_successful:
                try:
                    get_hero_popularity_guide(row[0])
                    call_successful = 1
                except:
                    logger.info(f"Waiting for API rate limit..")
                    time.sleep(15)
                    get_hero_popularity_guide(row[0])
                    call_successful = 1

    data__ids = [file.split(".")[0] for file in os.listdir(data_directory)]
    for i, id in enumerate(data__ids, start=1):
        # if id == "1.json":  # GuideFormatVersion 2 test
        #     compile_scrape_to_guide(id.split(".")[0], 1, 2)

        if id != data_file__hero_ids:
            logger.info(
                f"Compiling file {i}/{(len(data__ids))} {csv_match_string_for_relevant_column(constants_heroes,id,1)}"
            )
            compile_scrape_to_guide(id, remove_starting_items=remove_start_items)

    if os.path.exists(default_dota_itembuilds_windows_directory):
        build_amt = len(os.listdir(itembuilds_directory))
        for i, itembuild in enumerate(os.listdir(itembuilds_directory), start=1):
            logger.info(
                f"Moving file {i}/{build_amt} {csv_match_string_for_relevant_column(constants_heroes,itembuild[:-4],1)}"
            )
            shutil.copy(
                os.path.join(cwd, itembuilds_directory, itembuild),
                os.path.join(default_dota_itembuilds_windows_directory, itembuild),
            )
    else:
        logger.error(
            "Couldn't find steam installation path, manually replace itembuilds folder."
        )
