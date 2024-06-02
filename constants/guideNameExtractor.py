import os
import csv

# if a new hero breaks the opendota numbering, write a function to import data from `data\hero_ids.json`
# could've used https://dota2.fandom.com/wiki/Cheats#Hero_Names with just extracting the ` npc_dota_hero_`

csv_file_path = 'heroes.csv'
file_names = os.listdir("itembuilds")

hero_guide_list = []
for file_name in file_names:
    hero_guide_list.append(file_name[8:-4])

with open(csv_file_path, 'r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

for row, element in zip(data[1:], hero_guide_list):
    row.insert(2, element)

with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
