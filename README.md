# fm
Install dependencies with:
```
pip3 install -r requirements.txt
mv token_sample.json token.json
```
youtube-dl and ffmpeg must in your PATH
Fill the token.json file with twitter api credentials (not needed if you do not plan to use the radio command)

Run with:
```
python3 twitfm.py
```
commands:
```
radio                   #will start looking through twitter for spotify link that will be played
play [song]             #replace [song] with a https://youtu.be or https://open.spotify.com link
stop                    #stop the music
delete                  #delete all downloaded mp3
exit                    #exit the program
```
