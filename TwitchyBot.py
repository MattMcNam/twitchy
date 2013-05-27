'''
TwitchyBot.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

from twitchy import Bot
import traceback

def main():
    bot = Bot.Bot()
    
    if bot.configure():
        print("Configured, attempting to connect...")
    else:
        print("Unable to configure Twitchy")
        return 1
    
    try:
        print("blah")
        return 0
        #bot.connect()
        #return bot.run()
    except Exception as e:
        print(traceback.format_exc())
        return 1

if __name__ == '__main__':
    exit(main())
