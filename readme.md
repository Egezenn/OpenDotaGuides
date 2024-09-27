# ScrapedDotaGuides

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?  
Then you're in luck, this project scrapes what [OpenDota](https://www.opendota.com) has to offer in `opendota.com/heroes/<hero_id>/items` and aims to replace *pretty* outdated default guides in `../dota 2 beta/game/dota/itembuilds`.

How to use?

1. Replace the `itembuilds` folder with
   1. the one from the release
   2. the one you locally make. Instructions for it are:
      1. `git clone https://github.com/Egezenn/ScrapedDotaGuides.git`
      2. `cd ScrapedDotaGuides`
      3. `python -m venv .venv`
      4. Depending on your OS:
         - `.venv\Scripts\activate.bat`
         - `source .venv/Scripts/activate`
      5. `pip install -r requirements`
      6. `python main.py`
      7. If the steam installation isn't detected
         1. Remove `itembuilds` folder from dota2:
            - `rmdir <steam_folder_path>\dota 2 beta\game\dota\itembuilds`
            - `rm -r <steam_folder_path>/dota 2 beta/game/dota/itembuilds`
         2. Move newly created guides:
            - `move .\itembuilds <steam_folder_path>\dota 2 beta\game\dota\itembuilds`
            - `mv ./itembuilds <steam_folder_path>/dota 2 beta/game/dota/itembuilds`
2. Select the default guide in game
3. Have fun!

TODO:

- [ ] Cache page data via selenium if possible
- [ ] Create a function that automatically builds `constants/items.csv` by accessing vpk and inject flags from another csv
