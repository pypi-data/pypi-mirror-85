# api: modseccfg
# encoding: utf-8
# title: *.conf scanner
# description: Compiles a list of relevant apache/vhost files and Sec* settings
# type: tokenizer
# category: apache
# version: 0.5
# config:
#    { name: envvars, value: "/etc/default/apache2", type: str, description: "Look up APACHE_ENV vars from shell script", help: "Mostly applies to Debian derivates. Other distros usually embed SetEnv directives for log paths." }
# license: ASL
#
# Runs once to scan for an vhost* and mod_security config files.
# Uses `apache2ctl -t -D DUMP_INCLUDES` to find all includes,
# and regexes for Sec*Rules or *Log locations and ServerNames.
#
# This should yield any mod_security and vhost-relevant sections.
# The list is kept in `vhosts`. And secrule declarations+options
# in `rules`.
#
# Extraction is fairly simplistic, but for this purpose we don't
# need an exact representation nor nested structures. The UI will
# present vhost/conf files rather than <VirtualHost> sections.
# (We shouldn't penalize the average user for random edge cases.)
# 
# Notably this will not work with mod_security v3, since the
# SecRules/Flags have been moved into matryoshka directives and
# external *.conf files (but no JSON rulesets for some reason).
# Still doable, but not a priority right now. Same for nginx.
#


import os, re, sys
import subprocess
import traceback
from pprint import pprint
from modseccfg.utils import srvroot


# collected config/vhost sections
vhosts = {
    # fn → vhost:
           # .fn .t .name .logs[] .cfg{} .rulestate{} .ruledecl{} .linemap{}
}
# and SecRules (we don't actually use all extracted details)
rules = {
    # id → secrule:
           #  .id .chained_to .msg .flags{} .params{} .tags[] .tag_primary .ctl{} .setvar{} .vars .pattern
}


# extraction patterns
class rx:
    dump_includes = re.compile("^\s*\([\d*]+\)\s+(.+)$", re.M)
    # directives we care about
    interesting = re.compile(
        "^ \s* (ErrorLog | CustomLog | Server(Name|Alias) | (Virtual)?DocumentRoot | Sec\w* | Use\sSec\w+ | modsecurity\w* ) \\b",
        re.M|re.I|re.X
    )
    # extract directive line including line continuations (<\><NL>)
    configline = re.compile(
        """ ^
        [\ \\t]*                          # whitespace \h*
        # (?:Use \s{1,4})?                  # optional: `Use␣` to find custom macros like `Use SecRuleRemoveByPath…`
        (\w+)                             # alphanumeric directive 
          [\ \\t]+                        # whitespace \h+
        (
          (?: [^\\n\\\\]+ | [\\\\]. )*    # literals, or backslash + anything
        )
        $ """,
        re.M|re.S|re.X
    )
    # to strip <\><NL>
    escnewline = re.compile(
        """[\\\\][\\n]\s*"""              # escaped linkebreaks
    )
    # handle quoted/unquoted directive arguments (not entirely sure if Apache does \" escaped quotes within)
    split_args = re.compile(
        """
        (?:\s+)   |                       # skip whitespace (\K not supported in python re, so removing empty matches in postprocessing)
        \#.*$  |                          # skip trailing comment (which isn't technically allowed, but)
        " ((?:[^\\\\"]+|\\\\ .)+) "  |    # quoted arguments
        (?!\#) ([^"\s]+)                  # plain arguments (no quotes, no spaces)
        """,
        re.X
    )
    # SecRule … … `actions:argument,…`
    actions = re.compile(
        """
        (?: (t|pfx) :)? (\w+)             # action
        (?:
            :                             # : value…
            ([^,']+)     |                # bareword
            :
            ' ([^']+) '                   # ' quoted '
        )?
        """,
        re.X
    )
    # line number scan: roughly look for id:123456 occurences
    id_num = re.compile(
        "id:(\d+)"                        # without context
    )
    # comment lookup, directly preceeding id, uncompiled 
    rule_comment = """
        ( (?:^\#.*\\n | ^\s*\\n)+ )       # consecutive comment lines
        (?: ^(?!\#).*\\n  )*              # non-comment lines
        .*?  id:{}                        # id:nnnnn, requires rx.format(id)
    """
    # envvars
    shell_vars = re.compile("""
        ^\s* (?:export\s+)?  ([A-Z_]+)  =  ["']?  ([\w/\-.]+)  ["']?
    """, re.M|re.X)
    

