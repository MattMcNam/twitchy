from plugins.BasePlugin import BasePlugin

class HelloPlugin(BasePlugin):
	def __init__(self, twitchy):
		super(HelloPlugin, self).__init__(twitchy)
		
		self.registerCommand('hello', self.helloHandler) # respond when '!hello' is at beginning of message
		#self.registerTrigger('hi', self.hiHandler) # respond when 'hi' is anywhere in message
	
	def helloHandler(self, nick, commandArg):
		self.twitchy.sendMessage("Hello "+ nick +"!")
	
	def hiHandler(self, nick, fullMsg):
		self.twitchy.sendMessage("Hi there, "+nick)
