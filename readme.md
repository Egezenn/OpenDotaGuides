# OpenDotaGuides

<img alt="Windranger guide" style="padding-left:20px;" align="right" src="assets/image.png">

Tired of streamlined, opinionated and slowly updating guides? Want to see many item recommendations from the pros for the newest patch?

Then you're in luck, this project uses what [OpenDota](https://www.opendota.com) has to offer in in their [API](https://docs.opendota.com) and replaces *pretty* outdated and useless default guides in `..<dota_install_path>/game/dota/itembuilds`.

## How to install?

1. You can find the Dota2 installation path by going into `Steam` \> `Library` \> right click on `Dota 2` \> `Manage` \> `Browse Local Files`
2. Then go into `game` \> `dota`
3. Replace the `itembuilds` folder with
    1. the one from the [release](https://github.com/Egezenn/OpenDotaGuides/releases/latest)
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

- [ ] Add item display names and ids to `items.csv` and sort items based on it (looking at you, `angels_demise`)

- [ ] Add ability guides, facets and also maybe mayyyyyyyyyyyyybe add item tooltips
  - Workshop guide's attributes doesn't work on the default itembuilds. See [example](constants/default_antimage.txt).
    - Might have something to do with GuideFormatVersion
      - Can publish the guides to Dota2 and fetch the data from there as it uses the new format
        - Could automate this with a new project to overwrite userdata & dota2 files
  - There doesn't seem to be anything regarding ability paths and facets in OpenDota API, research for a provider?

- [x] Package the repo
  - [ ] Publish to PyPI
    - Learn about proper packaging

- [x] Use `logging` library for debug printouts
  - [ ] Didn't have time to check how to persist the logger's config throughout the submodules
    - [ ] Move warnings back to the submodules
  - [x] Make them print out the same thing
    - task_name \<current_task\>/\<amount_of_tasks\> \<hero_name\>

- [ ] Classify heroes as melee/ranged and don't insert items that don't work or not work in full effect
  - [x] Exceptions: Terrorblade, Troll Warlord, Vengeful Spirit
  - [ ] Expand `items.csv` to for the metadata that is required
    - There doesn't seem to be an attribute in OpenDota's `dotaconstants` which directly tells whether item works or not on the attack type
      - In the `description` of `abilities` of the item
        - Unreliably check for ranged or melee in description?
      - On `attrib`'s entries the `display` data has information such as `(Melee|Ranged Only)`
        - Not all of them have it e.g: Echo Sabre, Harpoon
      - There also isn't a doesn't work in full effect attribute

    - [ ] Add metadata manually
      - Melee
        - Battlefury
        - Echo Sabre
        - Harpoon
      - Ranged
        - Dragon's Lance (i mean, for the longest of time Meepo actually bought this for its stats)
        - Hurricane Pike
      - Doesn't work in full effect aka Ranged penalties
        - Not going to add stuff like Witch Blade's passive benefiting from intelligence attribute or neutral items
          - Could be added to the item descriptions but then the guide format already doesn't work and you can just read the item's description
          - The point of this attribute is to not add them to the guide at all
        - Quelling Blade (can be an exclusion)
        - Orb of Venom
        - Phase Boots (can be an exclusion)
        - Power Treads (can be an exclusion)
        - Basher
        - Abyssal Blade

  - Scrap the idea, pros wouldn't buy Echo Sabre on a ranged hero, *right*?
    - Also there are many exclusions which kinda makes this irrelevant
    - Remove attack type on `heroes.csv`

- [ ] The god awful KeyValue format that's used in itembuilds is an actual file format and named Valve Data File (VDF) and used throughout Valve. I transformed- further transformed into a caveman just by knowing this.
  - [ ] Implement the format properly with a serialization library
    - or.. not?
    - [vdf](https://pypi.org/project/vdf/)
    - [python-valve](https://pypi.org/project/python-valve/)
  - Why aren't they just using JSON to this day? :D
  - Source of the "oh shit this is an actual file format" moment: [Primeagen's reaction](https://www.youtube.com/watch?v=Mzm4d0qyK00), [source](https://www.youtube.com/watch?v=ShsoED-goDg)
