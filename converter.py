import json
import csv
import datetime


def search_csv(file_path, search_string):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and row[1] == search_string:
                return row[2]


def convert_scrape_to_guide(hero_id):
    with open(f"data\\{hero_id}.json") as f:
        hero_data = json.load(f)

    guide_name = search_csv("constants\\heroes.csv", hero_id)
    author = "OpenDotaGuides"
    hero = f"npc_dota_hero_{guide_name}"
    title = f"ODG {datetime.date.today().isoformat()}"
    hero_stages = []
    for stage in hero_data:
        hero_stage = []
        for item in hero_data[stage]:
            hero_stage.append(f"item_{item}")
        hero_stages.append(hero_stage)

    with open(f"itembuilds\\default_{guide_name}.txt", 'w', newline='') as file:
        file.write('"itembuilds"\n{\n')
        file.write(f'\t"author"\t\t"{author}"\n')
        file.write(f'\t"hero"\t\t\t"{hero}"\n')
        file.write(f'\t"Title"\t\t\t"{title}"\n')
        file.write('\n\t"Items"\n\t{\n')
        file.write('\t\t"#DOTA_Item_Build_Starting_Items"\t\t\n\t\t{\n')
        for item in hero_stages[0]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write('\t\t}\n')
        file.write('\t\t"#DOTA_Item_Build_Early_Game"\t\t\n\t\t{\n')
        for item in hero_stages[1]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write('\t\t}\n')
        file.write('\t\t"#DOTA_Item_Build_Mid_Items"\t\t\n\t\t{\n')
        for item in hero_stages[2]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write('\t\t}\n')
        file.write('\t\t"#DOTA_Item_Build_Late_Items"\t\t\n\t\t{\n')
        for item in hero_stages[3]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write('\t\t}\n')
        file.write('\t}\n')
        file.write('}')