# temporary state variables
class tmp:
    last_rule_id = 0

    tag_prio = ['event-correlation', 'anomaly-evaluation', 'OWASP_CRS/LEAKAGE/ERRORS_IIS', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_PHP', 'OWASP_CRS/LEAKAGE/ERRORS_PHP', 'OWASP_CRS/LEAKAGE/ERRORS_JAVA', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_JAVA', 'platform-sybase', 'platform-sqlite', 'platform-pgsql', 'platform-mysql', 'platform-mssql', 'platform-maxdb', 'platform-interbase', 'platform-ingres', 'platform-informix', 'platform-hsqldb', 'platform-frontbase', 'platform-firebird', 'platform-emc',
    'platform-db2', 'platform-oracle', 'CWE-209', 'OWASP_CRS/LEAKAGE/ERRORS_SQL', 'platform-msaccess', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_CGI', 'PCI/6.5.6', 'WASCTC/WASC-13', 'OWASP_CRS/LEAKAGE/INFO_DIRECTORY_LISTING', 'attack-disclosure', 'OWASP_CRS/WEB_ATTACK/JAVA_INJECTION', 'language-java', 'CAPEC-61', 'WASCTC/WASC-37', 'OWASP_CRS/WEB_ATTACK/SESSION_FIXATION', 'attack-fixation', 'OWASP_AppSensor/CIE1', 'WASCTC/WASC-19', 'OWASP_CRS/WEB_ATTACK/SQL_INJECTION', 'attack-sqli',
    'PCI/6.5.1', 'OWASP_TOP_10/A2', 'CAPEC-63', 'platform-internet-explorer', 'platform-tomcat', 'CAPEC-242', 'OWASP_AppSensor/IE1', 'OWASP_TOP_10/A3', 'WASCTC/WASC-22', 'WASCTC/WASC-8', 'OWASP_CRS/WEB_ATTACK/XSS', 'attack-xss', 'OWASP_CRS/WEB_ATTACK/NODEJS_INJECTION', 'attack-injection-nodejs', 'language-javascript', 'OWASP_CRS/WEB_ATTACK/PHP_INJECTION', 'attack-injection-php', 'language-php', 'language-powershell', 'PCI/6.5.2', 'WASCTC/WASC-31',
    'OWASP_CRS/WEB_ATTACK/COMMAND_INJECTION', 'attack-rce', 'platform-unix', 'language-shell', 'OWASP_CRS/WEB_ATTACK/RFI', 'attack-rfi', 'PCI/6.5.4', 'OWASP_TOP_10/A4', 'WASCTC/WASC-33', 'OWASP_CRS/WEB_ATTACK/FILE_INJECTION', 'OWASP_CRS/WEB_ATTACK/DIR_TRAVERSAL', 'attack-lfi', 'OWASP_CRS/WEB_ATTACK/HTTP_PARAMETER_POLLUTION', 'CAPEC-460', 'OWASP_CRS/WEB_ATTACK/HEADER_INJECTION', 'OWASP_CRS/WEB_ATTACK/RESPONSE_SPLITTING', 'OWASP_CRS/WEB_ATTACK/REQUEST_SMUGGLING',
    'paranoia-level/4', 'language-aspnet', 'paranoia-level/3', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_UA', 'OWASP_CRS/POLICY/HEADER_RESTRICTED', 'OWASP_CRS/POLICY/EXT_RESTRICTED', 'OWASP_CRS/POLICY/PROTOCOL_NOT_ALLOWED', 'OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE_CHARSET', 'OWASP_CRS/POLICY/CONTENT_TYPE_NOT_ALLOWED', 'OWASP_AppSensor/EE2', 'OWASP_TOP_10/A1', 'WASCTC/WASC-20', 'OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE', 'OWASP_CRS/POLICY/SIZE_LIMIT',
    'OWASP_CRS/PROTOCOL_VIOLATION/IP_HOST', 'OWASP_CRS/PROTOCOL_VIOLATION/EMPTY_HEADER_UA', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_ACCEPT', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_HOST', 'platform-windows', 'platform-iis', 'OWASP_CRS/PROTOCOL_VIOLATION/EVASION', 'OWASP_CRS/PROTOCOL_VIOLATION/INVALID_HREQ', 'CAPEC-272', 'OWASP_CRS/PROTOCOL_VIOLATION/INVALID_REQ', 'attack-protocol', 'OWASP_CRS/AUTOMATION/CRAWLER', 'attack-reputation-crawler',
    'OWASP_CRS/AUTOMATION/SCRIPTING', 'attack-reputation-scripting', 'PCI/6.5.10', 'OWASP_TOP_10/A7', 'WASCTC/WASC-21', 'OWASP_CRS/AUTOMATION/SECURITY_SCANNER', 'attack-reputation-scanner', 'paranoia-level/2', 'attack-dos', 'PCI/12.1', 'OWASP_AppSensor/RE1', 'OWASP_TOP_10/A6', 'WASCTC/WASC-15', 'OWASP_CRS/POLICY/METHOD_NOT_ALLOWED', 'OWASP_CRS', 'IP_REPUTATION/MALICIOUS_CLIENT', 'attack-reputation-ip', 'platform-multi', 'attack-generic', 'platform-apache', 'language-multi',
    'application-multi', 'paranoia-level/1']

    env = {
        "APACHE_LOG_DIR": "/var/log/apache2"  #/var/log/httpd/
    }
    env_locations = [
        "/etc/apache2/envvars", "/etc/default/httpd"
    ]


