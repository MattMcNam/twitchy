# Twitchy
# An IRC bot designed for Twitch.TV streams
# Matthew 'Blue' McNamara - matt@mattmcn.com
# 
# Please see the README for instructions on using Twitchy.
# It is released under the BSD license; the full license
# available in the LICENSE file.

# CONFIGURATION
Twitch_Username = 'Bot_Username' # Twitch.TV username for the bot, must be a registered username!
							## Note that this can be the same as your broadcasting account,
							## if people aren't paying attention to your bot

Twitch_Password = 'Bot_Password' # Password for above Twitch.TV account
Twitch_Channel = 'SpBlue' # Twitch.TV channel to connect to

# NOW DON'T TOUCH ANYTHING ELSE, UNLESS YOU KNOW WHAT YOU'RE DOING

# If you do want to improve the code, though, feel free.
# I'd like if you then made a pull request on GitHub for everyone to
# benefit from the improved code, but you aren't required to do so.

import socket
import time
import imp
import os
from time import sleep
import traceback
import re

class Twitchy:
	def __init__(self):
		self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ircServ = Twitch_Username +'.jtvirc.com'
		self.ircChan = '#'+ Twitch_Channel
		
		# Plugin system loosely based on blog post by lkjoel
		# http://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
		self._pluginFolder = './plugins/'
		self._mainModule = 'plugin'
		
		self.commands = []
	
	def sendMessage(self, message):
		self.ircSock.send("PRIVMSG " + self.ircChan + " :" + message + "\r\n")
	
	def connect(self, port):
		self.ircSock.connect((self.ircServ, port))
		self.ircSock.send("Pass " + Twitch_Password + "\r\n")
		self.ircSock.send("NICK " + Twitch_Username + "\r\n")
		self.ircSock.send("JOIN " + self.ircChan + "\r\n")
	
	def loadPlugins(self):
		plugins = []
		potentialPlugins = []
		allplugins = os.listdir(self._pluginFolder)
		for i in allplugins:
			location = os.path.join(self._pluginFolder, i)
			if not os.path.isdir(location) or not self._mainModule + ".py" in os.listdir(location):
				continue
			info = imp.find_module(self._mainModule, [location])
			potentialPlugins.append({"name": i, "info": info})
		
		for i in potentialPlugins:
			try:
				plugin = imp.load_module(self._mainModule, *i["info"])
				pluginInstance = plugin.getInstance(self)
				plugins.append(pluginInstance)
			except Exception as e:
				print "Error loading plugin."
				print traceback.format_exc()
	
	def registerCommand(self, command, pluginFunction):
		self.commands.append( {'regex': command, 'handler':pluginFunction} )
	
	def run(self):
		while True:
			fullIrcMsg = self.ircSock.recv(4096)	# Don't know JTVIRC's message size limit, if any,
											# but 4kb should be ok.
			ircMsgs = fullIrcMsg.split('\r\n')	# Sometimes multiple messages are received at once,
												# split them and handle individually.
			ircMsgs.pop() #remove final, empty entry
			
			ircMsg = ircMsgs[0]
			for message in ircMsgs:
				print "IRC:::: "+ message
			
			if ircMsg.find(' PRIVMSG '+ self.ircChan +' :') != -1:
				nick = ircMsg.split('!')[0][1:]
				msg = ircMsg.split(' PRIVMSG '+ self.ircChan +' :')[1]
				print nick+": "+msg
				
				for pluginDict in self.commands:
					if re.search('^'+pluginDict['regex'], msg, re.IGNORECASE):
						handler = pluginDict['handler']
						handler(nick, msg)
				#cmdParser.parse(nick, msg, sendMsg)
			
			elif ircMsg.find('PING ') != -1:
				self.ircSock.send('PING :pong\n')
			elif ircMsg.find('JOIN ') != -1:
				print ircMsg.split('!')[0][1:] +" joined chat"
			elif ircMsg.find('PART ') != -1:
				print ircMsg.split('!')[0][1:] +" left chat"
			elif ircMsg.find('MODE '+ self.ircChan +' +o') != -1:
				nick = ircMsg.split(' ')[-1]
				if nick.lower() != Twitch_Username.lower():
					print "Mod joined: "+nick
					#cmdParser.addMod(nick)
			elif ircMsg.find('MODE '+ self.ircChan +' -o') != -1:
				nick = ircMsg.split(' ')[-1]
				if nick.lower() != Twitch_Username.lower():
					print "Mod left: "+nick
					#cmdParser.addMod(nick)
			else:
				print ircMsg
	
	def callback(self):
		print "THE CALLOUT"

# 'main'
if __name__ == "__main__":
	twitchy = Twitchy()
	
	try:
		twitchy.loadPlugins()
		twitchy.connect(6667)
		twitchy.run()
	except Exception as e:
		print traceback.format_exc()
