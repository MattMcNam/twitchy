'''
Bot.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

from threading import Thread
import imp, inspect, socket, traceback, re
import PluginManager
from plugins.BasePlugin import BasePlugin

class Bot:
    '''
    classdocs
    '''


    def __init__(self, username, password):
        '''
        Constructor
        '''
        self._username = username
        self._password = password
        self.channel = ""
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False
        self._pluginFolder = './plugins/'
        self._plugins = []
        self._pluginNames  = []
        
        self._commands = []
        self._triggers = []
        self._joinParthandlers = []
        self._modHandlers = []
    
    def connect(self):
        self._socket.connect(("irc.twitch.tv", 6667))
        self._socket.send("Pass "+ self._password +"\r\n")
        self._socket.send("NICK "+ self._username +"\r\n")
        self._connected = True
    
    def isConnected(self):
        return self._connected
    
    def loadPluginsForChannel(self, plugins, channel):
        foundPlugins = PluginManager.getPluginsWithNames(plugins)
        for i in foundPlugins:
            try:
                plugin = imp.load_module('plugin', *i['info'])
                pluginClasses = inspect.getmembers(plugin, inspect.isclass)
                for className, classObj in pluginClasses:
                    if (className == 'BasePlugin' or className in self._pluginNames
                        or not issubclass(classObj, BasePlugin)):
                        continue # Exclude BasePlugin & classes that are not a subclass of it
                    pluginInstance = classObj(self)
                    self._plugins.append(pluginInstance)
                    self._pluginNames.append(className)
            except:
                print('Error loading plugin'+ i['name'] +', printing traceback:')
                print(traceback.format_exc())
    
    def registerCommand(self, command, handler):
        self._commands.append({'regex': command, 'handler': handler})
    
    def registerTrigger(self, trigger, handler):
        self._triggers.append({'regex': trigger, 'handler': handler})
    
    def registerForJoinPartNotifications(self, handler):
        self._joinParthandlers.append(handler)
    
    def registerForModNotifications(self, handler):
        self._modHandlers.append(handler)
    
    def joinChannel(self, chan):
        self._socket.send("JOIN #"+ chan +"\r\n")
        self.channel = chan
    
    def run(self):
        while True:
            fullIRCMsg = self._socket.recv(4096).decode('UTF-8')
            
            ircMsgs = fullIRCMsg.split('\r\n')
            ircMsgs.pop()
            
            for msg in ircMsgs:
                Thread(target=self._handleMessage, args=(msg,)).start()
    
    def _handleMessage(self, message):
        if message.find(' PRIVMSG #'+ self._channel +' :') != -1:
            nick = message.split('!')[0][1:]
            msg = message.split(' PRIVMSG #'+ self._channel +' :')[1]

            for pluginDict in self._commands:
                if re.search('^!'+pluginDict['regex'], msg, re.IGNORECASE):
                    handler = pluginDict['handler']
                    handler(nick, msg)

            for pluginDict in self._triggers:
                if re.search('^'+pluginDict['regex'], msg, re.IGNORECASE):
                    handler = pluginDict['handler']
                    handler(nick, msg)
        
        elif message.find('JOIN ') != -1:
            nick = message.split('!')[0][1:]
            #print(nick +" joined chat")
            for handler in self._joinPartHandlers:
                handler(nick, True)
        
        elif message.find('PART ') != -1:
            nick = message.split('!')[0][1:]
            #print(nick +" left chat")
            for handler in self._joinPartHandlers:
                handler(nick, False)
        
        elif message.find('MODE #'+ self._channel +' +o') != -1:
            nick = message.split(' ')[-1]
            if nick.lower() != self._username.lower():
                #print("Mod joined: "+nick)
                for handler in self._modHandlers:
                    handler(nick, True)
        
        elif message.find('MODE #'+ self._channel +' -o') != -1:
            nick = message.split(' ')[-1]
            if nick.lower() != self._username.lower():
                #print("Mod left: "+nick)
                for handler in self._modHandlers:
                    handler(nick, False)
        
        elif message.find('PING ') != -1:
            self._socket.send('PING :pong\r\n')
    