# encapsulate properties of config file (either vhosts, SecCfg*, or secrule collections)
class vhost:
    """
        Represents a config/vhost or mod_security rules file.
        
        Parameters
        ----------
        fn : str
            *.conf filename
        src : str
            config file source
        
        Attributes
        ----------
        fn : str
                filename
        t : str
                *.conf type (one of 'rules', 'vhost', 'cfg')
        name : str
                ServerName
        logs : list
                List of error/access.log filenames
        cfg : dict
                SecOption directives
        rulestate : dict
                SecRuleRemove* states (id→0)
        ruledecl : dict
                Map contained SecRules id into vhosts.rules{}
        linemap : dict
                Line number → RuleID (for looking up chained rules in error.log)
    """

    # split *.conf directives, dispatch onto assignment/extract methods
    def __init__(self, fn, src):

        # vhost properties
        self.fn = fn
        self.t = "cfg"
        self.name = ""
        self.logs = []
        self.cfg = {}
        self.rulestate = {}
        self.ruledecl = {}
        self.linemap = {} 
        self.mk_linemap(src)   # fill .linemap{}
        
        # extract directive lines
        for dir,args  in rx.configline.findall(src):    # or .finditer()? to record positions right away?
            dir = dir.lower()
            #print(dir, args)
            if hasattr(self, dir):
                # src.find(…) + str position to linecounter... / or do a separate line indexer scan (tx.msg:… -> id:…)
                func = getattr(self, dir)
                func(self.split_args(args))
            elif dir.startswith("sec"):
                self.cfg[dir] = args
        # determine config file type
        if self.name:
            self.t = "vhost"
        elif len(self.rulestate) >= 5:
            self.t = "cfg"
        elif len(self.ruledecl) >= 5:
            self.t = "rules"

    # strip \\ \n line continuations, split all "args"
    def split_args(self, args):
        args = re.sub(rx.escnewline, " ", args)
        args = rx.split_args.findall(args)
        args = [s[1] or s[0] for s in args]
        args = [s for s in args if len(s)]
        #args = [s.decode("unicode_escape") for s in args]   # don't strip backslashes
        return args
    # apply ${ENV} vars
    def var_sub(self, s):
        return re.sub('\$\{(\w+)\}', lambda m: tmp.env.get(m.group(1), ""), s)

    # apache: log directives
    def errorlog(self, args):
        self.logs.append(self.var_sub(args[0]))
    def customlog(self, args):
        self.logs.append(self.var_sub(args[0]))
    def servername(self, args):
        self.name = args[0]

    # modsec: create a rule{}
    def secrule(self, args):
        last_id = int(tmp.last_rule_id)
        r = secrule(args)
        if r.id:
            tmp.last_rule_id = r.id
        elif rules.get(last_id) and "chain" in rules[last_id].flags:
            tmp.last_rule_id = round(tmp.last_rule_id + 0.1, 1)
            r.id = tmp.last_rule_id
            r.chained_to = int(last_id) # primary parent
        rules[r.id] = self.ruledecl[r.id] = r
        #print(r.__dict__)

    # modsec: just a secrule without conditions
    def secaction(self, args):
        self.secrule(["@SecAction", "setvar:", args[0]])
    
    # modsec: SecRuleRemoveById 900001 900002 900003
    def secruleremovebyid(self, args):
        for a in args:
            if re.match("^\d+-\d+$", a):   # are ranges still allowed?
                a = [int(x) for x in a.split("-")]
                for i in range(*a):
                    if i in rules:    # only apply state for known/existing rules, not the whole range()
                        self.rulestate[i] = 0
            elif re.match("^\d+$", a):
                self.rulestate[int(a)] = 0
            else:
                self.rulestate[a] = 0  # from tag

    # modsec: SecRuleRemoveByTag sqli app-name
    def secruleremovebytag(self, args):
        self.secruleremovebyid(args)

    # these need to be mapped onto existing rules (if within t==cfg)
    # · SecRuleUpdateTargetById
    # · SecRuleUpdateActionById

    # modssec: irrelevant (not caring about skipAfter rules)
    def secmarker(self, args):
        pass

    # v3-connector: Include
    def modsecurity_rules_file(self, args):
        raise Exception("modsecurity v3 connector rules not supported (module doesn't provide disclosure of custom includes via `apache2ctl -t -D DUMP_INCLUDES` yet)")
        #vhosts[fn] = vhost(args[0], srvroot.read(args[0]))
    
    # apache: define ENV var
    def define(self, args):
        tmp.env[args[0]] = args[1]
    
    # map rule ids to line numbers
    def mk_linemap(self, src):
        for i,line in enumerate(src.split("\n")):
            id = rx.id_num.search(line)
            if id:
                self.linemap[i] = int(id.group(1))
    # find closest match
    def line_to_id(self, lineno):
        if not lineno in self.linemap:
            lines = [i for i in sorted(self.linemap.keys()) if i <= lineno]
            if lines and lines[-1] in self.linemap:
                self.linemap[lineno] = self.linemap.get(lines[-1])
        return self.linemap.get(lineno, 0)


