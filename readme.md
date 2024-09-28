# ScrapedDotaGuides

<img alt="Windranger guide" style="padding-left:20px;" align="right" src="assets/image.png">

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?

Then you're in luck, this project scrapes what [OpenDota](https://www.opendota.com) has to offer in `opendota.com/heroes/<hero_id>/items` and aims to replace *pretty* outdated default guides in `..<steam_folder_or_library_path>/dota 2 beta/game/dota/itembuilds`.

## How to use?

1. Replace the `itembuilds` folder with
    1. the one from the [release](https://github.com/Egezenn/ScrapedDotaGuides/releases)
    2. the one you locally make. Refer to [here](#local-compilation).
2. Select the default guide in game
3. Have fun!

NOTE: If you've modified the contents folder while you were in Dota and in a match, disconnect & reconnect to see the changes.

## Local compilation

Assuming you already have python (I'm currently using python3.11, change version if needed) and git installed:

1. `git clone https://github.com/Egezenn/ScrapedDotaGuides.git`
2. `cd ScrapedDotaGuides`
3. `python -m venv .venv`
4. Activate the virtual environment:
   1. 1 `.venv\Scripts\activate.bat`
   2. 2 `source .venv/Scripts/activate`
5. `pip install -r requirements`
6. `python main.py`
7. If the steam installation isn't detected
    1. Remove `itembuilds` folder from dota2:
        1. `rmdir <steam_folder_or_library_path>\dota 2 beta\game\dota\itembuilds`
        2. `rm -r <steam_folder_or_library_path>/dota 2 beta/game/dota/itembuilds`
8. 8 Move newly created guides:
   1. `move .\itembuilds <steam_folder_or_library_path>\steamapps\common\dota 2 beta\game\dota\itembuilds`
   2. `mv ./itembuilds <steam_folder_or_library_path>\steamapps\common/dota 2 beta/game/dota/itembuilds`

## TODO

- [x] Assign variables to directories and files used throughout the project for easy management
- [ ] Make use of the [OpenDota API](https://docs.opendota.com/) and change repo name, *again*
- [ ] Get more information about the guide template
- [ ] Classify heroes as melee/ranged don't insert items that don't work or not work in full effect
  - Exceptions: Terrorblade, Troll Warlord, Vengeful Spirit
- [ ] Add item display names to `items.csv` and sort items based on it (looking at you, `angels_demise`)
- [x] Categorize items like pipe, crimson guard in `team` category (items that you manage who should be the carrier or just support items like solar crest, glimmer cape)
- [ ] Create a function that automatically builds `constants/items.csv` using [dotaconstants](https://github.com/odota/dotaconstants) provided by OpenDota or by accessing vpk. Then inject flags from another csv
