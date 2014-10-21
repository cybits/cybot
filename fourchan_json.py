import json
import urllib
import random
import sys
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
        def __init__(self):
                self.reset();
                self.fed = []
        def handle_data(self, d):
                self.fed.append(d)
        def get_data(self):
                return ''.join(self.fed)

def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data();

# class tcol:
#         HEADER = '\033[95m'
#         OKBLUE = '\033[94m'
#         OKGREEN = '\033[92m'
#         WARNING = '\033[93m'
#         FAIL = '\033[91m'
#         ENDC = '\033[0m'

def formatText(text):
        text = text.replace("<br>", " ");
        text = text.replace("&gt;", ">");
        text = text.replace("&#039;", "'")
        text = strip_tags(text)
        return text

def write(text):
        sys.stdout.write(text)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_boards_json():
    response = urllib.urlopen("http://a.4cdn.org/boards.json")
    return json.loads(response.read())


def get_page_json(board, pageindex):
    return json.loads((urllib.urlopen("http://a.4cdn.org/" + board + "/" + str(pageindex) + ".json")).read())


def get_thread_json(board, threadno):
    return json.loads((urllib.urlopen("http://a.4cdn.org/" + board + "/thread/" + str(threadno) + ".json")).read())


def get_OP_no(pagedata, threadindex):
    return pagedata['threads'][threadindex]['posts'][0]['no']

def get_random_post():

    for iterations in range(0, 10):
        data = get_boards_json()

        allboards = data['boards']

        i = random.randint(0, len(allboards)-1)

        board = allboards[i]['board']
        numpages = allboards[i]['pages']

        i = random.randint(1, numpages)

        pagedata = get_page_json(board, i)
        threads = pagedata['threads']
        numthreads = len(threads)

        i = random.randint(0, numthreads-1)

        threadno = get_OP_no(pagedata, i)
        thread = get_thread_json(board, threadno)

        j = random.randint(0, len(thread['posts'])-1)

        postinfo = json.dumps(thread['posts'][j])

        if 'com' in postinfo and 'sticky' not in postinfo:
            content = thread['posts'][j]['com']
            text = (formatText(content))

            if len(text) > 1:
                final = text.encode('utf-8')
                return final
            else:
                get_random_post()

        elif iterations == 10:
            return ("No shitpost found.")

        else:
            get_random_post()

get_random_post()