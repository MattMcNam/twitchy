'''
Bot.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

from private import ConfigObj

class Bot:
    '''
    The main class that powers Twitchy.
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.accounts = []
        self.config = None
        
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
