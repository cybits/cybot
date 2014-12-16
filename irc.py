# Import some necessary libraries.
import socket
import string
import time
import sched
import requests
from commands import get_command

# Some basic variables used to configure the bot
server = "irc.rizon.net"  # Server
channel = "#cybitsBETA"  # Channel
botnick = "cybitsBETA"  # bot's nick
commandprefix = "."
# channel = "#omgatestchannel"  # Channel
# botnick = "cybits1"  # bot's nick




def sendmsg(recipient, msg):  # This is the send message function, it simply sends messages to the channel.
    if msg:
        ircsock.send("PRIVMSG " + recipient + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")


def _parsemsg(s):
    # I'm lazy - Fox
    # Breaks a message from an IRC server into its prefix, command, and arguments.
    prefix = ''
    trailing = []
    if not s:
        pass
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    ret = {"prefix": prefix,
           "command": command,
           "raw": s,
           "args": args,

        # Because circular imports
           "sendmsg": sendmsg}
    return ret

def parsemsg(s):
    # Breaks a message from an IRC server into its prefix, command, and arguments.
    prefix = ''
    trailing = []
    raw = s
    command = ""
    if not s:
        pass
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
        command = args[2][1:].strip() if len(args) >= 3 else ""
    else:
        args = s.split()
    event = args[0]
    ret = {"prefix": prefix,
           "command": command,
           "raw": raw,
           "event": event,
           "args": args,

        # Because circular imports
           "sendmsg": sendmsg}
    return ret

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # connect to the server using the port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick + " :some stuff\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # here we actually assign the nick to the bot
joinchan(channel)  # Join the channel using the functions we previously defined

while 1:
    ircmsg = ircsock.recv(1024)  # receive data from the server
    #print(ircmsg)  # Here we print what's coming from the server
    # if ircmsg.find(botnick) in ircmsg and "PRIVMSG " in ircmsg:
    # # # If we can find "cybits" it will call the function hello()
    #     hello(getuser(ircmsg))
    #     continue


    args = parsemsg(ircmsg)
    print args
    cmd = get_command(args["command"])
    sendmsg(channel, cmd(args))
