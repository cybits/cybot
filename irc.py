# Import some necessary libraries.
import socket
import commands.py
import string

# Some basic variables used to configure the bot        
server = "irc.rizon.net"  # Server
channel = "#omgatestchannel"  # Channel
botnick = "cybits1"  # Your bots nick


def ping():  # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :pingis\n")


def sendmsg(chan, msg):  # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG "+chan + " :"+msg+"\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN "+chan + "\n")



ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # connect to the server using the port 6667
ircsock.send("USER "+botnick + " " + botnick+" " + botnick + " :some stuff\n")  # user authentication
ircsock.send("NICK "+botnick + "\n")  # here we actually assign the nick to the bot

joinchan(channel)  # Join the channel using the functions we previously defined

while 1:
    ircmsg = ircsock.recv(1024)  # receive data from the server
  # ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
    print(ircmsg)  # Here we print what's coming from the server

    # if ircmsg.find(botnick) in ircmsg and "PRIVMSG ") in ircmsg and "rizon") == -1:
    # # If we can find "cybits" it will call the function hello()
    #     hello(ircmsg.split(":")[1].split('!')[0])
    #     continue

    if " :.lit" in ircmsg and channel in ircmsg:  # If we can find ".lit" it will call the function sentence()
        commands.sentence()
        continue

    if " :.feel" in ircmsg and channel in ircmsg:  # If we can find ".feel" it will call the function feel()
        commands.feel()
        continue

    if " :.interject" in ircmsg and channel in ircmsg:  # If we can find ".interject" it will call the function
                                                        # interjection()
        commands.interjection()
        continue

    lircmsg = string.lower(ircmsg)
    if "linux" in ircmsg and "gnu" not in ircmsg and "linuz" not in ircmsg \
            and "kernel" not in ircmsg and channel in ircmsg:  # mods are asleep, post interjects
        commands.autointerject(ircmsg.split(":")[1].split('!')[0])
        continue

    if " :.implying" in ircmsg and channel in ircmsg:  # If we can find ".implying" it will call the function implying()
        commands.implying()
        continue

    if " :.memearrows" in ircmsg and channel in ircmsg:  # If we can find ".memearrows" it will call the function
                                                         # memearrows()
        commands.memearrows()
        continue

    if " :.shitpost" in ircmsg and channel in ircmsg:  # If we can find ".interject" it will call the function
                                                       # interjection()
        commands.shitpost()
        continue

    if " :.int" in ircmsg and channel in ircmsg:  # If we can find ".int" it will call the function intensifies()
        commands.intensifies(ircmsg.split(":")[2].split('!')[0])
        continue

    if " :.cybhelp" in ircmsg and channel in ircmsg:  # If we can find ".cybhelp" it will call the function help()
        commands.halp(ircmsg.split(":")[1].split('!')[0])
        continue

    if "PING :" in ircmsg:  # respond to pings
        ping()
