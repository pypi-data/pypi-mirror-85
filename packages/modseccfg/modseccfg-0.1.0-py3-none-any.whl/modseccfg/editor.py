# api: modseccfg
# type: gui
# title: editor
# description: simple text window to edit *.conf file
# version: 0.2
# config:
#    { name: editor, type: str, value: "", description: External editor to use }
#
# Just a textbox really.


import os, re
from modseccfg import utils, appsettings, writer
from modseccfg.utils import srvroot
import PySimpleGUI as sg



def editor(fn, readonly=False):
    """
        Basic editor window.
        
        If you want to use an external tool, then configure
        `editor` in the settings. Notably this should be a
        GUI tool, else will show up in the terminal and block
        the main UI.
    """
    
    # external
    if appsettings.conf.get("editor"):
        return os.system(appsettings.conf["editor"] + " " + srvroot.fn(fn) + " &")

    # internal    
    layout = [
        [sg.Menu([
            ["File", ["Save", "Close"]],
            ["Edit", ["Undo", "Redo", "---", "Cut", "Copy", "Paste", "Delete", "---", "Search..."]],
            ["View", ["Font", ["FreeMono 12", "Sans 12", "Consolas 11", "DejaVu Sans Mono Bold 13", "Liberation Mono 11", "Noto Sans Mono 12", "Ubuntu Mono 11", "Mono 13"], "Color", ["Default", "Terminal"]]],
            ["Help", ["Info", "I"]]
        ])],
        [sg.Pane([
            sg.Column([[
               sg.Button("Save", key="save", disabled=readonly), sg.Button("Cancel", key="cancel"),
               sg.Text("                    Search:"), sg.Input("", key="findstr", size=(15,1), enable_events=True), sg.Button("⏿", key="s")
            ]], size=(50,20)),
            sg.Column([[
              sg.Multiline(default_text=srvroot.read(fn), key="src", font=("Consolas 11"), border_width=5, autoscroll=1, focus=True, size=(95,30))
            ]]),
            sg.Column([[
              sg.StatusBar("...")
            ]])
        ])],
    ]
    w = sg.Window(layout=layout, size=(930,670), title=f"Edit {srvroot.srv} {fn}", resizable=0)
    w.read(timeout=1)
    w_src = w["src"]
    w_src.set_vscroll_position(0.99)
    tk_src = w_src.Widget
    tk_src.tag_config("highlight", background="orange")
    search = search_pos = ""
    
    while True:
        event, data = w.read()
        #print(event,data)
        if event in (sg.WIN_CLOSED, "Cancel", "cancel", "Close", "Exit") or data.get("cancel"):
            w.close()
            break;
        elif event in ["Info"]:
            sg.popup(editor.__doc__)
        elif not readonly and event in ["Save", "save"] or data.get("save"):
            srvroot.write(fn, data["src"])
            if event == "save":
                w.close()
                break;
        elif re.match(r"\w+ \d+", event):
            w_src.update(font=re.findall("([\w\s]+)\s(\d+)", event)[0])
        elif event == "Terminal":
            w_src.update(text_color='white', background_color='black')
        elif event == "Default":
            w_src.update(text_color='black', background_color='white')
        elif event == "Undo":
            tk_src.edit_undo()
        elif event == "Redo":
            tk_src.edit_redo()
        elif event == "Paste":
            try: tk_src.insert("insert", w.TKroot.clipboard_get())
            except: pass
        elif event == "findstr" and len(data.get("findstr")):
            tk_src.tag_remove("highlight", "1.0", "end")
            for pos in find_all(tk_src, data["findstr"]):
                if pos:
                    tk_src.tag_add("highlight", pos, incr_index(pos, len(data["findstr"])))
        elif event in ["Search", "Search...", "s"]:
            if search != data["findstr"]:
                search = data["findstr"]
                search_pos = "1.0"
            search_pos = tk_src.search(search, incr_index(search_pos))
            if search_pos:
                tk_src.see(search_pos)
                tk_src.mark_set("insert", search_pos)
                w_src.SetFocus()

def find_all(tk, findstr, pos="1.0"):
    ls = []
    while True:
         pos = tk.search(findstr, incr_index(pos, 1))
         if pos in ls:
             break
         else:
             ls.append(pos)
    return ls

def incr_index(pos, add=1):
    if not pos or not pos.find("."):
        return "end"
    y,x = pos.split(".")
    x = int(x) + add
    return f"{y}.{x}"
