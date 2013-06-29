''''
BotManager.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''
from threading import Thread
from private import ConfigObj
import Bot, PluginManager

class BotManager:
    '''
    Class which configures and runs bots
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.bots = {}
        self._failedBots = []
        self.config = None
        self._shouldRun = True
        
        PluginManager._loadPlugins()
        
    def configure(self, filename = "config.cfg"):
        '''
        Reads form filename provided and tries to configure Twitchy
        '''
        self.config = ConfigObj.ConfigObj(filename)
        
        retVal = True
        
        if 'admin_accounts' not in self.config:
            print("[Config] 'admin_accounts' is not present. You need at least one admin account")
            retVal = False
        if 'accounts' not in self.config:
            print("[Config] 'accounts' section is missing!")
            retVal = False
        elif len(self.config['accounts']) < 1:
            print("[Config] One account must be present in the 'accounts' section")
            retVal = False
        if 'channels' not in self.config:
            print("[Config] 'channels' section is missing!")
            retVal = False
        elif len(self.config['channels']) < 1:
            print("[Config] One channel must be present in the 'channels' section")
            retVal = False
            
        if retVal:
            print("[Config] Found required settings, checking optional settings")
        else:
            return False
        
        if 'delay_all_messages' not in self.config:
            print("[Config] 'delay_all_messages' not specified, defaulting to True")
            self.config['delay_all_messages'] = True
        if 'webui_enabled' not in self.config:
            print("[Config] 'webui_enabled' not specified, defaulting to False")
            self.config['webui_enabled'] = False
        if 'webui_port' not in self.config:
            print("[Config] 'webui_port' not specified, defaulting to 9090")
            self.config['webui_port'] = 9090
        
        self.config.write()
        
        return True
    
    def connect(self):
        for account in self.config['accounts']:
            bot = Bot(account['username'], account['password'])
            try:
                bot.connect()
            except:
                print("Unable to connect as '"+account+"'")
                self._failedBots.append(account)
            self.bots[account] = bot
        
        for channel in self.config['channels']:
            shortAcc = channel['account']
            if shortAcc in self.bots:
                self.bots[shortAcc].loadPluginsForChannel(channel['plugins'], channel['channel'])
                self.bots[shortAcc].joinChannel(channel['channel'])
            elif shortAcc not in self._failedBots:
                print("Channel '"+ channel +"' has invalid account")
    
    def run(self):
        for bot in self.bots:
            Thread(target=bot.run).start()
    
    def shouldRun(self):
        return self._shouldRun
