# -*- coding: utf-8 -*-
import os
import fourchan_json
import fourchan_pic
import random
import string
import re
import reddit
from nltk.tag import pos_tag
import time
import requests
from bs4 import BeautifulSoup


class tcol:
        NORMAL = "\u000f"
        BOLD = "\u0002"
        UNDERLINE = "\u001f"
        REVERSE = "\u0016"
        WHITE = "\u00030"
        BLACK = "\u00031"
        DARK_BLUE = "\u00032"
        DARK_GREEN = "\u00033"
        RED = "\u00034"
        BROWN = "\u00035"
        GREEN = "\u00039"


def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    xfile = open(file_name)
    xfile.seek(random_point)
    c = xfile.read(1)
    s = ""
    while c != ".":
        c = xfile.read(1)

    xfile.read(1)
    c = xfile.read(1)
    while c == ".":
        xfile.read(1)
    while c != ".":
        if c != "\n":
            if c != "\r":
                s += c
            else:
                s += " "
        else:
            s += " "
        c = xfile.read(1)
    s += c
    c = xfile.read(1)
    s += c
    while c == ".":
        s += c
        c = xfile.read(1)
    s.replace("- ", " ")
    s = re.sub('\s+', ' ', s)
    return s


def getuser(ircmsg):
    return ircmsg.split(":")[1].split('!')[0]


_command_dict = {}


def command(name):
    # The decorator appending all fn's to a dict
    def _(fn):
        # Decorators return an inner function whom we
        # pass the function.
        _command_dict[name] = fn
    return _


def nothing(args):
    return ""


def get_command(name):
    # Explicity over implicity?
    # Fuck that

    # We just lower the string.
    # and check later its upper cased
    if name.lower() in _command_dict:
        return _command_dict[name.lower()]
    else:
        return nothing


def twitter(args):
    print(args["args"], type(args["args"]))
    if type(args["args"]) is not str:
        tweet = " ".join(args["args"])
        sendmsg = args["sendmsg"]
        channel = args["channel"]
    else:
        tweet = args
    r = requests.post("http://carta.im/tweetproxy/", data={'tweet': tweet[:139]})
    if "200" in r.text:
        return tweet[:139] + " @proxytwt"
    else:
        return ":( pls fix me ;-;"

def random_image(image_link):
    """
    Opens a directory with images using bs4.
    Then picks one value from list of images.
    """
    img_list = []
    soup = BeautifulSoup(requests.get(image_link).text, "html.parser")
    for i in soup.findAll("a"):
        parsed = image_link+i['href']
        img_list.append(parsed)
    img_link = random.choice(img_list)
    return img_link

@command("tweet")
def tweet(args):
    return twitter(args)

@command("rms.sexy")
def rms_sexy(args):
    return random_image("https://rms.sexy/img/")

@command("shitpost")
def shitposting(args):  # almost entirely automated shitposting

    shitpost = fourchan_json.get_random_post(args)
    res_shitpost = []
    for l in shitpost.splitlines():
        l = l.strip()
        if l.startswith(">"):
            l = tcol.DARK_GREEN + l + tcol.NORMAL
        res_shitpost.append(l)
    shitpost = " ".join(res_shitpost)

    if args["command"].isupper():
        shitpost = shitpost.upper()
    return shitpost

@command("pic")
def pic(args): #random pic from 4chan for big guys
    new_args = args["args"]
    new_args.append('')
    nick = args["prefix"].split('!')[0]
    random = True
    board_exists = False
    if len(new_args) != 1:
        random = False
        board_exists = fourchan_pic.open_board(new_args[0])
    if board_exists or random:
            response = '{}: {}'.format(nick, fourchan_pic.main(new_args))
            return response

@command("le")
def reddit_le(args):
    new_args = args["args"]

    subreddit = "linuxcirclejerk"
    if new_args:
        subreddit = new_args[0]

    try:
        response = reddit.get_random_comment(subreddit)
    except reddit.APIError as e:
        raise e
    except:
        raise Exception('Serious Reddit API error, everything is on fire')

    return response

