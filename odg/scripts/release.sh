# python -m venv .venv
# source .venv/Scripts/activate
# python -m pip install --upgrade pip
# pip install -r requirements.txt
rm -r release
rm -r PREVIOUS_RELEASE

# python -m odg -r -c -s

cd itembuilds
zip -r ../itembuilds.zip .
cd ..
# RELEASE_NAME=$(date +'%Y-%m-%d')

curl -L -o "PREVIOUS_RELEASE.zip" https://github.com/Egezenn/OpenDotaGuides/releases/latest/download/itembuilds.zip
unzip "PREVIOUS_RELEASE.zip" -d "PREVIOUS_RELEASE"
sh odg/scripts/diff.sh "itembuilds" "PREVIOUS_RELEASE"

mkdir release
mv itembuilds.zip release
mv comparison.diff release

rm -r data itembuilds
rm odg.log itembuilds.zip
rm -r PREVIOUS_RELEASE
rm "PREVIOUS_RELEASE.zip" comparison.diff