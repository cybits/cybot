import requests
import random
import re
from bs4 import BeautifulSoup

base_url = 'https://pornhub.com'

class APIError(Exception):
    pass

def get(url, no_cache=False):
    headers = {
        'User-Agent': 'cybits a cute IRC bot',
    }
    if no_cache:
        headers['Cache-Control'] = 'private,max-age=0'
    return requests.get(base_url + url, headers=headers)

# Fetch comments from a given pornhub page (or a random one if unspecified)
def get_comments(url):
    comments = []
    tries = 0
    while len(comments) < 2:
        if tries > 5:
            return ["Too many attempts"]
        print("Getting...")
        r = get(url)
        soup = BeautifulSoup(str(r.content, 'UTF-8', errors='replace'))
        comments = soup.findAll('div', class_='commentMessage')
        #try:
        #    len(comments)
        #except e:
        #    print(e)
        #    import code; code.interact(local=dict(globals(), **locals()))
        if comments is None:
            print("bloop")
            comments = []
        tries += 1

    comments.pop()
    comments_sanitised = list(map(lambda x : x.find('span').text,comments))
    return comments_sanitised

def get_random_comment(url = '/random'):
    comments = get_comments(url)
    return random.choice(comments)
