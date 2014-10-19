import irc
import os
import fourchan_json
import random

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
        c = xfile.read(1)
    s += c
    c = xfile.read(1)
    s += c
    while c == ".":
        s += c
        c = xfile.read(1)
    s.replace("- ", " ")
    return s


def halp(user):
    irc.ircsock.send("PRIVMSG " + irc.channel + " :Sending you private message of my commands.\n")
    irc.ircsock.send("PRIVMSG " + user + " :ur a faget\n")


def interjection():  # I'd just like to interject for a moment
    irc.ircsock.send("PRIVMSG "+ irc.channel + " :I'd just like to interject for moment. What you're referring to as "
                                               "Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, "
                                               "GNU plus Linux. pastebin.com/2YxSM4St\n")


def memearrows():  # >implying you can triforce
    irc.ircsock.send("PRIVMSG "+ irc.channel + " :Meme arrows are often used to preface implications or feels. See "
                                               "also: implying, feel.\n")


def intensifies(args):  # [python intensifies]
    if len(args.split(".int ")) > 1:
        args = args.split(".int ")[1].strip('\r\n')
        irc.ircsock.send("PRIVMSG " + irc.channel + " :[" + args + " intensifies]\n")
    else:
        irc.ircsock.send("PRIVMSG " + irc.channel + " :[no argument intensifies]\n")


def hello(user):  # This function responds to a user that inputs "Hello cybits"
    # random.randint(0, 5)
    irc.ircsock.send("PRIVMSG " + irc.channel + " :are you even cyb, " + user + "?\n")


def feel():  # >tfw
    irc.ircsock.send("PRIVMSG " + irc.channel + ' :"tfw no gf" is an abbreviated expression for "that feeling [I get] '
                                               'when [I have] no girlfriend" often used in online discussions and '
                                               'comments.\n')


def autointerject(user):  # making sure users don't forget the GNU
    irc.ircsock.send("PRIVMSG "+ irc.channel +
                     " :I'd just like to interject for moment. What you're referring to as Linux, is in fact, "
                     "GNU/Linux - further messages sent privately.\n")
    irc.ircsock.send("PRIVMSG "+user + " :I'd just like to interject for moment. What you're referring to as Linux, is "
                 "in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux "
                 "is not an operating system unto itself, but rather another free component of a fully"
                 " functioning GNU system made useful by the GNU corelibs, shell utilities and vital "
                 "system components comprising a full OS as defined by POSIX.\n")
    irc.ircsock.send("PRIVMSG "+user + " :Many computer users run a modified version of the GNU system every day, "
                                       "without realizing it. Through a peculiar turn of events, the version of GNU "
                                       "which is widely used today is often called Linux, and many of its users are not"
                                       " aware that it is basically the GNU system, developed by the GNU Project.\n")
    irc.ircsock.send("PRIVMSG " + user + " :There really is a Linux, and these people are using it, but it is just a "
                                         "part of the system they use. Linux is the kernel: the program in the system "
                                         "that allocates the machine's resources to the other programs that you run. "
                                         "The kernel is an essential part of an operating system, but useless by "
                                         "itself; it can only function in the context of a complete operating "
                                         "system.\n")
    irc.ircsock.send("PRIVMSG " + user + " :Linux is normally used in combination with the GNU operating system: the "
                                         "whole system is basically GNU with Linux added, or GNU/Linux. All the "
                                         "so-called Linux distributions are really distributions of GNU/Linux!\n")


def implying():  # >implying this needs a comment
    irc.ircsock.send("PRIVMSG " + irc.channel + ' :>implying is used in a mocking manner to challenge an "implication" '
                                                'that has been made, or sometimes it can be simply used as a joke in '
                                                'itself.\n')


def sentence():  # This function grabs a random sentence from a txt file and posts it to the channel
    irc.ircsock.send("PRIVMSG " + irc.channel + " :" +
                 get_random_line(random.choice(os.listdir("/home/polaris/PycharmProjects/cybot/texts/"))) + "\n")


def shitpost():  # almost entirely automated shitposting
    post = "None"
    while post == "None":
        post = str(fourchan_json.get_random_post())
    irc.ircsock.send("PRIVMSG "+ irc.channel + " :" + post + "\n")

