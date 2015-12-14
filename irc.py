import socket
import sys
import ssl
import time
import random
import itertools
from commands import get_command


# Basic config
server = "irc.rizon.net"
port = 6697
if len(sys.argv) < 2:
    print("Usage: main.py <channel> [nick]")
    exit(1)
channel = sys.argv[1]
botnick = "BOT" + str(random.randint(1, 9999)) if len(sys.argv) < 3 else sys.argv[2]
commandprefix = "."

def sendmsg(recipient, msg):
    """Sends a message."""
    if msg and isinstance(msg, tuple):
        for i in msg:
            ircsock.send("PRIVMSG %s :%s\n" % (recipient, i))
    elif msg:
        ircsock.send(bytes("PRIVMSG %s :%s\n" % (recipient, msg), 'UTF-8'))


def joinchan(chan):
    """Joins a channel."""
    print("trying")
    ircsock.send(bytes("JOIN %s\n" % chan, 'UTF-8'))


def parsemsg(s):
    """Breaks a message from an IRC server into its prefix, command, and
    arguments.
    """
    # TODO: Refactor the fuck out of this
    prefix = ""
    trailing = []
    retargs = []
    raw = s
    command = ""
    if not s:
        pass
    if s[0] == ":":
        prefix, s = s[1:].split(" ", 1)
    if s.find(" :") != -1:
        s, trailing = s.split(" :", 1)
        args = s.split()
        args.append(trailing)
        if trailing[0] == commandprefix:
            commands = args[2][1:].strip().split() if len(args) >= 3 else ""
            if commands:
                command = commands[0]
                retargs = commands[1:]
        else:
            pass
    else:
        args = s.split()
    event = args[0]
    channel = args[1]

    # If there is nothing in command at this point
    # We append whatever is in event as a command.
    # Easier to handle events like ping
    command = event if not command else command
    ret = {"prefix": prefix,
           "command": command,
           "raw": raw,
           "event": event,
           "args": retargs,
           "channel": channel,

        # Because circular imports
           "sendmsg": sendmsg}
    return ret


_partial_data = None


def process_data(data):
    """Process the data received from the socket. Ensures that there is no
    partial command at the end of the data chunk (that can happen if the data
    does not fit in the socket buffer). If that happens the partial command will
    be reconstructed next time this function is called.

    data: raw data from the socket.
    """
    global _partial_data

    data = data.decode(encoding='UTF-8')
    print(data)
    if not data:
        return []
    lines = data.splitlines()
    # There is at least one newline => this data chunk contains the end of at
    # least one command. If previous command was stored then it is complete now.
    if "\n" in data and _partial_data:
        lines[0] = _partial_data + lines[0]
        _partial_data = None
    # Store partial data.
    if not data.endswith("\n"):
        if _partial_data is None:
            _partial_data = ""
        _partial_data += lines.pop()
    return lines

def isplit(iterable,splitters):
    return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

def pipe_commands(args, channel):
    pipelist = args["args"].copy()
    pipelist.insert(0,args["command"])
    l = isplit(pipelist,"|")
    out = None
    for i in l:
        cmd = i[0].strip(".")
        a = i[1:]
        if out:
            a.append(out)
        args["command"] = cmd
        args["args"] = a
        print(a)
        c = get_command(args["command"])
        out = " ".join(c(args))
    sendmsg(channel, out)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(.5)
s.connect((server, port))
time.sleep(.5)
ircsock = ssl.wrap_socket(s)
time.sleep(.5)
ircsock.send(bytes("USER %s %s %s :some stuff\n" % (botnick, botnick, botnick), 'UTF-8'))
time.sleep(.5)
ircsock.send(bytes("NICK %s\n" % botnick, 'UTF-8'))
time.sleep(.5)
joinchan(channel)

while True:
    data = ircsock.recv(1024)
    for ircmsg in process_data(data):
        if "PING :" in ircmsg:
            ircsock.send(bytes("PONG :ping\n", 'UTF-8'))
        elif channel in ircmsg:
            args = parsemsg(str(ircmsg))
            if "|" in args["args"]:
                pipe_commands(args, channel)
            else:
                cmd = get_command(args["command"])
                try:
                    sendmsg(channel, cmd(args))
                except Exception as e:
                    print(e)
                    sendmsg(channel, (str(e)))
        else:
            continue
