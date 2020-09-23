# fm
Install dependencies with:
```
pip3 install -r requirements.txt
mv token_sample.json token.json
```
Fill the token.json file with twitter api credentials (not needed if you do not plan to use the programm without arguments)

Run with:
```
python3 twitfm.py [song]
```
If no song are supplied, the programm will look on twitter for spotify song posted by user
