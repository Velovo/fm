from playsound import playsound
import twitter as tw
import requests
import os
import sys
import random
import string
import json
import time
import eyed3

token_filename = 'token.json'

token = json.load(open(token_filename, 'r'))

api = tw.Api(consumer_key=token['consumer_key'],
            consumer_secret=token['consumer_secret'],
            access_token_key=token['access_token_key'],
            access_token_secret=token['access_token_secret'])

def random_string(length):
    letters = string.ascii_lowercase
    return (''.join(random.choice(letters) for i in range(length)))

def test_string(strr):
    for i in strr:
        if i.isalnum() or i == '-' or i == '?' or i == '=':
            pass
        else:
            return 1
    return 0

def download_and_play(filename, url):
    if url.startswith('https://youtu.be/') and test_string(url.split('https://youtu.be/')[1]) == 0:
        print('Starting youtube-dl')
        os.system('youtube-dl --extract-audio --audio-format mp3 -o "' + filename + '.%(ext)s" ' + url)
        print('Can\'t get metadata trough youtube')
        playsound(filename + '.mp3')
        print('Finished audio\ndeleting file')
        os.remove(filename + '.mp3')
    elif url.startswith('https://open.spotify.com/track/') and test_string(url.split('https://youtu.be/')[1]) == 0:
        print('Starting spotdl')
        os.system('spotdl -o mp3 -f' + filename + '.mp3 --song ' + url)
        c_file = eyed3.load(filename + '.mp3')
        print('Finished downloading\nTitle:  ' + c_file.tag.title + '\nArtist: ' + c_file.tag.artist)
        playsound(filename + '.mp3')
        print('Finished audio\ndeleting file')
        os.remove(filename + '.mp3')

def geturl():
    i = 0
    url = None

    print('Getting url')
    while url == None:
        i = 0
        ret = api.GetSearch(raw_query='q=open.spotify.com&result_type=recent&count=10')
        while i < 10 and url == None:
            try:
                url = ret[i].urls[0].expanded_url
                if not url.startswith('https://open.spotify.com/track/'):
                    url = None
            except:
                pass
            i = i + 1
    return url

def main():
    url = None
    i = 1

    if len(sys.argv) > 1:
        while i < len(sys.argv):
            print(i, len(sys.argv))
            filename = random_string(32)
            download_and_play(filename, sys.argv[i])
            i = i + 1
    else:
        while (True):
            url = None
            while url == None:
                url = geturl()
                if url == None:
                    time.sleep(10)
            filename = random_string(32)
            download_and_play(filename, url)

if __name__ == "__main__":
    main()