@command("cybhelp")
def halp(args):
    user = getuser(args["raw"])
    string = user + ", sending you a private message of my commands.\n"
    args["sendmsg"](user, "ur a faget")
    return string


@command("interject")
def interjection(args):  # I'd just like to interject for a moment
    str = ("I'd just like to interject for moment. What you're referring to as "
              "Linux, is in fact, GNU/Linux, or as I've recently taken to calling it,"
              " GNU plus Linux. !http://pastebin.com/2YxSM4St\n")
    return str


@command("git")
def git(args):
    str = "!https://github.com/cybits/cybot What are we going to do on the repo? waaaah fork =3\n"
    return str
@command("reminder")
def reminder(args):  # today, I will remind them
    return ('Remember to fix your posture :D http://gateway.ipfs.io/ipfs/QmR91KZ77KMg1h8HqBTxtHNZiWCECiXhHkTR7coVqyyFvF/posture.jpg\n')

@command("memearrows")
def memearrows(args):  # >implying you can triforce
    str = ("Meme arrows are often used to preface implications or feels. See "
              "also: implying, feel.\n")
    return str


@command("int")
def intensifies(args):  # [python intensifies]
    if args["args"]:
        ret = "[" + " ".join(args["args"]) + " intensifies]\n"
    else:
        ret = "[no argument intensifies]\n"
    if args["command"].isupper():
        return ret.upper()
    else: return ret


# TODO: Use for something
def hello(user):  # This function responds to a user that inputs "Hello cybits"
    # random.randint(0, 5)
    str = ("are you even cyb, " + user + "?\n")
    return str


@command("ayylmao")
def ayylmao(args):
    sendmsg = args["sendmsg"]
    line = ('ABDUCTION: INCOMING')

    ayylien = ["       .-""""-.        .-""""-.    ",
               "      /        \      /        \   ",
               "     /_        _\    /_        _\  ",
               "    // \      / \\  // \      / \\ ",
               "    |\__\    /__/|  |\__\    /__/| ",
               "     \    ||    /    \    ||    /  ",
               "      \        /      \        /   ",
               "       \  __  /        \  __  /    ",
               "        '.__.' ayy lmao '.__.'     "]


    ircmsg = args["raw"]
    user = ircmsg.split(":")[1].split('!')[0]
    channel = args["channel"]
    sendmsg(channel, line)
    for lines in ayylien:
        sendmsg(user, lines)
        time.sleep(1)
   # ayy lmao
   # Doing all the logic inside the function
   # Since sendmsg wont post empty strings.
    return ""

@command("feel")
def feel(args):  # >tfw
    sendmsg = args["sendmsg"]
    line = ('"tfw no gf" is an abbreviated expression for "that feeling [I get] '
              'when [I have] no girlfriend" often used in online discussions and '
              'comments.')

    feelguy  = ["░░░░░░░▄▀▀▀▀▀▀▀▀▀▀▄▄░░░░░░░░░",
                "░░░░▄▀▀░░░░░░░░░░░░░▀▄░░░░░░░",
                "░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░",
                "░░█░░░░░░░░░░░░░░░░░░░░░▀▄░░░",
                "░▐▌░░░░░░░░▄▄▄▄▄▄▄░░░░░░░▐▌░░",
                "░█░░░░░░░░░░░▄▄▄▄░░▀▀▀▀▀░░█░░",
                "▐▌░░░░░░░▀▀▀▀░░░░░▀▀▀▀▀░░░▐▌░",
                "█░░░░░░░░░▄▄▀▀▀▀▀░░░░▀▀▀▀▄░█░",
                "█░░░░░░░░░░░░░░░░▀░░░▐░░░░░▐▌",
                "▐▌░░░░░░░░░▐▀▀██▄░░░░░░▄▄▄░▐▌",
                "░█░░░░░░░░░░░▀▀▀░░░░░░▀▀██░▀▄",
                "░▐▌░░░░▄░░░░░░░░░░░░░▌░░░░░░█",
                "░░▐▌░░▐░░░░░░░░░░░░░░▀▄░░░░░█",
                "░░░█░░░▌░░░░░░░░▐▀░░░░▄▀░░░▐▌",
                "░░░▐▌░░▀▄░░░░░░░░▀░▀░▀▀░░░▄▀░",
                "░░░▐▌░░▐▀▄░░░░░░░░░░░░░░░░█░░",
                "░░░▐▌░░░▌░▀▄░░░░▀▀▀▀▀▀░░░█░░░",
                "░░░█░░░▀░░░░▀▄░░░░░░░░░░▄▀░░░",
                "░░▐▌░░░░░░░░░░▀▄░░░░░░▄▀░░░░░",
                "░▄▀░░░▄▀░░░░░░░░▀▀▀▀█▀░░░░░░░",
                "▀░░░▄▀░░░░░░░░░░▀░░░▀▀▀▀▄▄▄▄▄"]


    ircmsg = args["raw"]
    user = ircmsg.split(":")[1].split('!')[0]
    channel = args["channel"]
    sendmsg(channel, line)
    for lines in feelguy:
        sendmsg(user, lines)
        time.sleep(1)
    # Doing all the logic inside the function
    # Since sendmsg wont post empty strings.
    return ""

