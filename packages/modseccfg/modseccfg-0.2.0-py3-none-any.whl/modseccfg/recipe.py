# api: modseccfg
# encoding: utf-8
# version: 0.0
# type: data
# title: recipe
# description: Apache/mod_security config examples or conversions
# category: config
# config:
#    { name: replace_rules, type: bool, value: 0, description: "try to find replacement spot, else just append" }
#
# Basically just blobs of text and an editor window.
# [Save] will append directives to selected vhost/*.conf file.
#


from modseccfg import utils, vhosts
import PySimpleGUI as sg
import re
from textwrap import dedent



class recipe:

    location = """
      <Location "/app/">
        SecRuleRemoveById $id   #@wrap
      </Location>
    """

    directory = """
      <Directory "/srv/www/app/">
        SecRuleRemoveById $id   #@wrap
      </Directory>
    """

    filesmatch = """
      <FilesMatch "*.php">
        SecRuleRemoveById $id   #@wrap
      </FilesMatch>
    """
    
    exclude_parameter = """
       SecRuleUpdateTargetByID $id "!ARGS:param"
    """
    
    macros = """
    <IfModule mod_alias.c>
      <Macro SecRuleRemoveByPath $id $path>
        SecRule REQUEST_URI "@eq $path" "id:%{md5:$id-$path},t:none,msg:'Whitelist $path',ctl:removeById=$id"
      </Macro>
    </IfModule>
    """

    @staticmethod
    def has(name):
        return hasattr(recipe, name)

    @staticmethod
    def show(name, data, id=0, vhost={}):
    
        # resolve
        text = getattr(recipe, name)
        if type(text) is str:
            text = dedent(text)
            if re.search(r"\$(id|path|tag)", text):
                if data.get("rule"):
                    text =  re.sub(r"\$id", str(data["rule"][0]), text)
                #@ToDo: mainwindow should supply a data bag (either full secrule entry, or params from log - depending on which is active)
        else:
            text = text(data)
        print(data)
        print(text)
    
        # window
        w = sg.Window(title=f"Recipe '{name}'", layout=[
            [sg.Multiline(default_text=text, key="src", size=(80,20), font="Sans 14")],
            [sg.Button("Save", key="save"), sg.Button("Cancel", key="cancel")]
        ])
        event, values = w.read()
        print(event, values)
        w.close()
        
        # write …
        if event == "save":
            writer.append(vhost.fn, text)

