import csv
import json
import os

cwd = os.getcwd()
constants_directory = r"constants"
constants_file__flags = r"flags.json"
constants_file__heroes = r"heroes.csv"
constants_file__items = r"items.csv"
data_directory = r"data"
data_file__hero_ids = r"hero_ids.json"
itembuilds_directory = r"itembuilds"
logfile = r"odg.log"
project_name = r"OpenDotaGuides"
project_name_shorthand = r"ODG"

constants_flags = os.path.join(constants_directory, constants_file__flags)
constants_heroes = os.path.join(constants_directory, constants_file__heroes)
constants_items = os.path.join(constants_directory, constants_file__items)
data_hero_ids = os.path.join(data_directory, data_file__hero_ids)
default_dota_installation_windows_directory = os.path.join(
    "C:\\",
    r"Program Files (x86)",
    r"Steam",
    r"steamapps",
    r"common",
    r"dota 2 beta",
)
default_dota_itembuilds_windows_directory = os.path.join(
    default_dota_installation_windows_directory,
    r"game",
    r"dota",
    r"itembuilds",
)


def csv_match_string_for_relevant_column(
    file_path: str, search_string: str, x: int
) -> str:
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            for column in row:
                if column == search_string:
                    return row[x]


def remove_repeated_elements(input_list: list):
    seen = set()
    result = []

    for lst in input_list:
        new_lst = [element for element in lst if element not in seen]
        seen.update(new_lst)
        result.append(new_lst)

    return result


def export_flags():
    with open(constants_items, "r") as items_csv:
        reader = csv.reader(items_csv)

        item_flags = {}
        for row in reader:
            if [row[3], row[4]] != ["item_name", "flag"]:
                if row[4] != "":
                    item_flags[row[3]] = row[4]

    with open(constants_flags, "w") as flags_csv:
        json.dump(item_flags, flags_csv, indent=2)


def import_flags():
    with open(constants_items, "r+") as items_csv:
        reader = csv.reader(items_csv)
        writer = csv.writer(items_csv)
        rows = list(reader)

        with open(constants_flags, "r") as flags_json:
            data = json.load(flags_json)

        for row in rows:
            if row[3] != "item_name":
                key_to_match = row[3]

                if key_to_match in data:
                    row[4] = data[key_to_match]
                else:
                    row[4] = ""
                    # if there is a new item, there isn't going
                    # to be any data for itso insert nothing
        with open(constants_items, "w", newline="") as items_csv:
            writer = csv.writer(items_csv)
            writer.writerows(rows)
