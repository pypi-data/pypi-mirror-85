# encoding: utf-8
# api: modseccfg
# title: Writer
# description: updates *.conf files with new directives
# version: 0.1
# type: file
# category: config
# config:
#     { name: write_etc, type: bool, value: 0, description: "Write to /etc without extra warnings", help: "Normally modseccfg would not update default apache/modsecurity config files." }
#     { name: write_sudo, type: bool, value: 0, description: "Use sudo to update non-writable files", help: "Run `sudo` on commandline to update files, if permissions insufficient" }
# state: alpha
#
# Reads, updates and then writes back configuration files.
# Contains multiple functions for different directives.
# Some need replacing, while others (lists) just need to be
# appended.
# 


import os, re
from modseccfg import vhosts, appsettings, utils
import PySimpleGUI as sg


class rx:
    pfx = re.compile("""
        ^(\s*)\w+
    """, re.M)
    end = re.compile("""
        \Z | ^\s*</VirtualHost>
    """, re.M)


# read src from config file
def read(fn):
    return open(fn, "r", encoding="utf8").read()

# update file
def write(fn, src):
    if not appsettings.conf["write_etc"] and re.search("^/etc/|^/usr/share/", fn):# and not re.search("/sites|/crs-setup.conf", fn):
        # alternatively check for `#editable:1` header with pluginconf
        if sg.popup_yes_no("Default Apache/mod_sec config file '{}' should not be updated. Proceed anyway?".format(fn)) != "Yes":
            return
    if not os.access(fn, os.W_OK):
        sg.popup_cancel("Config file '{}' isn't writeable. (Use chown/chmod to make it so.)".format(fn))
        # elif appsettings.conf["write_sudo"]: write_sudo(fn, src)
        return
    open(fn, "w", encoding="utf8").write(src)

# write to file via sudo/tee pipe instead
def write_sudo(fn, src):
    p = subprocess.Popen(['sudo', 'tee'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(src.encode("utf-8"))
    p.stdin.close()
    print(p.stdout.read())
    p.wait()

# detect leading whitespace
def pfx(src):
    space = rx.pfx.findall(src)
    if space:
        return space[0]
    else:
        return ""

# updates `src` on existing occurence of directive, else appends
def augment(src, directive, value):
    pass

# doesn't look for context
def append(fn, directive, value):
    src = read(fn)
    src = rx.end.sub("{} {}".format(directive, value), src)
    write(fn, src)


