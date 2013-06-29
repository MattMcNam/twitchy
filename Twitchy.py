'''
Twitchy.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

from twitchy import BotManager
import traceback
import time

def main():
    botManager = BotManager.BotManager()
    
    if botManager.configure():
        print("Configured, attempting to connect...")
    else:
        print("Unable to configure Twitchy")
        return 1
    
    try:
        botManager.connect()
        botManager.run()
    except:
        print(traceback.format_exc())
        return 1
    
    while botManager.shouldRun():
        time.sleep(5)

if __name__ == '__main__':
    exit(main())
