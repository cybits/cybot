# Import some necessary libraries.
import socket
import string
import sched
import requests
from commands import get_command

# Some basic variables used to configure the bot
server = "irc.rizon.net"  # Server
channel = "#/g/punk"  # Channel
botnick = "cybits"  # bot's nick
commandprefix = "."


def sendmsg(recipient, msg):  # This is the send message function, it simply sends messages to the channel.
    if msg and isinstance(msg, tuple):
        for i in msg:
            ircsock.send("PRIVMSG " + recipient + " :" + i + "\n")
    elif msg:
        ircsock.send("PRIVMSG " + recipient + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")


def parsemsg(s):
    # TODO: Refactor the fuck out of this
    # Breaks a message from an IRC server into its prefix, command, and arguments.
    prefix = ''
    trailing = []
    retargs = []
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
        commands = args[2][1:].strip().split() if len(args) >= 3 else ""
        if commands:
            command = commands[0]
            retargs = commands[1:]
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

    if not data:
        return []
    lines = data.splitlines()
    # There is at least one newline => this data chunk contains the end of at
    # least one command. If previous command was stored then it is complete now.
    if '\n' in data and _partial_data:
        lines[0] = _partial_data + lines[0]
        _partial_data = None
    # Store partial data.
    if not data.endswith('\n'):
        if _partial_data is None:
            _partial_data = ''
        _partial_data += lines.pop()
    return lines


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # connect to the server using the port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick + " :some stuff\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # here we actually assign the nick to the bot
joinchan(channel)  # Join the channel using the functions we previously defined


while True:
    data = ircsock.recv(1024)
    for ircmsg in process_data(data):
        if "PING :" in ircmsg:
            ircsock.send("PONG :ping\n")
        else:
            args = parsemsg(ircmsg)
            cmd = get_command(args["command"])
            try:
                sendmsg(channel, cmd(args))
            except Exception as e:
                sendmsg(channel, (str(e), "plz, fix me mother valka"))
