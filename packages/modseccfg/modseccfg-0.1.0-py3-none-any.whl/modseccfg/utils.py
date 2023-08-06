# encoding: utf-8
# api: python
# type: functions
# category: utils
# title:  Utils & Config
# description: various shortcut functions, config data, UI and remoting wrappers
# version: 0.3
# config:
#   { name: sshfs_mount, type: str, value: "~/.config/modseccfg/mnt/", description: "Remote connection (sshfs) mount point", help: "This will be used for `modseccfg vps123:` invocations to bind the servers / root locally." }
# state: alpha
#
# Monkeypatching some Python modules, and convenience wrappers


import sys
import os
import pathlib
import re
import functools
import subprocess
import atexit
try:
    import frosch
    frosch.hook()
except:
    pass


#-- path
def expandpath(dir):
    return str(pathlib.Path(dir).expanduser())


#-- @decorator to override module function
@functools.singledispatch
def inject(mod):
    def decorator(func):
        setattr(mod, func.__name__, func)
    return decorator
#-- patch re for \h support
@inject(re)
def compile(regex, *kargs, re_compile_orig=re.compile, **kwargs):
    if type(regex) is str:
        regex = re.sub(r'\\h(?![^\[]*\])', r'[\ \t\f]', regex)
        #print("re_compile: " + regex)
    return re_compile_orig(regex, *kargs, **kwargs)
@inject(re)
def grep(regex, list, flags=0):
    return [s for s in list if re.search(regex, s, flags)]


#-- remote/sshfs bindings
#
# This wraps any modseccfg file operations on config or log files.
# If modseccfg is started with a ssh:/ parameter, then we'll connect
# the remote file system. All file IO uses the mount prefix henceforth;
# thusly enabling remote log scans and config editing.
# (Because X11 forwarding with Python/Tkinter is unworkable at best.)
#
class remote:

    # initialize if argv[] contains any `(user@)hostname:/`
    def __init__(self, srv=[]):
        from modseccfg import appsettings
        if not srv:
            self.local = 1
            self.mnt = ""
            self.srv = self.srvname = ""
        else:
            self.local = 0
            self.srvname = re.sub(":.*?$", "", srv[0])
            self.srv = self.srvname + ":/"   # must be / root
            self.mnt = expandpath(appsettings.conf["sshfs_mount"]) + "/" + self.srv
            os.makedirs(self.mnt, 0o0700, True)
            sshfs_o = re.sub("(^\s*(?=\w)|-o\s*|[^\w=]+)", "-o ", appsettings.conf.get("sshfs_o", ""))
            os.system(f"sshfs {sshfs_o} {self.srv}/ {self.mnt}")
            atexit.register(self.umount)

    def umount(self):
        if self.mnt and self.srv:
            os.system("fusermount -u " + self.mnt)
            os.rmdir(self.mnt)

    def fn(self, fn):
        return self.mnt + fn

    def read(self, fn):
        if not self.exists(fn):
            if not re.search("letsencrypt|ssl", fn):
                print("WARNING: file not found", self.mnt, fn)
            return ""
        with open(self.fn(fn), "r", encoding="utf8") as f:
            return f.read()

    def write(self, fn, src):
        with open(self.fn(fn), "w", encoding="utf8") as f:
            return f.write(src)

    def popen(self, cmd, action="r"):
        if not self.local:
            cmd = ["ssh", self.srvname] + cmd
        if action=="r":
            return subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        else:
            return subprocess.Popen(cmd, stdin=subprocess.PIPE).stdin

    def exists(self, fn):
        return os.path.exists(self.fn(fn))

    def writable(self, fn):
        if self.local:
            return os.access(self.fn(fn), os.W_OK)
        else:
            return True  # need a real test here
    writeable=writable  # alias
            

# initialize with argv[]
srvroot = remote(re.grep("\w+:", sys.argv[1:]))
