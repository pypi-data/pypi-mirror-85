# api: python
# type: io
# title: app settings
# description: read/store modseccfg options
# depends: pluginconf (>= 0.7.2), python:appdirs (>= 1.3), python:pathlib
# category: config
# version: 0.1
# config:
#    { name: "test[key]", type: bool, value: 1, description: "Array[key] test" }
# 
# Basically just a dictionary for the GUI and some
# module behaviours. GUI courtesy of pluginconf.
#


import json, os
from modseccfg.utils import expandpath
import pluginconf, pluginconf.gui
#import appdirs

# defaults
conf = {
    "theme": "DarkGrey",
    "edit_sys_files": False,
    "backup_files": True,
    "log_entries": 5000,
    "log_filter": "(?!404|429)[45]\d\d",
    "log_skip_rx" : "PetalBot|/.well-known/ignore.cgi",
    "max_rule_range": 1000,  # obsolete already (SecRuleDisById ranges do a lookup)
    "backup_dir": expandpath("~/backup-config/"),
    "conf_file": expandpath("~/.config/modseccfg.json")
}

# plugin lookup
pluginconf.module_base=__name__
pluginconf.plugin_base=["modseccfg"]
for module,meta in pluginconf.all_plugin_meta().items():
    pluginconf.add_plugin_defaults(conf, {}, meta, module)
#print(__package__)
#print(pluginconf.module_list())
#print(conf)

# read config file
def read():
    if os.path.exists(conf["conf_file"]):
        conf.update(json.load(open(conf["conf_file"], "r")))

# write config file
def write():
    if not os.path.exists(os.path.dirname(conf["conf_file"])):
        os.mkdir(os.path.dirname(conf["conf_file"]))
    print(str(conf))
    json.dump(conf, open(conf["conf_file"], "w"), indent=4)

# show config option dialog
def window(mainself, *kargs):
    pluginstates = {"mainwindow": 1, "__init__":1,"appsettings":1,"vhosts":1,"logs":1,"writer":1}
    fn_py = __file__.replace("appsettings", "*")
    save = pluginconf.gui.window(conf, pluginstates, files=[fn_py], theme=conf["theme"])
    if save:
        write()

# initialze conf{}
read()