# break up SecRule definition into parameters, attributes (id,msg,tags,meta,actions etc.)
class secrule:
    """
        SecRule properties
        
        Parameters
        ----------
        args : list
               Three directive parameters (as in 'SecRule […] […] […]')
        
        Attributes
        ----------
        id : int
                Rule ID
        chained_to : int
                Parent rule ID for flags=[chain] rules
        msg : str
                Message
        flags : list
                Any of block, deny, t:none, ... rule actions
        params : dict
                Any action:value from rule actions, e.g. logdata:..
        tags : list
                Any tag:name from actions
        tag_primary : str
                Most unique of the tags
        ctl : dict
                Any ctl:action=value from rule actions
        setvar : dict
                Any servar:name=val from rule actions
        vars : str
                e.g. ARGS|PARAMS or &TX.VAR
        pattern : str
                e.g. '@rx ^.*$'
        hidden : bool
                Mark pure control rules / SecActions
    """
    
    def __init__(self, args):
        # secrule properties
        self.id = 0
        self.chained_to = 0
        self.msg = ""
        self.flags = []
        self.params = {}
        self.tags = []
        self.tag_primary = ""
        self.ctl = {}
        self.setvar = {}
        self.vars = "REQ*"
        self.pattern = "@rx ..."
        self.hidden = False
        # args must contain 3 bits for a relevant SecRule
        if len(args) != 3:
            #print("UNEXPECTED NUMBER OF ARGS:", args)
            return
        self.vars, self.pattern, actions = args
        #print(args)
        # split up actions,attributes:…
        for pfx, action, value, qvalue in rx.actions.findall(actions):
            #print(pfx,action,value,qvalue)
            self.assign(pfx, action, value or qvalue)
        # most specific tag
        for p in tmp.tag_prio:
            if p in self.tags:
                self.tag_primary = p
                break
        # if SecAction (uncoditional rule, mostly setvars:)
        if self.vars == "@SecAction" and not self.msg:
            self.msg = f"@SecAction {self.setvar or self.params}" #.format(str(self.setvar) if self.setvar else str(self.params))
        # alternative .msg
        if not self.msg:
            self.msg = self.params.get("logdata") or f"{self.vars}   {self.pattern}" #.format(self.vars, self.pattern)
        # .hidden (flow control rules)
        self.hidden = self.pattern == "@eq 0" or self.vars == "TX:EXECUTING_PARANOIA_LEVEL"


    # distribute actions/attributes into properties here
    def assign(self, pfx, action, value):
        if action == "id":
            self.id = int(value)
        elif action == "msg":
            self.msg = value
        elif action == "tag":
            self.tags.append(value)
        elif action == "ctl":
            if value.find("=") > 0:
                action, value = value.split("=", 1)
            self.ctl[action] = value or 1
        elif action == "setvar":
            if value.find("=") > 0:
                action, value = value.split("=", 1)
            self.setvar[action] = value
        elif pfx == "t" and not value:
            self.flags.append(pfx+":"+action)
        elif action and not pfx:
            if value:
                self.params[action] = value
            else:
                self.flags.append(action)
        else:
            print("  WHATNOW? ", [pfx, action, value])
    
    # look up doc comment in source file
    def help(self):
        id = int(self.id)
        for fn,vh in vhosts.items():
            if id in vh.ruledecl:
                src = srvroot.read(fn)
                r = rx.rule_comment.format(id)
                comment = re.search(r, src, re.X|re.M)
                if comment:
                    comment = re.sub("^#\s*|\\n(?=\\n)", "", comment.group(1), 0, re.M)
                    #comment = re.sub("\\n\\n+", "\n", comment, 0, re.M)
                    return comment.strip()
                break
        return "No documentation comment present"
    


