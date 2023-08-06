# encoding: utf-8
# api: python
# type: main
# title: main window
# description: GUI with menus, actions, rules and logs
# category: config
# version: 0.2.0
# state:   alpha
# license: ASL
# config: 
#    { name: theme, type: select, value: DarkRed1, select: "Default|DarkGrey|Black|BlueMono|BluePurple|BrightColors|BrownBlue|Dark|Dark2|DarkAmber|DarkBlack|DarkBlack1|DarkBlue|DarkBlue1|DarkBlue10|DarkBlue11|DarkBlue12|DarkBlue13|DarkBlue14|DarkBlue15|DarkBlue16|DarkBlue17|DarkBlue2|DarkBlue3|DarkBlue4|DarkBlue5|DarkBlue6|DarkBlue7|DarkBlue8|DarkBlue9|DarkBrown|DarkBrown1|DarkBrown2|DarkBrown3|DarkBrown4|DarkBrown5|DarkBrown6|DarkBrown7|DarkGreen|DarkGreen1|DarkGreen2|DarkGreen3|DarkGreen4|DarkGreen5|DarkGreen6|DarkGreen7|DarkGrey|DarkGrey1|DarkGrey10|DarkGrey11|DarkGrey12|DarkGrey13|DarkGrey14|DarkGrey2|DarkGrey3|DarkGrey4|DarkGrey5|DarkGrey6|DarkGrey7|DarkGrey8|DarkGrey9|DarkPurple|DarkPurple1|DarkPurple2|DarkPurple3|DarkPurple4|DarkPurple5|DarkPurple6|DarkPurple7|DarkRed|DarkRed1|DarkRed2|DarkTanBlue|DarkTeal|DarkTeal1|DarkTeal10|DarkTeal11|DarkTeal12|DarkTeal2|DarkTeal3|DarkTeal4|DarkTeal5|DarkTeal6|DarkTeal7|DarkTeal8|DarkTeal9|Default|Default1|DefaultNoMoreNagging|Green|GreenMono|GreenTan|HotDogStand|Kayak|LightBlue|LightBlue1|LightBlue2|LightBlue3|LightBlue4|LightBlue5|LightBlue6|LightBlue7|LightBrown|LightBrown1|LightBrown10|LightBrown11|LightBrown12|LightBrown13|LightBrown2|LightBrown3|LightBrown4|LightBrown5|LightBrown6|LightBrown7|LightBrown8|LightBrown9|LightGray1|LightGreen|LightGreen1|LightGreen10|LightGreen2|LightGreen3|LightGreen4|LightGreen5|LightGreen6|LightGreen7|LightGreen8|LightGreen9|LightGrey|LightGrey1|LightGrey2|LightGrey3|LightGrey4|LightGrey5|LightGrey6|LightPurple|LightTeal|LightYellow|Material1|Material2|NeutralBlue|Purple|Python|Reddit|Reds|SandyBeach|SystemDefault|SystemDefault1|SystemDefaultForReal|Tan|TanBlue|TealMono|Topanga", description: "PySimpleGUI window theme", help: "Requires a restart to take effect." }
#    { name: switch_auto, type: bool, value: 0, description: "Automatically switch to matching error.log when chaning conf/vhost selection" }
#    { name: keyboard_binds, type: bool, value: 1, description: "Enable keyboard shortcuts in main window", help: "F1=info, F3/F4=editor, F5=log-viewer, F12=settings" }
# priority: core
# classifiers: x11, http
#
# The main window binds all processing logic together. Lists
# primarily the SecRules and their states (depending on the
# selected vhost/*.conf file). Then allows to search through
# logs to find potential false positives.
#



import sys, os, re, json, subprocess
from modseccfg import utils, icons, vhosts, logs, writer, editor, ruleinfo
from modseccfg.utils import srvroot, conf
from modseccfg.recipe import recipe
import PySimpleGUI as sg
sg.theme(conf["theme"])

#-- init
vhosts.scan_all()


