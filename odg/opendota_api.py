import csv
import json
import os

import requests

from odg.utils import (
    constants_heroes,
    constants_items,
    csv_match_string_for_relevant_column,
    data_directory,
    export_flags,
    import_flags,
)

opendota_api_url = "https://api.opendota.com/api"


def get_hero_popularity_guide(hero_id: str):
    """Gets the item popularies for the specified hero id.

    Args:
        hero_id (str): Hero's id.
    """
    response = requests.get(f"{opendota_api_url}/heroes/{hero_id}/itemPopularity")
    guide = response.json()

    try:
        stages = {}
        for key, value in guide.items():
            stage = []
            for inner_keys in value.keys():
                stage.append(
                    csv_match_string_for_relevant_column(constants_items, inner_keys, 2)
                )
            stages[key] = stage

        with open(os.path.join(data_directory, f"{hero_id}.json"), "w") as json_file:
            json.dump(stages, json_file, indent=2)

    except AttributeError:  # if response is not a json?
        get_hero_popularity_guide(hero_id)


def create_constant_heroes_csv():
    """Creates hero constants csv file in `constants` directory."""
    response = requests.get(f"{opendota_api_url}/heroes")
    heroes = response.json()
    headers = ["id", "localized_name", "name", "guide_name", "attack_type"]
    hero_attr_lists = []
    for hero in heroes:
        hero_attr_list = [
            hero["id"],
            hero["localized_name"],
            hero["name"],
            f"default_{hero['name'][14:]}",
            hero["attack_type"],
        ]
        hero_attr_lists.append(hero_attr_list)

    with open(constants_heroes, "w", newline="") as heroes_file:
        writer = csv.writer(heroes_file)
        writer.writerow(headers)
        for hero in hero_attr_lists:
            if hero[1] in ["Terrorblade", "Troll Warlord", "Vengeful Spirit"]:
                hero_attrs_mixed = hero[:-1]
                hero_attrs_mixed.append("Mixed")
                writer.writerow(hero_attrs_mixed)
            else:
                writer.writerow(hero[:])


def create_constant_items_csv():
    """Creates item constants csv file in `constants` directory and automatically exports & imports the flag metadata."""
    if os.path.exists(constants_items):
        export_flags()
    response = requests.get(f"{opendota_api_url}/constants/items")
    items = response.json()
    headers = ["id", "dname", "guide_name", "item_name", "flag"]
    item_attr_lists = []
    for item, item_attrs in items.items():
        if "dname" in item_attrs:
            # to not trigger an exception for
            # items that are legacy or test items that are
            # forgotten and still in the dota for some reason
            item_attr_list = [
                item_attrs["id"],
                item_attrs["dname"],
                f"item_{item}",
                item,
                "",
            ]
            item_attr_lists.append(item_attr_list)
    item_attr_lists = sorted(item_attr_lists, key=lambda x: x[0])

    with open(constants_items, "w", newline="") as items_csv:
        writer = csv.writer(items_csv)
        writer.writerow(headers)
        writer.writerows(item_attr_lists)

    import_flags()
