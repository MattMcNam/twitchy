''''
PluginManager.py
Twitchy project

Copyright (c) 2013 Matthew McNamara
BSD 2-Clause License
http://opensource.org/licenses/BSD-2-Clause
'''

import imp, os

_foundPlugins = []
_pluginsFolder = './plugins/'

def _loadPlugins():
    plugins = os.listdir(_pluginsFolder)
    for i in plugins:
        loc = os.path.join(_pluginsFolder, i)
        if not os.path.isdir(loc) or not 'plugin.py' in os.listdir(loc):
            continue
        info = imp.find_module('plugin', [loc])
        _foundPlugins.append({'name': i, 'info': info})
    
def getPluginsWithNames(names):
    p = []
    for i in _foundPlugins:
        if i['name'] in names:
            p.append(i)
    return p