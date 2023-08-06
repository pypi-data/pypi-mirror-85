# api: modseccfg
# encoding: utf-8
# type: file
# category: log
# title: log reader
# description: scan error.logs / audit log
# config:
#    { name: log_entries, type: int, value: 5000, description: "How many log entries to show (whole log will be counted regardless)" }
#    { name: log_filter, type: str, value: "(?!404|429)4\d\d|5\d\d", description: "Error codes to look out for in access.logs" }
#    { name: log_skip_rx, type: str, value: "PetalBot|/.well-known/ignore.cgi", description: "Regex to skip whole log lines on" }
#    { name: log_search_id, type: bool, value: 0, description: "Look up rule id, if only file+line given in log (slow)" }
# version: 0.1
#
# Basic filtering and searching within the logs.
# Filters out by error codes (http 4xx/5xx) or mod_security messages.
#
# Audit log types (serial/concurrent/json) aren't supported yet.
#


import os, re
from modseccfg import utils, vhosts, data
from modseccfg.utils import srvroot, conf


# detected rule ids and number of occurences
log_count = {}     # id→count
class state:
    log_curr = ""  # fn


# extraction rules
class rx:
    interesting = re.compile("""
        ModSecurity: |
        \[id\s"\d+"\] |
        "\s((?!429)[45]\d\d)\s\d+        # should come from conf[log_filter]
    """, re.X)
    id = re.compile("""
        (?:\[id\s|\{"id":\s*)"(\d+)"[\]\}]   # [id "…"] or json {"id":"…"}
    """, re.X)
    file_line = re.compile("""
        \[file \s "(?P<file>.+?)"\] \s* \[line \s "(?P<line>\d+)"\]
    """, re.X)
    shorten = re.compile("""
        :\d\d.\d+(?=\]) |
        \s\[pid\s\d[^\]]*\] |
        \s\[tag\s"[\w\-\.\/]+"\] |
        \s\[client\s[\d\.:]+\] |
        \sRule\s[0-9a-f]{12} |
        (?<=\[file\s")/usr/share/modsecurity-crs/rules/ |
    """, re.X)


# search through log file, filter, extract rule ids, return list of log lines
def scan_log(fn):

    if fn == state.log_curr:
        return   # no update
    state.log_curr = ""
    if not srvroot.exists(fn):
        return
    log_curr = fn
    
    # filter lines
    log_lines = []
    with open(srvroot.fn(fn), "r", encoding="utf8") as f:
        #print(fn, f)
        for line in f:
            if rx.interesting.search(line):
                if re.search(conf["log_skip_rx"], line):
                    continue
                m = rx.id.search(line)
                if m:
                    incr_log_count(int(m.group(1)))
                elif conf["log_search_id"]:
                    m = rx.file_line.search(line)
                    if m:
                        id = search_id(m.group("file"), m.group("line"))
                        if id:
                            incr_log_count(int(id))
                log_lines.append(line.strip())

    # slice entries
    if len(log_lines) >= conf["log_entries"]:
        log_lines = log_lines[-conf["log_entries"]:]
    # shorten infos in line
    log_lines = [rx.shorten.sub("", line) for line in log_lines]
    return log_lines

# count++
def incr_log_count(id):
    if id in log_count:
        log_count[id] += 1
    else:
        log_count[id] = 1

# search [id …] from only [file …] and [line …] - using vhosts.linemap{}
def search_id(file, line):
    print("linemap:", file, line)
    if file and line:
        vh = vhosts.vhosts.get(file)
        if vh:
            return vh.line_to_id(int(line))
    return 0


# assemble list of error/access/audit logs
def find_logs():
    log_list = []
    for fn,vh in vhosts.vhosts.items():
        log_list = log_list + vh.logs
    #log_list.append("./fossil.error.log")  # testing
    if conf.get("add_stub_logs"):
        add = [data.dir+"/common_false_positives.log"]
    else:
        add = []
    return list(set(log_list)) + add