#-- prepare vhost/rules/logs for UI structures
class ui_data:

    @staticmethod
    def rules(log_count={}, rulestate={}):
        rule_tree = sg.TreeData()
        hidden = [0]
        for id,r in vhosts.rules.items():
            # skip control rules
            if r.hidden:
                hidden.append(id)
                continue
            parent = ""
            if r.chained_to:
                parent = r.chained_to
                if parent in hidden:
                    continue
            # prepare treedata attributes
            state = rulestate.get(id)
            if state in (0, "off"):
                state = "❌"
            elif state in (-1, "change"):
                state = "➗"
            else:
                state = "✅"
            rule_tree.insert(
                parent=parent,
                key=id,
                text=id,
                values=[
                   state, str(id), r.msg, r.tag_primary, log_count.get(id, 0)
                ],
                icon=icons.vice #ui_data.img_vice
            )
        return rule_tree

#-- widget structure
layout = [
    [sg.Column([
            # menu
            [sg.Menu([
                    ["File", ["Edit conf/vhost file", "---", "Settings", "SecEngine options", "CRS options", "---", "Rescan configs", "Rescan logs", "Test", "---", "Exit"]],
                    ["Rule", ["Info", "Disable", "Enable", "Modify", "<Wrap>", "Masquerade"]],
                    ["Recipe", ["<Location>", "<FilesMatch>", "<Directory>", "Exclude parameter", "ConvertToRewriteRule"]],
                    ["Help", ["Advise"]]
                ], key="menu"
            )],
            # button row
            [
                sg.Button("⭐ Info"),
                sg.Button("❌ Disable"),
                sg.Button("✅ Enable"),
                sg.Button("➗ Modify",disabled=1),
                sg.Button("❮❯ Wrap",disabled=1)
            ],
            [sg.T(" ")],
            # comboboxes
            [sg.Text("vhost/conf", font="bold"),
             sg.Combo(key="confn", size=(50,1), values=vhosts.list_vhosts(), enable_events=True),
             sg.Text("Log"),
             sg.Combo(key="logfn", values=logs.find_logs(), size=(30,1), enable_events=True),
             ],
        ]),
        # logo
        sg.Column([ [sg.Image(data=icons.logo)] ], element_justification='r', expand_x=1),
    ],
    # tabs
    [sg.TabGroup([[
        # rule
        sg.Tab("   SecRules                                                                        ", [[
            sg.Tree(
                key="rule", data=ui_data.rules(), headings=["❏","RuleID","Description","Tag","Count"],
                col0_width=0, col_widths=[1,10,65,15,10], max_col_width=500,
                justification="left", show_expanded=0, num_rows=30, auto_size_columns=False,
                enable_events=False
            )
            #], expand_x=1, expand_y=1, size=(600,500))
        ]]),
        # log
        sg.Tab("  Log                                             ", [[
            sg.Listbox(values=["... 403", "... 500"], size=(980,650), key="log")
        ]])
    ]], key="active_tab")],
    [sg.Text("...", key="status")]
]



