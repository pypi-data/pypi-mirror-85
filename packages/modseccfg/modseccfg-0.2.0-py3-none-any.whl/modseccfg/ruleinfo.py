# encoding: utf8
# api: modseccfg
# type: function
# category: gui
# title: Rule Info
# description: displays details (params/flags) of mod_security rule
# version: 0.2
# config:
#    { name: info_log_count, type: int, value: 7, description: Number of log entries to show. }
#
# Brings up a text window to visualise SecRule flags and options.
# Highlights some interesting flags, and appends recent log entries
# about the rule when available.
#


import re, json
from modseccfg import utils, vhosts, icons
from modseccfg.utils import conf
import PySimpleGUI as sg


def show(id, log_values=None):

    # display options
    class m(dict):
        head = dict(font=("Ubuntu", 20, "bold"))
        sect = dict(font=("Ubuntu", 13, "bold"))
        msg = dict(font=("Ubuntu", 14, "italic"), pad=(50,0))
        grp = dict(font=("Sans", 12, "italic"), pad=(50,0))
        val = dict(font=("Sans", 11, "italic"), pad=(50,0))
        desc = dict(text_color="gray")
        phase = dict(background_color="yellow")
        block = dict(background_color="orange")
        deny = dict(background_color="red")
        audit = dict(background_color="lightgray")
        chain = dict(text_color="magenta")
        capture = dict(background_color="darkgray")
        severity = dict(background_color="#ffccbb")
    setattr(m, "pass", dict(background_color="lightgreen"))
    def m_(v, alt={}):
        return m.__dict__.get(v, alt)
    # flag documentation
    desc = {
        "pass": "No action, not blocking request yet",
        "deny": "Quit request with error 40x",
        "block": "Quit request with error 50x",
        "t:none": "No transformation on input vars",
        "phase:1": "Request header checks",
        "phase:2": "Request body inspection",
        "phase:3": "Response headers",
        "phase:4": "Response body",
        "phase:5": "Logging"
    }

    # params 2 widget
    r = vhosts.rules[id]
    layout = [
        [sg.T(f"SecRule {id}", **m.head)],
        [sg.Frame("doc", layout=[[sg.Multiline(r.help(), auto_size_text=1, size=(60,4), background_color="lightgray")]], size=(90,4))],
    ]
    for key in "msg", "vars", "pattern":
        layout.append([sg.T(key, **m.sect), sg.T(getattr(r, key), **m_(key, m.val))])
    for key in "flags", "params", "ctl", "setvar", "tags":
        grp = getattr(r, key)
        if not grp:
            continue
        layout.append([sg.T(key, **m.sect)])
        if type(grp) is list:
            for v in grp:
                layout.append([
                    sg.T(v, **m.grp, **m_(v)),
                    sg.T(desc.get(v,""), **m.desc)
                ])
        elif type(grp) is dict:
            for k,v in grp.items():
                layout.append([
                    sg.T(k, **m.grp),
                    sg.T(v, **m_(k)),
                    sg.T(desc.get(f"{k}:{v}",""), **m.desc)
                ])
    
    # logs
    if log_values and conf.get("info_log_count"):
        layout.append([sg.Frame(title="recent log entries", pad=(10,25),
            layout=[[sg.Multiline(
                default_text="\n----------\n".join(
                    re.grep(fr"\b{id}\b", log_values())[ -conf["info_log_count"]: ]
                ),
                size=(60,12)
            )]]
        )])

    # as json?
    #layout.append(  [sg.T(json.dumps(r.__dict__, indent=4))]  )

    # finalize window
    layout = [
        [sg.Menu([["Rule",["Close"]]])],
        [sg.Column(layout, expand_x=1, expand_y=0, size=(675,820), scrollable="vertically", element_justification='left')]
    ]
    return sg.Window(layout=layout, title=f"SecRule #{id}", resizable=1, font="Sans 12", icon=icons.icon)
    
    #w.read()
    #w.close()

