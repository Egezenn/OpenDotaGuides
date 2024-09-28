import os
import csv

constants_directory = r"constants"
constants_file__heroes = r"heroes.csv"
constants_file__items = r"items.csv"
data_directory = r"data"
data_file__hero_ids = r"hero_ids.json"
itembuilds_directory = r"itembuilds"
project_name = r"ScrapedDotaGuides"
project_name_shorthand = r"SDG"
cwd = os.getcwd()

constants_heroes = os.path.join(constants_directory, constants_file__heroes)
constants_items = os.path.join(constants_directory, constants_file__items)
data_hero_ids = os.path.join(data_directory, data_file__hero_ids)
default_dota_installation_windows_directory = os.path.join(
    "C:\\",
    r"Program Files (x86)",
    r"Steam",
    r"steamapps",
    r"common",
)
default_dota_itembuilds_windows_directory = os.path.join(
    default_dota_installation_windows_directory,
    r"dota 2 beta",
    r"game",
    r"dota",
    r"itembuilds",
)


def search_csv(file_path, search_string):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and row[1] == search_string:
                return row[2]


def checkFlags(file_path, search_string):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3 and row[0] == search_string:
                return row[2]


def remove_repeated_elements(input_list):
    seen = set()
    result = []

    for lst in input_list:
        new_lst = [element for element in lst if element not in seen]
        seen.update(new_lst)
        result.append(new_lst)

    return result