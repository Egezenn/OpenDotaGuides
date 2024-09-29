# OpenDotaGuides

<img alt="Windranger guide" style="padding-left:20px;" align="right" src="assets/image.png">

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?

Then you're in luck, this project uses what [OpenDota](https://www.opendota.com) has to offer in `opendota.com/heroes/<hero_id>/items` and aims to replace *pretty* outdated default guides in `..<dota_install_path>/game/dota/itembuilds`.

## How to install?

1. You can find the Dota2 installation path by going into `Steam` \> `Library` \> right click on `Dota 2` \> `Manage` \> `Browse Local Files`
2. Then go into `game` \> `dota`
3. Replace the `itembuilds` folder with
    1. the one from the [release](https://github.com/Egezenn/OpenDotaGuides/releases)
    2. the one you locally make. Refer to [here](#local-compilation).
4. Select the default guide in game
5. Have fun!

NOTE: If you've modified the contents of the folder while you were in Dota and in a match, disconnect & reconnect to see the changes.

## Local compilation

Assuming you already have [python](https://www.python.org/downloads/)(3.11), [node](https://nodejs.org/en/download/prebuilt-installer/current)(22.9) and [git](https://git-scm.com/downloads) installed:

1. `git clone https://github.com/Egezenn/OpenDotaGuides.git`
2. `cd OpenDotaGuides`
3. `python -m venv .venv`
4. Activate the python virtual environment:
   1. `.venv\Scripts\activate.bat`
   2. `source .venv/Scripts/activate`
5. `pip install -r requirements`
6. `nodeenv .nodeenv`
7. Activate the node virtual environment:
   1. `.nodeenv\Scripts\activate.bat`
   2. `source .nodeenv/Scripts/activate`
8. `npm install dotaconstants`
9. `python main.py`
10. If the steam installation isn't detected
    1. Remove `itembuilds` folder from dota2:
        1. `rmdir <dota_install_path>\dota 2 beta\game\dota\itembuilds`
        2. `rm -r <dota_install_path>/dota 2 beta/game/dota/itembuilds`
11. Move newly created guides:
    1. `move .\itembuilds <dota_install_path>\game\dota\itembuilds`
    2. `mv ./itembuilds <dota_install_path>/game/dota/itembuilds`

## TODO

- [ ] Get more information about the guide template
- [ ] Classify heroes as melee/ranged don't insert items that don't work or not work in full effect
  - Exceptions: Terrorblade, Troll Warlord, Vengeful Spirit
- [ ] Add item display names to `items.csv` and sort items based on it (looking at you, `angels_demise`)
- [ ] Create a function that automatically builds `constants/items.csv` using [dotaconstants](https://github.com/odota/dotaconstants) provided by OpenDota or by accessing vpk. Then inject flags from another csv
  - don't create any constants and just use `dotaconstants`?
  - or generate everything through it?

### DONE

- [x] Make use of the [OpenDota API](https://docs.opendota.com/) and change repo name, *again*
- [x] Assign variables to directories and files used throughout the project for easy management
- [x] Categorize items like pipe, crimson guard in `team` category (items that you manage who should be the carrier or just support items like solar crest, glimmer cape)
