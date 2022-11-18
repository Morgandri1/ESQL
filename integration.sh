cd package
python3.10 -m build # adds to the dist folder so it can be uploaded
python3.10 -m twine upload dist/* # uploads the dist folder
rm -r dist # removes built files. this lets this file be run again
cd src
rm -r esql.egg-info # removes info from the src folder
echo "removed dist and egg-info packages. exiting..."
python3.10 -m pip install --upgrade esql # first try to update
python3.10 -m pip install --upgrade esql # second try to update