import json
import requests
from bs4 import BeautifulSoup
import sys
import string
from twilio.rest import Client
from time import sleep

global_client = Client("secret", "secret")

def send_text_message(text):
    to_phone = "+11DigitPhoneToText"
    from_phone = "+11DigitPhoneTextFrom"
    global_client.messages.create(to="+13045501189",
                       from_="+12018015162",
                       body=text)

def containsDigit(word):
    for ch in word:
        if ch in string.digits:
            return word

def meets_criteria(word):
    if not word.isupper():
        return False
    if len(word) < 5 or len(word) > 14:
        return False
    if not containsDigit(word):
        return False

    return True

def check_instagram():
    r = requests.get('https://www.instagram.com/chipotle/')
    soup = BeautifulSoup(r.text, 'lxml')

    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    relevant_captions = []
    index = 0
    for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        for caption in post['node']['edge_media_to_caption']['edges']:
            if index < 1:
                relevant_captions.append(caption['node']['text'])
        index += 1

    caption = relevant_captions[0].split(" ")
    word_to_text = "junk"

    for word in caption:
        if meets_criteria(word):
            word_to_text = word
            break

    stripped_word = word_to_text.strip()

    if stripped_word != "junk":
        print(stripped_word)
        send_text_message(stripped_word)
    else:
        pass


if __name__ == '__main__':
    for i in range(3600):
        check_instagram()
        sleep(1)
        i += 1
