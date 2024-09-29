import datetime
import json
import os

from utils import (
    checkFlags,
    constants_heroes,
    constants_items,
    data_directory,
    itembuilds_directory,
    project_name_shorthand,
    project_name,
    remove_repeated_elements,
    search_csv,
)

removed_items = ["ignore", "component"]
categorized_items = ["team", "risky"]


def compile_scrape_to_guide(hero_id, remove_starting_items=0):
    if remove_starting_items:
        removed_items.append("start")
    with open(f"{os.path.join(data_directory, hero_id)}.json") as f:
        hero_data = json.load(f)

    guide_name = search_csv(constants_heroes, hero_id)
    author = project_name
    hero = f"npc_dota_hero_{guide_name}"
    title = f"{project_name_shorthand} {datetime.date.today().isoformat()}"
    hero_stages = []
    for stage in hero_data:
        hero_stage = []
        for item in hero_data[stage]:
            hero_stage.append(f"item_{item}")
        hero_stages.append(hero_stage)

    hero_stages = remove_repeated_elements(hero_stages)
    modified_hero_stages = []
    team_category = []
    risky_category = []
    for stage in hero_stages:
        modified_hero_stage = []
        for item in stage:
            if checkFlags(constants_items, item) not in removed_items:
                if checkFlags(constants_items, item) in categorized_items:
                    if checkFlags(constants_items, item) == "team":
                        team_category.append(item)
                    if checkFlags(constants_items, item) == "risky":
                        risky_category.append(item)
                else:
                    modified_hero_stage.append(item)
        modified_hero_stage.sort()
        modified_hero_stages.append(modified_hero_stage)
    team_category.sort()
    risky_category.sort()

    with open(
        os.path.join(itembuilds_directory, f"default_{guide_name}.txt"), "w", newline=""
    ) as file:
        file.write('"itembuilds"\n{\n')
        file.write(f'\t"author"\t\t"{author}"\n')
        file.write(f'\t"hero"\t\t\t"{hero}"\n')
        file.write(f'\t"Title"\t\t\t"{title}"\n')
        file.write('\n\t"Items"\n\t{\n')
        if modified_hero_stages[0] != []:
            file.write('\t\t"#DOTA_Item_Build_Starting_Items"\n\t\t{\n')
            for item in modified_hero_stages[0]:
                file.write(f'\t\t\t"item"\t\t"{item}"\n')
            file.write("\t\t}\n")
        file.write('\t\t"#DOTA_Item_Build_Early_Game"\n\t\t{\n')
        for item in modified_hero_stages[1]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write("\t\t}\n")
        file.write('\t\t"#DOTA_Item_Build_Mid_Items"\n\t\t{\n')
        for item in modified_hero_stages[2]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write("\t\t}\n")
        file.write('\t\t"#DOTA_Item_Build_Late_Items"\n\t\t{\n')
        for item in modified_hero_stages[3]:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
        file.write("\t\t}\n")
        if team_category != []:
            file.write('\t\t"TEAM UTILITIES"\n\t\t{\n')
            for item in team_category:
                file.write(f'\t\t\t"item"\t\t"{item}"\n')
            file.write("\t\t}\n")
        if risky_category != []:
            file.write('\t\t"RISKY"\n\t\t{\n')
            for item in risky_category:
                file.write(f'\t\t\t"item"\t\t"{item}"\n')
            file.write("\t\t}\n")
        file.write("\t}\n")
        file.write("}")