@command("wake")
def wake(args):
    return "(can't wake up)"

@command("twerk")
def twerk(args):
    return "♪┏(・o･)┛♪┗ ( ･o･) ┓♪┏ (・o･) ┛♪┗ (･o･ ) ┓♪┏(･o･)┛♪"

# TODO: Use this for something
def autointerject(args):  # making sure users don't forget the GNU
    str1 = ("I'd just like to interject for moment. What you're referring to as Linux, is in fact, "
            "GNU/Linux - further messages sent privately.\n")

    str2 = ("I'd just like to interject for moment. What you're referring to as Linux, is "
            "in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux "
            "is not an operating system unto itself, but rather another free component of a fully"
            " functioning GNU system made useful by the GNU corelibs, shell utilities and vital "
            "system components comprising a full OS as defined by POSIX.\n"
            "Many computer users run a modified version of the GNU system every day, "
            "without realizing it. Through a peculiar turn of events, the version of GNU "
            "which is widely used today is often called Linux, and many of its users are not"
            " aware that it is basically the GNU system, developed by the GNU Project.\n"
            "There really is a Linux, and these people are using it, but it is just a "
            "part of the system they use. Linux is the kernel: the program in the system "
            "that allocates the machine's resources to the other programs that you run. "
            "The kernel is an essential part of an operating system, but useless by "
            "itself; it can only function in the context of a complete operating "
            "system.\n"
            "Linux is normally used in combination with the GNU operating system: the "
            "whole system is basically GNU with Linux added, or GNU/Linux. All the "
            "so-called Linux distributions are really distributions of GNU/Linux!\n")

    return str1, str2


@command("implying")
def implying(args):  # >implying this needs a comment
    return ('>implying is used in a mocking manner to challenge an "implication" '
            'that has been made, or sometimes it can be simply used as a joke in '
            'itself.\n')


@command("lit")
def sentence(args):  # This function grabs a random sentence from a txt file and posts it to the channel
    directory = os.path.dirname(__file__)
    directory = directory + os.path.join("/texts/books/")
    line = directory + os.path.join(random.choice(os.listdir(directory)))
    return get_random_line(line) + "\n"
    # return get_random_line(random.choice(os.listdir("/home/polaris/PycharmProjects/cybot/texts/"))) + "\n"

@command("guinea")
def guinea(args):
    directory = os.path.dirname(__file__)
    guinea = directory + os.path.join("/texts/other/guinea.txt")
    return random.choice(list(open(guinea)))

@command("checkem")
def checkem(args):
    not_dubs = random.randint(0, 99)
    return str(not_dubs).zfill(2)

@command("terry")
def terry(args):  # Grabs a random Terry quote from the 9front list
    directory = os.path.dirname(__file__)
    terry = directory + os.path.join("/texts/other/terry.txt")
    return random.choice(list(open(terry)))

