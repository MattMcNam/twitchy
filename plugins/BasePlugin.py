class BasePlugin(object):
	def __init__(self, twitchy):
		self.twitchy = twitchy

	def registerCommand(self, command, handler):
		self.twitchy.registerCommand(command, handler)