# scan for APACHE_ENV= vars
def read_env_vars():
    for fn in tmp.env_locations:
        if srvroot.exists(fn):
            src = srvroot.read(fn)
            tmp.env.update(
                dict(rx.shell_vars.findall(src))
            )

# iterate over all Apache config files, visit relevant ones (vhosts/mod_security configs)
def scan_all():
    read_env_vars()
    for fn in apache_dump_includes():
        print(".", end=""); sys.stdout.flush()
        src = srvroot.read(fn)
        if rx.interesting.search(src):
            vhosts[fn] = vhost(fn, src)

# get *.conf list from apache2ctl
def apache_dump_includes():
    stdout = srvroot.popen(["apache2ctl", "-t", "-D", "DUMP_INCLUDES"])
    return rx.dump_includes.findall(stdout.read().decode("utf-8"))

# just used once    
def count_tags():
    import collections
    tags = []
    for fn,v in rules.items():
        if v.tags:
            tags = tags + v.tags
    print(list(reversed(list(collections.Counter(tags).keys()))))
    
# prepare list of names for mainwindow vhosts/conf combobox
def list_vhosts(types=["cfg","vhost"]):
    return [k for k,v in vhosts.items() if v.t in types]



# initialization (scan_all) is done atop mainwindow

#scan_all()
#count_tags()
#pprint(vhosts)
#print({k:pprint(v.__dict__) for k,v in vhosts.items()})