@command("rob")
def pike(args):
    directory = os.path.dirname(__file__)
    pike = directory + os.path.join("/texts/other/rob.txt")
    return random.choice(list(open(pike)))

@command("gene")
def ray(args):
    directory = os.path.dirname(__file__)
    ray = directory + os.path.join("/texts/other/timecube.txt")
    return random.choice(list(open(ray)))

@command("linus")
def torv(args):
    directory = os.path.dirname(__file__)
    torv = directory + os.path.join("/texts/other/linus.txt")
    return random.choice(list(open(torv)))

@command("rms")
def stallman(args):
    directory = os.path.dirname(__file__)
    richard = directory + os.path.join("/texts/other/stallman.txt")
    return random.choice(list(open(richard)))

@command("eightball")
def eight(args):
    directory = os.path.dirname(__file__)
    eight = directory + os.path.join("/texts/other/eightball.txt")
    return random.choice(list(open(eight)))

@command("lewd")
def lewd(args):
    directory = os.path.dirname(__file__)
    lewd = directory + os.path.join("/texts/other/lewd.txt")
    return random.choice(list(open(lewd)))

@command("smug")
def smug(args):
    directory = os.path.dirname(__file__)
    smug = directory + os.path.join("/texts/other/smug.txt")
    return random.choice(list(open(smug)))

@command("joerogan")
def joerogan(args):
    sendmsg = args["sendmsg"]
    channel = args["channel"]
    if random.randrange(1,5) == 3: # chosen by fair dice roll.
                                   # guaranteed to be random.
        intromsg = [
            "THIS IS YOUR DAILY REMINDER TO PLUG IN YOUR BLENDERS, HEAT UP YOUR FLOTATION TANKS TO SKIN TEMP (35.5*C)",
            "THE WEED HAS BEEN LIT AND IT'S TIME TO SLAM YOUR KALE SHAKES, TAKE A TOKE & MARK OFF YOUR CHECKLIST TO POP YOUR:",
            "ALPHA BRAIN",
            "SHROOMTECH",
            "KRILL & MCT OIL",
            "PRIMATE CARE PILLS",
            "!https://www.youtube.com/watch?v=22GjkJw0WXk <---- HIT PLAY NIGGA"]
        for msg in intromsg:
            sendmsg(channel, msg)
            time.sleep(1)
        return ""
    else:
        directory = os.path.dirname(__file__)
        joerogan = directory + os.path.join("/texts/other/joerogan.txt")
        l = random.choice(list(open(joerogan)))
        l = l.strip()
        if l.startswith(">"):
            l = tcol.DARK_GREEN + l + tcol.NORMAL
        return l
        
@command("triforce")
def coolt(args):
    sendmsg = args["sendmsg"]
    channel = args["channel"]
    spaces1 = random.randint(1,5)
    spaces2 = random.randint(1,3)
    string1 = (" "*spaces1 + ("▲"))
    string2 = (" "*spaces2 + ("▲ ▲"))
    sendmsg(channel, string1)
    sendmsg(channel, string2)
    return ""

@command("booty")
def booty(args):
    return "( ͡° ͜ʖ ͡°)"


@command("shrug")
def shrug(args):
    return "¯\_(ツ)_/¯"

@command("denko")
def denko(args):
    return "(´･ω･`)"