#-- GUI event loop and handlers
class gui_event_handler:

    # prepare window
    def __init__(self):
        self.w = sg.Window(
            title=f"mod_security config {utils.srvroot.srv}", layout=layout, font="Sans 12",
            size=(1200,775), return_keyboard_events=conf["keyboard_binds"], resizable=1, icon=icons.icon
        )
        self.tab = "secrules"
        self.status = self.w["status"].update
        self.vh = None
        self.no_edit = [949110, 980130]
        self.win_map = {}
    
   # add to *win_map{} event loop
    def win_register(self, win, cb=None):
        if not cb:
            cb = lambda *e: win.close()
        self.win_map[win] = cb
        win.read(timeout=1)

    # demultiplex PySimpleGUI events across multiple windows
    def main(self):
        self.win_register(self.w, self.event)
        while True:
            win_ls = [win for win in self.win_map.keys()]
            #print(f"l:{len(win_ls)}")
            # unlink closed windows
            for win in win_ls:
                if win.TKrootDestroyed:
                    print("destroyed" + str(win))
                    del self.win_map[win]
            # all gone
            if len(win_ls) == 0:
                break
            # if we're just running the main window, then a normal .read() does suffice
            elif len(win_ls) == 1 and win_ls==[self.w]:
                print(f"main window only: {{win_ls}}")
                self.event(*self.w.read())
            # poll all windows - sg.read_all_windows() doesn't quite work
            else:
                #win_ls = self.win_map.iteritems()
                for win in win_ls:
                    event, data = win.read(timeout=20)
                    if event and event != "__TIMEOUT__" and self.win_map.get(win):
                        self.win_map[win](event, data)
                    elif event == sg.WIN_CLOSED:
                        win.close()
        sys.exit()

    # mainwindow event dispatcher
    def event(self, event, data):
            
        # prepare common properties
        data = data or {}
        event = self._case(data.get("menu") or event)
        event = gui_event_handler.map.get(event, event)
        self.tab = self._case(data.get("active_tab", ""))
        self.id = (data.get("rule") or [0])[0]
        self.vh = vhosts.vhosts.get( data.get("confn") )

        # dispatch
        if event and hasattr(self, event):
            getattr(self, event)(data)
        elif recipe.has(event):
            recipe.show(event, data)
        elif event == "exit":
            self.w.close()
        else:
            #self.status(value=
            print(f"UNKNOWN EVENT: {event} / {data}")

    # alias/keyboard map
    map = {
        sg.WIN_CLOSED: "exit",
        "none": "exit",  # happens when mainwindow still in destruction process
        "f3_69": "edit_conf_vhost_file",
        "f4_70": "edit_conf_vhost_file",
        "f5_71": "log_view",
        "f12_96": "settings",
        "return_36": "info"
    }
    
    # change in vhost combobox
    def confn(self, data):
        logfn = data.get("logfn")
        # switch logfn + automatically scan new error.log?
        if conf["switch_auto"]:
            logs = re.grep("error", self.vh.logs)
            if len(logs):
                self.w["logfn"].update(value=logs[0])
                self.logfn(data=dict(logfn=logs[0]))
        self.update_rules()

    # scan/update log
    def logfn(self, data):
        self._cursor("watch")
        self.w["log"].update(
            logs.scan_log(data["logfn"])
        )
        self.update_rules()
        self._cursor("arrow")

    # add "SecRuleRemoveById {id}" in vhost.conf
    def disable(self, data):
        if self.id in self.no_edit and self._cancel("This rule should not be disabled (it's a heuristic/collective marker). Continue?"):
            return
        if data["confn"] and self.id:
            writer.append(data["confn"], directive="SecRuleRemoveById", value=self.id, comment=" # "+vhosts.rules[self.id].msg)
            self._update_rulestate(self.id, 0)  # 0=disabled

    # remove any "SecRuleRemove* {id}" in vhost.conf
    def enable(self, data):
        if not self.id: # or not vhosts.rules.get(self.id):
            return
        if self.vh and self.vh.rulestate.get(self.id) != 0 and self._cancel("SecRule might be wrapped/masked. Reenable anyway?"):
            return
        writer.remove_remove(data["confn"], "SecRuleRemoveById", self.id)
        self._update_rulestate(self.id, None)

    # remap 'settings' event to pluginconf window
    def settings(self, data):
        utils.cfg_window(self)

    # editor
    def edit_conf_vhost_file(self, data):
        editor.editor(data.get("confn"), register=self.win_register)

    # log view
    def log_view(self, data):
        editor.editor(data.get("logfn"), readonly=1)

    # secrule details
    def info(self, data):
        if self.tab == "secrules":
            self.win_register(
                ruleinfo.show(self.id, log_values=self.w["log"].get_list_values)
            )
        else:
            print("No info() for "+self.tab)

    # renew display of ruletree with current log and vhost rulestate
    def update_rules(self, *data):
        if self.vh:
            self.w["rule"].update(ui_data.rules(log_count=logs.log_count, rulestate=self.vh.rulestate))

    # called from disable/enable to set 0=disabled, 1=masked, None=enabled, etc
    def _update_rulestate(self, id, val):
        if self.vh:
            if val==None and id in self.vh.rulestate:
                del self.vh.rulestate[id]
            else:
                self.vh.rulestate[id] = val
            self.update_rules()

    # remove non-alphanumeric characters (for event buttons / tab titles / etc.)
    def _case(self, s):
        return re.sub("\W+", "_", str(s)).strip("_").lower()

    # set mouse pointer ("watch" for planned hangups)
    def _cursor(self, s="arrow"):
        self.w.TKroot.config(cursor=s)
        self.w.read(timeout=1)
    
    def _cancel(self, text):
        return sg.popup_yes_no(text) == "No"
        
    # tmp/dev
    def test(self, data):
        print("No test code")

            

#-- main
def main():
    gui_event_handler().main()


