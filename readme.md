# ScrapedDotaGuides

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?

Then you're in luck, this project scrapes what [OpenDota](https://www.opendota.com) has to offer in `opendota.com/heroes/<hero_id>/items` and aims to replace *pretty* outdated default guides in `..<steam_folder_or_library_path>/dota 2 beta/game/dota/itembuilds`.

How to use?

1. Replace the `itembuilds` folder with
    1. the one from the release
    2. the one you locally make. Refer to [here](#local-installation).
2. Select the default guide in game
3. Have fun!

Example screenie of a windranger guide:

![example](image.png)

## Local installation

Assuming you already have python and git installed:

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

- [ ] Cache page data via selenium if possible
- [ ] Create a function that automatically builds `constants/items.csv` by accessing vpk and inject flags from another csv
