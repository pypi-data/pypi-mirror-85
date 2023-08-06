# encoding: utf-8
# api: modseccfg
# title: Writer
# description: updates *.conf files with new directives
# version: 0.3
# type: file
# category: config
# config:
#     { name: write_etc, type: bool, value: 0, description: "Write to /etc without extra warnings", help: "Normally modseccfg would not update default apache/modsecurity config files." }
#     { name: write_sudo, type: bool, value: 0, description: "Use sudo to update non-writable files", help: "Run `sudo` on commandline to update files, if permissions insufficient" }
#     { name: backup_files, value: 1, type: bool, description: "Copy files to ~/backup-config/ before rewriting" }
#     { name: backup_dir, value: "~/backup-config/", type: str, description: "Where to store copies of configuration files" }
# state: alpha
#
# Reads, updates and then writes back configuration files.
# Contains multiple functions for different directives.
# Some need replacing, while others (lists) just need to be
# appended.
# 


import os, re, time, shutil
from modseccfg import vhosts, appsettings, utils
from modseccfg.utils import srvroot
import PySimpleGUI as sg


class rx:
    pfx = re.compile("""
        ^(\s*)\w+
    """, re.X|re.M)
    end = re.compile(r"""
        ^\s*</VirtualHost> | \Z
    """, re.X|re.M)


# read src from config file
def read(fn):
    return srvroot.read(fn)

# update file
def write(fn, src):
    if not appsettings.conf["write_etc"] and re.search("^/etc/|^/usr/share/", fn):# and not re.search("/sites|/crs-setup.conf", fn):
        # alternatively check for `#editable:1` header with pluginconf
        if sg.popup_yes_no(f"Default Apache/mod_sec config file '{fn}' should not be updated. Proceed anyway?") != "Yes":
            return
    if not srvroot.writable(fn):
        sg.popup_cancel(f"Config file '{fn}' isn't writeable. (Use chown/chmod to make it so.)")
        # elif appsettings.conf["write_sudo"]: write_sudo(fn, src)
        return
    # save a copy before doing anything else
    if appsettings.conf.get("backup_files"):
        backup(fn)
    # actually write
    srvroot.write(fn, src)

def backup(fn):
    dir = utils.expandpath(appsettings.conf["backup_dir"])
    os.makedirs(dir, 0o751, True)
    dest = re.sub("[^\w\.\-\+\,]", "_", fn)
    dest = f"{dir}/{time.time()}.{dest}"
    shutil.copyfile(srvroot.fn(fn), dest)

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
def append(fn, directive, value, comment=""):
    src = read(fn)
    insert = f"{pfx(src)}{directive} {value}   {comment}\n" #.format(pfx(src), directive, value, comment)
    if src == rx.end.sub(insert, src):
        print("NOTHING CHANGED FOR APPEND()")
    src = rx.end.sub(insert, src)
    write(fn, src)

# strip SecRuleRemoveById …? nnnnnnn …?
def remove_remove(fn, directive, value):
    pass
