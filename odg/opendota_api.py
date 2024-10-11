import csv
import json
import os

import requests

from .utils import (
    constants_heroes,
    constants_items,
    data_directory,
    export_flags,
    import_flags,
    search_csv_match_y_for_x,
)

opendota_api_url = "https://api.opendota.com/api"


def get_hero_popularity_guide(hero_id: str):
    response = requests.get(f"{opendota_api_url}/heroes/{hero_id}/itemPopularity")
    guide = response.json()

    try:
        stages = {}
        for key, value in guide.items():
            stage = []
            for inner_keys in value.keys():
                stage.append(
                    search_csv_match_y_for_x(constants_items, inner_keys, 0, 2)
                )
            stages[key] = stage

        with open(os.path.join(data_directory, f"{hero_id}.json"), "w") as json_file:
            json.dump(stages, json_file, indent=2)

    except AttributeError:  # if response is not a json?
        get_hero_popularity_guide(hero_id)


def create_constant_heroes_csv():
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
                (
                    id,
                    localized_name,
                    name,
                    guide_name,
                ) = hero[:-1]
                writer.writerow([id, localized_name, name, guide_name, "Mixed"])
            else:
                writer.writerow(hero[:])


def create_constant_items_csv():
    if os.path.exists(constants_items):
        export_flags()
    response = requests.get(f"{opendota_api_url}/constants/items")
    items = response.json()
    headers = ["id", "dname", "guide_name", "item_name", "flag"]
    item_attr_lists = []
    for item, item_attrs in items.items():
        if "dname" in item_attrs:
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
