import os
import requests
import json

from utils import dotaconstants_item_ids, data_directory


def get_hero_popularity_guide(hero_id):
    opendota_api_url = "https://api.opendota.com/api"
    response = requests.get(f"{opendota_api_url}/heroes/{hero_id}/itemPopularity")
    response_json = response.json()

    with open(dotaconstants_item_ids, "r") as file:
        data = json.load(file)

    stages = {}
    for key, value in response_json.items():
        stage = []
        for inner_keys in value.keys():
            stage.append(data.get(inner_keys))
        stages[key] = stage

    with open(os.path.join(data_directory, f"{hero_id}.json"), "w") as json_file:
        json.dump(stages, json_file, indent=2)
