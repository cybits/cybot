# Import some necessary libraries.
import socket
import os
import random
import string
import fourchan_json

# Some basic variables used to configure the bot        
server = "irc.rizon.net"  # Server
channel = "#/g/punk"  # Channel
botnick = "cybits"  # Your bots nick

def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    xfile = open(file_name)
    xfile.seek(random_point)
    c = xfile.read(1)
    s = ""
    while c != ".":
        c = xfile.read(1)

    c = xfile.read(1)
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


def ping():  # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :pingis\n")


def sendmsg(chan, msg):  # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG "+chan + " :"+msg+"\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN "+chan + "\n")

def halp(user):
    ircsock.send("PRIVMSG "+channel + " :Sending you private message of my commands.\n")
    ircsock.send("PRIVMSG "+user + " :ur a faget\n")

def interjection():  # I'd just like to interject for a moment
    ircsock.send("PRIVMSG "+channel + " :I'd just like to interject for moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. pastebin.com/2YxSM4St\n")

def memearrows():  # >implying you can triforce
    ircsock.send("PRIVMSG "+channel + " :Meme arrows are often used to preface implications or feels. See also: implying, feel.\n")

def intensifies(args):  # [python intensifies]
    if len(args.split(".int ")) > 1:
        args = args.split(".int ")[1].strip('\r\n')
        ircsock.send("PRIVMSG "+channel + " :[" + args + " intensifies]\n")
    else:
        ircsock.send("PRIVMSG "+channel + " :[no argument intensifies]\n")

def hello(user):  # This function responds to a user that inputs "Hello cybits"
    # random.randint(0, 5)
    ircsock.send("PRIVMSG "+channel + " :are you even cyb, " + user + "?\n")

def feel():  # >tfw
    ircsock.send("PRIVMSG "+channel + ' :"tfw no gf" is an abbreviated expression for "that feeling [I get] when [I have] no girlfriend" often used in online discussions and comments.\n')

def autointerject(user):  # making sure users don't forget the GNU
    ircsock.send("PRIVMSG "+channel + " :I'd just like to interject for moment. What you're referring to as Linux, is in fact, GNU/Linux - further messages sent privately.\n")
    ircsock.send("PRIVMSG "+user + " :I'd just like to interject for moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.\n")
    ircsock.send("PRIVMSG "+user + " :Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.\n")
    ircsock.send("PRIVMSG "+user + " :There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system.\n")
    ircsock.send("PRIVMSG "+user + " :Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!\n")


def implying():  # >implying this needs a comment
    ircsock.send("PRIVMSG "+channel + ' :implying is used in a mocking manner to challenge an "implication" that has been made, or sometimes it can be simply used as a joke in itself.\n')

def sentence():  # This function grabs a random sentence from a txt file and posts it to the channel
    ircsock.send("PRIVMSG "+channel + " :" +
                 get_random_line(random.choice(os.listdir("/home/pi/PycharmProjects/cybot/texts/"))) + "\n")

def shitpost():  # almost entire automated shitposting
    post = "None"
    while post == "None":
        post = str(fourchan_json.get_random_post())
    ircsock.send("PRIVMSG "+channel + " :" + post + "\n")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # connect to the server using the port 6667
ircsock.send("USER "+botnick + " " + botnick+" " + botnick + " :some stuff\n")  # user authentication
ircsock.send("NICK "+botnick + "\n")  # here we actually assign the nick to the bot

joinchan(channel)  # Join the channel using the functions we previously defined

while 1:
    ircmsg = ircsock.recv(1024)  # receive data from the server
  # ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
    print(ircmsg)  # Here we print what's coming from the server


    # if ircmsg.find(botnick) != -1 and ircmsg.find("PRIVMSG ") != -1 and ircmsg.find("rizon") == -1:
    # # If we can find "cybits" it will call the function hello()
    #     hello(ircmsg.split(":")[1].split('!')[0])
    #     continue

    if ircmsg.find(" :.lit") != -1 and ircmsg.find(channel) != -1:  # If we can find ".lit" it will call the function sentence()
        sentence()
        continue

    if ircmsg.find(" :.feel") != -1 and ircmsg.find(channel) != -1:  # If we can find ".feel" it will call the function feel()
        feel()
        continue

    if ircmsg.find(" :.interject") != -1 and ircmsg.find(channel) != -1:  # If we can find ".interject" it will call the function interjection()
        interjection()
        continue
    #
    # lircmsg = string.lower(ircmsg);
    # if lircmsg.find("linux") != -1 and lircmsg.find("gnu") == -1 and lircmsg.find("linuz") == -1 \
    #         and lircmsg.find("kernel") == -1  and ircmsg.find(channel) != -1:  # mods are asleep, post interjects
    #     autointerject(ircmsg.split(":")[1].split('!')[0])
    #     continue

    if ircmsg.find(" :.implying") != -1 and ircmsg.find(channel) != -1:  # If we can find ".implying" it will call the function implying()
        implying()
        continue

    if ircmsg.find(" :.memearrows") != -1 and ircmsg.find(channel) != -1:  # If we can find ".memearrows" it will call the function memearrows()
        memearrows()
        continue

    if ircmsg.find(" :.shitpost") != -1 and ircmsg.find(channel) != -1:  # If we can find ".interject" it will call the function interjection()
        shitpost()
        continue

    if ircmsg.find(" :.int") != -1 and ircmsg.find(channel) != -1:  # If we can find ".int" it will call the function intensifies()
        intensifies(ircmsg.split(":")[2].split('!')[0])
        continue

    if ircmsg.find(" :.cybhelp") != -1 and ircmsg.find(channel) != -1:  # If we can find ".cybhelp" it will call the function help()
        halp(ircmsg.split(":")[1].split('!')[0])
        continue

    if ircmsg.find("PING :") != -1:  # respond to pings
        ping()
