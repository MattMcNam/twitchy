'''
Bot.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

import socket
from threading import Thread
import os
import imp

class Bot:
    '''
    classdocs
    '''


    def __init__(self, username, password):
        '''
        Constructor
        '''
        self.username = username
        self.password = password
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False
        self._pluginFolder = './plugins/'
    
    def connect(self):
        self._socket.connect(("irc.twitch.tv", 6667))
        self._socket.send("Pass "+ self.password +"\r\n")
        self._socket.send("NICK "+ self.username +"\r\n")
        self._connected = True
    
    def isConnected(self):
        return self._connected
    
    def loadPluginsForChannel(self, plugins, channel):
        plugins = []
        potentialPlugins = []
        allPlugins = os.listDir(self._pluginFolder)
        for i in allPlugins:
            loc = os.path.join(self._pluginFolder, i)
            if not os.path.isdir(loc) or not 'plugin.py' in os.listDir(loc):
                continue
            info = imp.find_module('plugin', [loc])
    
    def joinChannel(self, chan):
        self._socket.send("JOIN #"+ chan +"\r\n")
    
    def run(self):
        while True:
            fullIRCMsg = self._socket.recv(4096).decode('UTF-8')
            
            ircMsgs = fullIRCMsg.split('\r\n')
            ircMsgs.pop()
            
            for msg in ircMsgs:
                Thread(target=self._handleMessage, args=(msg,)).start()
    
    def _handleMessage(self, message):
        
    