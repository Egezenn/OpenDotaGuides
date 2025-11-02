import os
import tempfile
import shutil
import urllib.request

temp_dir = tempfile.gettempdir()
base_path = os.path.join(temp_dir, "ODG")
zip_path = os.path.join(base_path, "OpenDotaGuides.zip")
temp_dump_path = os.path.join(base_path, "temp")
most_likely_path = os.path.join(
    "C:\\", "Program Files (x86)", "Steam", "steamapps", "common", "dota 2 beta", "game", "dota", "itembuilds"
)

os.makedirs(base_path, exist_ok=True)
if not os.path.exists(os.path.join(most_likely_path, "default_antimage.txt")):
    try:
        with open("itembuilddir.txt") as file:
            itembuilds_dir = os.path.normpath(file.readline())
    except:
        itembuilds_dir_input = input("Write your itembuild dir:\n")
        itembuils_dir = itembuilds_dir_input
        with open("itembuilddir.txt", "w") as file:
            file.write(itembuilds_dir_input)
else:
    itembuilds_dir = most_likely_path
    print("Itembuild dir detected")

try:
    urllib.request.urlretrieve(
        "https://github.com/Egezenn/OpenDotaGuides/releases/latest/download/itembuilds.zip", zip_path
    )
    shutil.unpack_archive(zip_path, temp_dump_path, "zip")
    os.makedirs(os.path.join(itembuilds_dir, "bkup"), exist_ok=True)
    for name in os.listdir(itembuilds_dir):
        try:
            if name != "bkup":
                os.rename(os.path.join(itembuilds_dir, name), os.path.join(itembuilds_dir, "bkup", name))
        except:
            pass
    for file in os.listdir(temp_dump_path):
        shutil.copy(os.path.join(temp_dump_path, file), os.path.join(itembuilds_dir, file))
    shutil.rmtree(base_path)

except:
    pass
