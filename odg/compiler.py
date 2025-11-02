import datetime
import json
import os

import utils

removed_items = ["component", "consumable", "ignore"]
categorized_items = ["early", "risky", "team"]


def compile_scrape_to_guide_vdf(hero_id: str, remove_starting_items=0):
    """Compiles a json file in `data` directory into the Valve Data File (VDF) format in `itembuilds` directory.

    Args:
        hero_id (str): Hero's id.
        remove_starting_items (int, optional): Removes `starting items` category & injects impactful progression items into `early game` category. Defaults to 0.
    """
    if remove_starting_items:
        removed_items.append("start")
    with open(f"{os.path.join(utils.data_directory, hero_id)}.json") as f:
        hero_data = json.load(f)

    localized_name = utils.csv_match_string_for_relevant_column(utils.constants_heroes, hero_id, 1)
    name = utils.csv_match_string_for_relevant_column(utils.constants_heroes, hero_id, 2)
    guide_name = utils.csv_match_string_for_relevant_column(utils.constants_heroes, hero_id, 3)
    author = utils.project_name
    title = f"{utils.project_name_shorthand} {localized_name} {datetime.date.today().isoformat()}"
    hero_stages = []
    for stage in hero_data:
        hero_stage = []
        for item in hero_data[stage]:
            hero_stage.append(item)
        hero_stages.append(hero_stage)

    hero_stages = utils.remove_repeated_elements(hero_stages)
    modified_hero_stages = []
    team_category = []
    risky_category = []
    early_category = []
    for stage in hero_stages:
        modified_hero_stage = []
        for item in stage:
            if utils.csv_match_string_for_relevant_column(utils.constants_items, item, 4) not in removed_items:
                if utils.csv_match_string_for_relevant_column(utils.constants_items, item, 4) in categorized_items:
                    if utils.csv_match_string_for_relevant_column(utils.constants_items, item, 4) == "team":
                        team_category.append(item)
                    elif utils.csv_match_string_for_relevant_column(utils.constants_items, item, 4) == "risky":
                        risky_category.append(item)
                    # append to early if starting items are removed
                    if utils.csv_match_string_for_relevant_column(utils.constants_items, item, 4) == "early":
                        if remove_starting_items:
                            early_category.append(item)
                        else:
                            modified_hero_stage.append(item)
                else:
                    modified_hero_stage.append(item)
        modified_hero_stage = sorted(
            modified_hero_stage,
            key=lambda item: utils.csv_match_string_for_relevant_column(utils.constants_items, item, 1) or item,
        )
        modified_hero_stages.append(modified_hero_stage)
    team_category = sorted(
        team_category,
        key=lambda item: utils.csv_match_string_for_relevant_column(utils.constants_items, item, 1) or item,
    )
    risky_category = sorted(
        risky_category,
        key=lambda item: utils.csv_match_string_for_relevant_column(utils.constants_items, item, 1) or item,
    )
    early_category = sorted(
        early_category,
        key=lambda item: utils.csv_match_string_for_relevant_column(utils.constants_items, item, 1) or item,
    )

    with open(os.path.join(utils.itembuilds_directory, f"{guide_name}.txt"), "w", newline="") as file:
        file.write('"itembuilds"\n{\n')
        file.write(f'\t"Author"\t\t"{author}"\n')
        file.write(f'\t"Hero"\t\t\t"{name}"\n')
        file.write(f'\t"Title"\t\t\t"{title}"\n')
        file.write('\n\t"Items"\n\t{\n')
        if modified_hero_stages[0] != []:
            file.write('\t\t"#DOTA_Item_Build_Starting_Items"\n\t\t{\n')
            for item in modified_hero_stages[0]:
                file.write(f'\t\t\t"item"\t\t"{item}"\n')
            file.write("\t\t}\n")
        file.write('\t\t"#DOTA_Item_Build_Early_Game"\n\t\t{\n')
        for item in early_category:
            file.write(f'\t\t\t"item"\t\t"{item}"\n')
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
        file.write("}\n")
