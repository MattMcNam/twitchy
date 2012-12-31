twitchy
=======

An IRC bot designed for Twitch.TV channels.

Usage
-
Clone this repo, edit Twitch_Username, Twitch_Password and Twitch_Channel and run 'python twitchy.py'.
An example plugin is provided which responds to '!hello' and 'hey', as well as detecting users joining or leaving, or their moderator status changing.

Plugins
-
These are some quick notes on the plugin structure within Twitchy. Don't worry it's simpler than the length of the section would have you believe.

* Plugins must be in their own directory in the plugins folder, and must be * named plugin.py.  
* Plugin classes must be a subclass of BasePlugin, as shown in HelloPlugin.  
* Plugins _should_ call the super classes \_\_init__, though it is not strictly required.  
* Multiple plugins _can_ be defined in one file.  
* Additionally, only classes which are subclasses of BasePlugin are treated as plugins, allowing you to have multiple helper classes in the same file.

There is a very basic plugin 'API' with the following 4 functions:

1. self.registerCommand( *commandString*, *handlerFunction* )
-  self.registerTrigger( *triggerString*, *handlerFunction* )
-  self.registerForJoinPartNotifications( *handlerFunction* )
-  self.registerForModNotifications( *handlerFunction* )
-  self.sendMessage( *message* )

Their corresponding handlerFunctions should accept these arguments:

1. functionName( self, *nickname*, *message* ) *# full message is provided, may change to an argument list in future*
-  functionName( self, *nickname*, *message* ) *# full message provided*
-  functionName( self, *nickname*, *isJoining* ) *# isJoining; true is joining, false if parting*
-  functionName( self, *nickname*, *receivingModStatus* ) *# receivingModStatus; true when receiving, false when losing*

**However**, plugins are not limited to these commands. plugins can access any part of Twitchy.py via the self.twitchy object.
Basically, these commands are for convenience, you are free to write plugins that do anything you want.

Example plugins will be uploaded soon to a separate repository, though HelloPlugin should show you the boilerplate code needed to get started.

License
-
Twitchy is provided under the BSD License. It is available in full in LICENSE.md

Created by
-
Matthew 'Blue' McNamara  
matt@mattmcn.com
