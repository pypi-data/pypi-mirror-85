# encoding: utf-8
# api: python
# type: main
# title: main window
# description: GUI with menus, actions, rules and logs
# category: config
# version: 0.1.0
# state:   alpha
# license: ASL
# config: 
#    { name: theme, type: select, value: DarkRed1, select: "Default|DarkGrey|Black|BlueMono|BluePurple|BrightColors|BrownBlue|Dark|Dark2|DarkAmber|DarkBlack|DarkBlack1|DarkBlue|DarkBlue1|DarkBlue10|DarkBlue11|DarkBlue12|DarkBlue13|DarkBlue14|DarkBlue15|DarkBlue16|DarkBlue17|DarkBlue2|DarkBlue3|DarkBlue4|DarkBlue5|DarkBlue6|DarkBlue7|DarkBlue8|DarkBlue9|DarkBrown|DarkBrown1|DarkBrown2|DarkBrown3|DarkBrown4|DarkBrown5|DarkBrown6|DarkBrown7|DarkGreen|DarkGreen1|DarkGreen2|DarkGreen3|DarkGreen4|DarkGreen5|DarkGreen6|DarkGreen7|DarkGrey|DarkGrey1|DarkGrey10|DarkGrey11|DarkGrey12|DarkGrey13|DarkGrey14|DarkGrey2|DarkGrey3|DarkGrey4|DarkGrey5|DarkGrey6|DarkGrey7|DarkGrey8|DarkGrey9|DarkPurple|DarkPurple1|DarkPurple2|DarkPurple3|DarkPurple4|DarkPurple5|DarkPurple6|DarkPurple7|DarkRed|DarkRed1|DarkRed2|DarkTanBlue|DarkTeal|DarkTeal1|DarkTeal10|DarkTeal11|DarkTeal12|DarkTeal2|DarkTeal3|DarkTeal4|DarkTeal5|DarkTeal6|DarkTeal7|DarkTeal8|DarkTeal9|Default|Default1|DefaultNoMoreNagging|Green|GreenMono|GreenTan|HotDogStand|Kayak|LightBlue|LightBlue1|LightBlue2|LightBlue3|LightBlue4|LightBlue5|LightBlue6|LightBlue7|LightBrown|LightBrown1|LightBrown10|LightBrown11|LightBrown12|LightBrown13|LightBrown2|LightBrown3|LightBrown4|LightBrown5|LightBrown6|LightBrown7|LightBrown8|LightBrown9|LightGray1|LightGreen|LightGreen1|LightGreen10|LightGreen2|LightGreen3|LightGreen4|LightGreen5|LightGreen6|LightGreen7|LightGreen8|LightGreen9|LightGrey|LightGrey1|LightGrey2|LightGrey3|LightGrey4|LightGrey5|LightGrey6|LightPurple|LightTeal|LightYellow|Material1|Material2|NeutralBlue|Purple|Python|Reddit|Reds|SandyBeach|SystemDefault|SystemDefault1|SystemDefaultForReal|Tan|TanBlue|TealMono|Topanga", description: "PySimpleGUI window theme", help: "Requires a restart to take effect." }
#    { name: switch_auto, type: bool, value: 0, description: "Automatically switch to matching error.log when chaning conf/vhost selection" }
# priority: core
# classifiers: x11, http
#
# The main window binds all processing logic together. Lists
# primarily the SecRules and their states (depending on the
# selected vhost/*.conf file). Then allows to search through
# logs to find potential false positives.
#



import sys, os, re, json, subprocess
from modseccfg import utils, appsettings, icons, vhosts, logs, writer
from modseccfg.recipe import recipe
import PySimpleGUI as sg
sg.theme(appsettings.conf["theme"])

#-- init
rule_tree = sg.TreeData()
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
                    ['File', ['Rescan configs', 'Rescan logs', "Edit conf/vhost file", 'Test', 'Settings', 'Exit']],
                    ['Rule', ['Info', 'Disable', 'Enable', 'Modify', '<Wrap>', 'Masquerade']],
                    ['Recipe', ['<Location>', '<FilesMatch>', '<Directory>', "Exclude parameter", "ConvertToRewriteRule"]],
                    ['Help', ['Advise']]
                ], key="menu"
            )],
            # button row
            [
                sg.Button("ℹ  Info",disabled=1),
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
                justification="left", show_expanded=0, num_rows=30, auto_size_columns=False
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
        self.w = sg.Window(title=f"mod_security config {utils.srvroot.srv}", layout=layout, size=(1200,775), font="Sans 12", resizable=1)
        self.tab = "secrules"
        self.status = self.w["status"].update
        self.vh = None
        self.no_edit = [949110, 980130]

    # event loop and function/module dispatching
    def main(self):
        while True:
            event, data = self.w.read()
            if event == sg.WIN_CLOSED:
                event, data = "exit", {}
            event = self._case(data.get("menu") or event)
            self.tab = self._case(data.get("active_tab", ""))

            if event and hasattr(self, event):
                getattr(self, event)(data)
            elif recipe.has(event):
                recipe.show(event, data)
            elif event == "exit":
                break
            else:
                #self.status(value=
                print(f"UNKNOWN EVENT: {event} / {data}")
        self.w.close()
    
    # change in vhost combobox
    def confn(self, data):
        self.vh = vhosts.vhosts.get( data.get("confn") )
        logfn = data.get("logfn")
        # switch logfn + automatically scan new error.log?
        if appsettings.conf["switch_auto"]:
            logs = re.grep("error", self.vh.logs)
            if len(logs):
                self.w["logfn"].update(value=logs[0])
                self.logfn(data=dict(logfn=logs[0]))
        self.update_rules()

    # scan/update log
    def logfn(self, data):
        self.w["log"].update(
            logs.scan_log(data["logfn"])
        )
        self.update_rules()

    # SecRuleRemoveById
    def disable(self, data):
        id = data["rule"]
        if id:
            id = id[0]
        else:
            return
        if id in self.no_edit and sg.popup_yes_no("This rule should not be disabled (it's a heuristic/collective marker). Continue?") != "Yes":
            return
        fn = data["confn"]
        if fn and id:
            writer.append(fn, directive="SecRuleRemoveById", value=id, comment=" # "+vhosts.rules[id].msg)
            self.vh.rulestate[id] = 0
            self.update_rules()

    # remap 'settings' event to pluginconf window
    def settings(self, data):
        appsettings.window(self)

    def edit_conf_vhost_file(self, data):
        import modseccfg.editor
        modseccfg.editor.editor(data["confn"])

    # renew display of ruletree with current log and vhost rulestate
    def update_rules(self):
        if self.vh:
            self.w["rule"].update(ui_data.rules(log_count=logs.log_count, rulestate=self.vh.rulestate))

    # remove non-alphanumeric characters (for event buttons / tab titles / etc.)
    def _case(self, s):
        return re.sub("\W+", "_", str(s)).strip("_").lower()
        
    # tmp/dev
    def test(self, data):
        print("No test code")

            

#-- main
def main():
    gui_event_handler().main()


