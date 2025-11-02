import csv
import json
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

constants_directory = os.path.join(project_root, "constants")
constants_file__flags = "flags.json"
constants_file__heroes = "heroes.csv"
constants_file__items = "items.csv"
data_directory = os.path.join(project_root, "data")
itembuilds_directory = os.path.join(project_root, "itembuilds")
logfile = os.path.join(project_root, "odg.log")
project_name = "OpenDotaGuides"
project_name_shorthand = "ODG"

constants_flags = os.path.join(constants_directory, constants_file__flags)
constants_heroes = os.path.join(constants_directory, constants_file__heroes)
constants_items = os.path.join(constants_directory, constants_file__items)
default_dota_installation_windows_directory = os.path.join(
    "C:\\", "Program Files (x86)", "Steam", "steamapps", "common", "dota 2 beta"
)
default_dota_itembuilds_windows_directory = os.path.join(
    default_dota_installation_windows_directory, "game", "dota", "itembuilds"
)


def csv_match_string_for_relevant_column(file_path: str, search_string: str, x: int) -> str:
    """Searches a csv file for a matching string in every row, returns the desired column in that row.

    Args:
        file_path (str): File path.
        search_string (str): String used to get the desired row.
        x (int): Desired column.

    Returns:
        str: _description_
    """
    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            for column in row:
                if column == search_string:
                    return row[x]


def remove_repeated_elements(input_list: list) -> list:
    """Removes duplicate elements in a nested list.

    Args:
        input_list (list): nested list.

    Returns:
        list: Returns the modified list.
    """
    seen = set()
    result = []

    for lst in input_list:
        new_lst = [element for element in lst if element not in seen]
        seen.update(new_lst)
        result.append(new_lst)

    return result


def export_flags():
    """Exports the flags in `items.csv.`"""
    with open(constants_items) as items_csv:
        reader = csv.reader(items_csv)

        item_flags = {}
        for row in reader:
            if [row[3], row[4]] != ["item_name", "flag"]:
                if row[4] != "":
                    item_flags[row[3]] = row[4]

    with open(constants_flags, "w") as flags_json:
        json.dump(item_flags, flags_json, indent=2)


def import_flags():
    """Imports the flags in `flags.json`."""
    with open(constants_items, "r+") as items_csv:
        reader = csv.reader(items_csv)
        writer = csv.writer(items_csv)
        rows = list(reader)

        with open(constants_flags) as flags_json:
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
