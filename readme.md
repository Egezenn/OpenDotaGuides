# OpenDotaGuides

<img alt="Windranger guide" style="padding-left:20px;" align="right" src="assets/image.png">

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?

Then you're in luck, this project uses what [OpenDota](https://www.opendota.com) has to offer in in their [API](https://docs.opendota.com) and replaces *pretty* outdated and useless default guides in `..<dota_install_path>/game/dota/itembuilds`.

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

Assuming you already have [python](https://www.python.org/downloads/)(~=3.13) and [git](https://git-scm.com/downloads) installed:  
First instruction set is for Windows, second is for Linux.

1. `git clone https://github.com/Egezenn/OpenDotaGuides.git`
2. `cd OpenDotaGuides`
3. `python -m venv .venv`
4. Activate the python virtual environment:
   1. `.venv\Scripts\activate.bat`
   2. `source .venv/Scripts/activate`
5. `pip install -r requirements.txt`
6. `python -m odg` `-v -r -c -s` `-h`
7. If the dota installation isn't detected
    1. Remove `itembuilds` folder from Dota2:
        1. `rmdir <dota_install_path>\dota 2 beta\game\dota\itembuilds`
        2. `rm -r <dota_install_path>/dota 2 beta/game/dota/itembuilds`
    2. Move newly created guides:
        1. `move .\itembuilds <dota_install_path>\game\dota\itembuilds`
        2. `mv ./itembuilds <dota_install_path>/game/dota/itembuilds`

## TODO

- [x] Use `logging` library for debug printouts
  - [ ] Didn't have time to check how to persist the logger's config throughout the submodules
  - [x] Make them print out the same thing
    - task_name \<current_task\>/\<amount_of_tasks\> \<hero_name\>
- [x] Package the repo
  - [ ] Publish to PyPI
    - Learn about proper packaging
- [ ] Add item display names and ids to `items.csv` and sort items based on it (looking at you, `angels_demise`)
- [ ] Classify heroes as melee/ranged don't insert items that don't work or not work in full effect
  - [x] Exceptions: Terrorblade, Troll Warlord, Vengeful Spirit
- [ ] Make the project an executable
- [ ] Add ability guides and also maybe mayyyyyyyyyyyyybe add item tooltips
  - Workshop guide format doesn't work. see [example](constants/default_antimage.txt)
    - Might have something to do with GuideFormatVersion

### DONE

- [x] Make CLI
  - [x] Add optionals/customizations
- [x] Classify the args required for functions
- [x] Remove npm, nodeenv and dotaconstants dependencies, the data is available on OpenDota API. Adjust compilation steps.
  - GET /heroes
  - GET /constants/{resource}
- [x] Create a function that builds `constants/items.csv`. Then inject flag metadata from another json
- [x] Create a function that builds `heroes.csv`
- [x] for the complete removal of starting items category, would need to add items like basilius, bracer, orb of venom, blight stone etc
- [x] Add an option to reduce or remove starting items category. I think that you should be using the normal shop panel for them anyway.
  - 500- gold, not a component and items not like soul booster and perseverance which you only buy it for the build up of items (like no one buying a buckler but basilius for the early mana regen)
- [x] Make use of the [OpenDota API](https://docs.opendota.com/) and change repo name, *again*
- [x] Assign variables to directories and files used throughout the project for easy management
- [x] Categorize items like pipe, crimson guard in `team` category (items that you manage who should be the carrier or just support items like solar crest, glimmer cape)
