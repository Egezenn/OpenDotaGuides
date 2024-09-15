"heroes like abyssal_underlord need to be not injected in ascending order, this is just a WIP"

import csv
import os
import json


def build_heroes_csv():
    csv_file_path = r"constants/heroes.csv"
    try:
        file_names = os.listdir(
            r"C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/itembuilds/"
        )
    except FileNotFoundError:
        file_names = repr(input("Enter itembuilds path: "))

    hero_guide_list = []
    for file_name in file_names:
        hero_guide_list.append(file_name[8:-4])  # default_ <hero name> .txt

    with open("data/hero_ids.json", "r") as json_file:
        data = json.load(json_file)

    with open("constants/heroes.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["hero name", "hero id"])
        for key, value in data.items():
            csv_writer.writerow([key, value])

    with open(csv_file_path, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    # not worky properly
    for row, element in zip(
        data[1:], hero_guide_list
    ):  # ignore first line, do something i forgot
        row.insert(2, element)

    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