@command("cute")
def cute(args):
    user = getuser(args["raw"])
    args = args["args"]
    if len(args) < 1:
        cutelist = ["✿◕ ‿ ◕✿", "❀◕ ‿ ◕❀", "(✿◠‿◠)",
                    "(◕‿◕✿) ", "( ｡◕‿◕｡)", "(◡‿◡✿)",
                    "⊂◉‿◉つ ❤", "{ ◕ ◡ ◕}", "( ´・‿-) ~ ♥",
                    "(っ⌒‿⌒)っ~ ♥", "ʕ´•ᴥ•`ʔσ”", "(･Θ･) caw",
                    "(=^･ω･^)y＝", "ヽ(=^･ω･^=)丿", "~(=^･ω･^)ヾ(^^ )",
                    "| (•□•) | (❍ᴥ❍ʋ)", "ϞϞ(๑⚈ ․̫ ⚈๑)∩", "ヾ(･ω･*)ﾉ",
                    "▽・ω・▽ woof~", "(◎｀・ω・´)人(´・ω・｀*)", "(*´・ω・)ノ(-ω-｀*)",
                    "(❁´ω`❁)", "(＊◕ᴗ◕＊)", "{´◕ ◡ ◕｀}", "₍•͈ᴗ•͈₎",
                    "(˘･ᴗ･˘)", "(ɔ ˘⌣˘)˘⌣˘ c)", "(⊃｡•́‿•̀｡)⊃", "(´ε｀ )♡",
                    "(◦˘ З(◦’ںˉ◦)♡", "( ＾◡＾)っ~ ❤ Leper",
                    "╰(　´◔　ω　◔ `)╯", "(*･ω･)", "(∗•ω•∗)", "( ◐ω◐ )"]
    else:
        args = " ".join(args)
        cutelist = ["(✿◠‿◠)っ~ ♥ " + args, "⊂◉‿◉つ ❤ " + args, "( ´・‿-) ~ ♥ " + args,
                    "(っ⌒‿⌒)っ~ ♥ " + args, "ʕ´•ᴥ•`ʔσ” BEARHUG " + args,
                    user + " ~(=^･ω･^)ヾ(^^ ) " + args, user + " (◎｀・ω・´)人(´・ω・｀*) " + args,
                    user + " (*´・ω・)ノ(-ω-｀*) " + args,
                    user + " (ɔ ˘⌣˘)˘⌣˘ c) " + args,
                    "(⊃｡•́‿•̀｡)⊃ U GONNA GET HUGGED " + args, args + " (´ε｀ )♡",
                    user + " (◦˘ З(◦’ںˉ◦)♡ " + args, "( ＾◡＾)っ~ ❤ " + args]
    return random.choice(cutelist)

@command("bots")
def bots(args):
    return "Reporting in! [Python] Try .cybhelp for commands."

@command("spikehog")
def spikehog(args):
    directory = os.path.dirname(__file__)
    spikehog = directory + os.path.join("/texts/other/spikehog.txt")
    return random.choice(list(open(spikehog)))

@command("rate")
def random_rate0(args):
    message = args["args"]
    give_rating = random.randint(0, 1)
    message = pos_tag(message)
    print(message)
    nounlist = []
    for word, tag in message:
        if tag == "NNP" or tag == "NN":
            nounlist.append(word)
    if not nounlist:
        nounlist.append("nothings")
    word = nounlist[random.randint(0, len(nounlist)-1)]
    rating = random.randint(0, 10)
    if give_rating or nounlist[0] == "nothings":
        return str(rating) + "/10"
    else:
        return word + "/10"


@command("r8")
def random_rate(args):
    message = args["args"]
    give_rating = random.randint(0, 1)
    message = pos_tag(message)
    print(message)
    nounlist = []
    for word, tag in message:
        if tag == "NNP" or tag == "NN":
            nounlist.append(word)
    if not nounlist:
        nounlist.append("nothings")
    word = nounlist[random.randint(0, len(nounlist)-1)]
    rating = random.randint(0, 10)
    if give_rating or nounlist[0] == "nothings":
        return str(rating) + "/10"
    else:
        return word + "/10"

@command("hackers")
def hackers(args):
    directory = os.path.dirname(__file__)
    hackers = directory + os.path.join("/texts/other/hackers.txt")
    return random.choice(list(open(hackers)))

@command("noided")
def noided(args):
    directory = os.path.dirname(__file__)
    noided = directory + os.path.join("/texts/other/grips.txt")
    return random.choice(list(open(noided)))

@command("just")
def just(args):
	return "...type it yourself..."

@command("spooky")
def spooky(args):
    directory = os.path.dirname(__file__)
    spook = directory + os.path.join("/texts/other/spooks.txt")
    return random.choice(list(open(spook)))

