# python -m venv .venv
# source .venv/Scripts/activate
# python -m pip install --upgrade pip
# pip install -r requirements.txt
RELEASE_NAME=$(date +'%Y-%m-%d %H.%M.%S')

python -m odg -r -c -s

cd itembuilds
zip -q -r ../itembuilds.zip .
cd ..

curl -s -L -o "PREVIOUS_RELEASE.zip" https://github.com/Egezenn/OpenDotaGuides/releases/latest/download/itembuilds.zip
unzip -q "PREVIOUS_RELEASE.zip" -d "PREVIOUS_RELEASE"
bash ./scripts/diff.sh "itembuilds" "PREVIOUS_RELEASE"

mkdir -p release/"$RELEASE_NAME"
mv itembuilds.zip release/"$RELEASE_NAME"
mv comparison.diff release/"$RELEASE_NAME"

rm odg.log PREVIOUS_RELEASE.zip
rm -r data itembuilds PREVIOUS_RELEASE 