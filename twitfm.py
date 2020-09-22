import youtube_dl as ydl
from playsound import playsound
#import twitter as tw
import os
import random
import string

def random_string(length):
    letters = string.ascii_lowercase
    return (''.join(random.choice(letters) for i in range(length)))

filename = random_string(32)

option = {
    'outtmpl' : filename
}

url = 'https://youtu.be/jKW4s02ib7s'

if url.startswith('https://youtu.be/') and url[-11:].isalnum():
    yt = ydl.YoutubeDL(option)
    yt.download([url])
    if os.path.exists(filename + '.webm'):
        os.system('ffmpeg -i ' + filename + '.webm -vn -c:a libmp3lame -y ' + filename + '.mp3')
        os.remove(filename + '.webm')
    if os.path.exists(filename + '.mkv'):
        os.system('ffmpeg -i ' + filename + '.mkv -vn -c:a libmp3lame -y ' + filename + '.mp3')
        os.remove(filename + '.mkv')
    playsound(filename + '.mp3')
    os.remove(filename + '.mp3')