def breaklines(str):  # This function breaks lines at \n and sends the split lines to where they need to go
    strarray = string.split(str, "\n")
    return strarray

@command("ba")  
def ba(args):  
    #define a user agent  
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'}  
    baseurl = "http://www.beeradvocate.com"  
    if args["args"]:  
        try:  
            int(args["args"][-1])  
            payload = {"q" : " ".join(args["args"][:-1])}  
        except ValueError:  
            payload = {"q" : " ".join(args["args"])}  
        r = requests.get(baseurl + "/search/", headers=user_agent, params=payload)  
        if r.status_code == 200:  
            soup = BeautifulSoup(r.text, "html.parser")  
            regex = re.compile("/beer/profile/.*/.+") #so we match only the beers and not the brewery.
            beers = []
            for i in range(int(round(len(soup.find_all('a'))/2))):
                if re.match(regex, (soup.find_all('a')[i].get("href"))):
                    beers.append(soup.find_all('a')[i].get("href"))
            if len(beers) > 0:  
                data = beer_lookup(baseurl+beers[0], user_agent)
                print(data)
                oneliner = data['name'].decode() + " | " + data['style'].decode(), "BA score: " + data['ba_score'].decode() + " (From: " + data['ba_ratings'].decode() +") | Bro score: " + data['bro_score'].decode(), data['brewery'].decode() + " | " + data['abv'].decode(), ("!" + baseurl+beers[0])
                return " ".join(oneliner)
  
            else:  
               return "No results from BA."  
  
# BA helper function.  
def beer_lookup(url, user_agent):  
    r = requests.get(url, headers=user_agent)  
    if r.status_code == 200:  
        soup = BeautifulSoup(r.text, "html.parser")  
        table = soup.find('table', attrs = {"width" : "100%"})  
        data = []  
        rows = table.find_all("tr")  
        for r in rows:  
            cols = r.find_all("td")  
            cols = [e.text.strip() for e in cols]  
            data.append([e for e in cols if e])  
  
        info = {}  
        rel_data = data[0][1].split('\n')  
        info['name'] = soup.title.string.split("|")[0]  
        info['ba_score'] = rel_data[1]  
        info['ba_class'] = rel_data[2]  
        info['ba_ratings'] = rel_data[3]  
        info['bro_score'] = rel_data[7]  
        info['brewery'] = rel_data[25]  
        (info['style'], info['abv']) = rel_data[29].split("|")  
        for e in info.keys():  
            info[e] = info[e].encode("utf-8")
        return info  

bicd ={"epic":"ebin",
        "penis":"benis",
        "wh":"w",
        "th":"d",
        "af":"ab",
        "ap":"ab",
        "ca":"ga",
        "ck":"gg",
        "co":"go",
        "ev":"eb",
        "ex":"egz",
        "et":"ed",
        "iv":"ib",
        "it":"id",
        "ke":"ge",
        "nt":"nd",
        "op":"ob",
        "ot":"od",
        "po":"bo",
        "pe":"be",
        "pi":"bi",
        "up":"ub",
        "va":"ba",
        "cr":"gr",
        "kn":"gn",
        "lt":"ld",
        "mm":"m",
        "nt":"dn",
        "pr":"br",
        "ts":"dz",
        "tr":"dr",
        "bs":"bz",
        "ds":"dz",
        "fs":"fz",
        "gs":"gz",
        "is":"iz",
        "ls":"lz",
        "ms":"mz",
        "ns":"nz",
        "rs":"rz",
        "ss":"sz",
        "ts":"tz",
        "us":"uz",
        "ws":"wz",
        "ys":"yz",
        "alk":"olk",
        "ing":"ign",
        "ic":"ig",
        "ng":"nk",
        "kek":"geg",
        "some":"sum",
        "meme":"maymay"
}
ebinFaces = [ ':D', ':DD', ':DDD', ':-D', 'XD', 'XXD', 'XDD', 'XXDD' ];
@command("spurd")
def spurd(str):
	str.lower()
	for k, v in bicd.items():
		str = str.replace(k,v)
	
	return str+" "+ random.choice(ebinFaces)
