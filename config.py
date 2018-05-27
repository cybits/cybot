import sys
import json
import random
class Config:
    with open(sys.argv[1], 'r') as data_file:
        try:
            config = json.loads(data_file.read())
        except ValueError:
            print('Please provide valid config')
            exit(1)
    try:
        server = config["server"]
        port = config["port"]
        channels = config["channels"]
        if config["bot_nick"]:
            bot_nick = config["bot_nick"]
        else:
            bot_nick = "BOT" + str(random.randint(1, 9999))
        password = config["password"]
        prefix = config["prefix"]
        untappd_cookie = config["untappd_cookie"]

    except KeyError:
        print('Please provide valid config')
        exit(1)
