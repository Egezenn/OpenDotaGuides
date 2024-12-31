import os
import tempfile
import shutil
import urllib.request

temp_dir = tempfile.gettempdir()
base_path = os.path.join(temp_dir, "ODG")
zip_path = os.path.join(base_path, "OpenDotaGuides.zip")
temp_dump_path = os.path.join(base_path, "temp")


os.makedirs(base_path, exist_ok=True)

try:
    with open("itembuilddir.txt", "r") as file:
        itembuilds_dir = os.path.normpath(file.readline())
except:
    itembuilds_dir_input = input("Write your itembuild dir:\n")
    with open("itembuilddir.txt", "w") as file:
        file.write(itembuilds_dir_input)


urllib.request.urlretrieve(
    "https://github.com/Egezenn/OpenDotaGuides/releases/latest/download/itembuilds.zip",
    zip_path,
)
shutil.unpack_archive(zip_path, temp_dump_path, "zip")
for file in os.listdir(temp_dump_path):
    shutil.copy(
        os.path.join(temp_dump_path, file),
        os.path.join(itembuilds_dir, file),
    )
shutil.rmtree(base_path)
