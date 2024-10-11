import datetime
import json
import os

from .utils import (
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
categorized_items = ["team", "risky", "early"]


def compile_scrape_to_guide(hero_id, remove_starting_items=0, compiler_version=1):
    if remove_starting_items:
        removed_items.append("start")
    with open(f"{os.path.join(data_directory, hero_id)}.json") as f:
        hero_data = json.load(f)

    guide_name = search_csv(constants_heroes, hero_id)
    author = project_name
    v1_hero_name = f"npc_dota_hero_{guide_name}"
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
    early_category = []
    for stage in hero_stages:
        modified_hero_stage = []
        for item in stage:
            if checkFlags(constants_items, item) not in removed_items:
                if checkFlags(constants_items, item) in categorized_items:
                    if checkFlags(constants_items, item) == "team":
                        team_category.append(item)
                    elif checkFlags(constants_items, item) == "risky":
                        risky_category.append(item)
                    if checkFlags(constants_items, item) == "early":
                        if remove_starting_items:
                            early_category.append(item)
                        else:
                            modified_hero_stage.append(item)
                else:
                    modified_hero_stage.append(item)
        modified_hero_stage.sort()
        modified_hero_stages.append(modified_hero_stage)
    team_category.sort()
    risky_category.sort()
    early_category.sort()

    if compiler_version == 1:
        with open(
            os.path.join(itembuilds_directory, f"default_{guide_name}.txt"),
            "w",
            newline="",
        ) as file:
            file.write('"itembuilds"\n{\n')
            file.write(f'\t"Author"\t\t"{author}"\n')
            file.write(f'\t"Hero"\t\t\t"{v1_hero_name}"\n')
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
            file.write("}")

    elif compiler_version == 2:
        # test case
        with open(
            os.path.join(itembuilds_directory, f"default_{guide_name}.txt"),
            "w",
            newline="",
        ) as file:
            v2_hero_name = guide_name
            v2_role = "#DOTA_HeroGuide_Role_Core"
            v2_dota_version = "7.37c"

            file.write('"guidedata"\n{\n')
            file.write(f'\t"Hero"\t\t"{v2_hero_name}"\n')
            file.write(f'\t"Title"\t\t"{title}"\n')
            file.write(f'\t"Role"\t\t"{v2_role}"\n')
            file.write(f'\t"GameplayVersion"\t\t"{v2_dota_version}"\n')
            file.write('\t"Overview"\t\t"i20v0EPbB1iPsdMujTq06O5KC2GcKofs"\n')
            file.write('\t"GuideRevision"\t\t"8342"\n')
            file.write('\t"AssociatedWorkshopItemID"\t\t"0x0000000000000001"\n')
            file.write('\t"OriginalCreatorID"\t\t"0x0000000000000001"\n')
            file.write('\t"GuideFormatVersion"\t\t"2"\n')
            file.write('\t"TimeUpdated"\t\t"0x0000000000000001"\n')
            file.write('\t"TimePublished"\t\t"0x0000000000000001"\n')
            file.write('\t"ItemBuild"\n\t{\n')
            file.write('\t\t"Items"\n\t\t{\n')
            file.write('\t\t\t"#DOTA_Item_Build_Starting_Items"\n\t\t\t{\n')
            file.write('\t\t\t\t"item"\t\t"item_angels_demise"\n')
            file.write("\t\t\t}\n")
            file.write("\t\t}\n")
            file.write('\t\t"ItemTooltips"\n\t\t{\n')
            file.write('\t\t\t"item_angels_demise"\t\t"UYgGymhcQvUesFLc"\n')
            file.write("\t\t}\n")
            file.write("\t}\n")
            file.write('\t"AbilityBuild"\n\t{\n')
            file.write('\t\t"AbilityOrder"\n\t\t{\n')
            file.write('\t\t\t"1"\t\t"antimage_mana_break"\n')
            file.write('\t\t\t"2"\t\t"antimage_blink"\n')
            file.write('\t\t\t"3"\t\t"antimage_mana_break"\n')
            file.write('\t\t\t"4"\t\t"antimage_blink"\n')
            file.write('\t\t\t"5"\t\t"antimage_counterspell"\n')
            file.write('\t\t\t"6"\t\t"antimage_mana_void"\n')
            file.write('\t\t\t"7"\t\t"antimage_mana_break"\n')
            file.write('\t\t\t"8"\t\t"antimage_blink"\n')
            file.write('\t\t\t"9"\t\t"antimage_mana_break"\n')
            file.write('\t\t\t"10"\t\t"antimage_blink"\n')
            file.write('\t\t\t"11"\t\t"special_bonus_unique_antimage_4"\n')
            file.write('\t\t\t"12"\t\t"antimage_mana_void"\n')
            file.write("\t\t}\n")
            file.write('\t\t"AbilityTooltips"\n\t\t{\n')
            file.write('\t\t\t"antimage_mana_break"\t\t"dDLphB5MM1mo5wiI"\n')
            file.write("\t\t}\n")
            file.write("\t}\n")
            file.write("}\n")
