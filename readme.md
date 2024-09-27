# ScrapedDotaGuides

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?  
Then you're in luck, this project scrapes what [OpenDota](https://www.opendota.com) has to offer in `opendota.com/heroes/<hero_id>/items` and aims to replace *pretty* outdated default guides in `../dota 2 beta/game/dota/itembuilds`.

How to use?

Replace the `itembuilds` folder with  
1 the one from the release  
2 the one you locally make. Instructions for it are:  
2⟩1 `git clone https://github.com/Egezenn/ScrapedDotaGuides.git`  
2⟩2 `cd ScrapedDotaGuides`  
2⟩3 `python -m venv .venv`  
2⟩4 Depending on your OS:  
2⟩4⟩1 `.venv\Scripts\activate.bat`  
2⟩4⟩2 `source .venv/Scripts/activate`  
2⟩5 `pip install -r requirements`  
2⟩6 `python main.py`  
2⟩7 If the steam installation isn't detected  
2⟩7⟩1 Remove `itembuilds` folder from dota2:  
2⟩7⟩1⟩1 `rmdir <steam_folder_path>\dota 2 beta\game\dota\itembuilds`  
2⟩7⟩1⟩2 `rm -r <steam_folder_path>/dota 2 beta/game/dota/itembuilds`  
2⟩7⟩2 Move newly created guides:  
2⟩7⟩2⟩1 `move .\itembuilds <steam_folder_path>\dota 2 beta\game\dota\itembuilds`  
2⟩7⟩2⟩2 `mv ./itembuilds <steam_folder_path>/dota 2 beta/game/dota/itembuilds`  
Select the default guide in game  
Have fun!

TODO:

- [ ] Cache page data via selenium if possible
- [ ] Create a function that automatically builds `constants/items.csv` by accessing vpk and inject flags from another csv
