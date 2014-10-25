# Import some necessary libraries.
import socket
import string
import commands

# Some basic variables used to configure the bot        
server = "irc.rizon.net"  # Server
channel = "#omgatestchannel"  # Channel
botnick = "cybits1"  # bot's nick


def ping():  # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :ping\n")


def sendmsg(recipient, msg):  # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG " + recipient + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")



ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # connect to the server using the port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick + " :some stuff\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # here we actually assign the nick to the bot
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
        sendmsg(channel, commands.sentence())
        continue

    if " :.feel" in ircmsg and channel in ircmsg:  # If we can find ".feel" it will call the function feel()
        array = commands.feel()
        sendmsg(channel, array[0])
        user = ircmsg.split(":")[1].split('!')[0]
        sendmsg(user, array[1])
        continue

    if " :.interject" in ircmsg and channel in ircmsg:  # If we can find ".interject" it will call the function
        sendmsg(channel, commands.interjection())       # interjection()
        continue

    # lircmsg = string.lower(ircmsg)
    # if "linux" in ircmsg and "gnu" not in ircmsg and "linuz" not in ircmsg and "source" not in ircmsg \
    #         and "kernel" not in ircmsg and channel in ircmsg:  # mods are asleep, post interjects
    #     user = ircmsg.split(":")[1].split('!')[0]
    #     msg, msg1, msg2, msg3, msg4 = commands.autointerject()
    #     sendmsg(channel, msg)
    #     sendmsg(user, msg1)
    #     sendmsg(user, msg2)
    #     sendmsg(user, msg3)
    #     sendmsg(user, msg4)
    #     continue

    if " :.implying" in ircmsg and channel in ircmsg:  # If we can find ".implying" it will call the function implying()
        sendmsg(channel, commands.implying())
        continue

    if " :.memearrows" in ircmsg and channel in ircmsg:  # If we can find ".memearrows" it will call the function
        sendmsg(channel, commands.memearrows())          # memearrows()
        continue

    if " :.shitpost" in ircmsg and channel in ircmsg:  # If we can find ".shitpost" it will call the function
        sendmsg(channel, commands.shitpost())          # shitpost()
        continue

    if " :.SHITPOST" in ircmsg and channel in ircmsg:        # If we can find ".SHITPOST" it will call the function
        sendmsg(channel, string.upper(commands.shitpost()))  # shitpost(), but in caps
        continue

    if " :.int" in ircmsg and channel in ircmsg:  # If we can find ".int" it will call the function intensifies()
        sendmsg(channel, commands.intensifies(ircmsg.split(":")[2].split('!')[0]))
        continue

    if " :.cybhelp" in ircmsg and channel in ircmsg:  # If we can find ".cybhelp" it will call the function help()
        user = ircmsg.split(":")[1].split('!')[0]
        array = commands.halp(user)
        sendmsg(channel, array[0])
        sendmsg(user, array[1])
        continue
    if " :.git" in ircmsg and channel in ircmsg:
        sendmsg(channel, commands.git())
        continue

    if "PING :" in ircmsg:  # respond to pings
        ping()
