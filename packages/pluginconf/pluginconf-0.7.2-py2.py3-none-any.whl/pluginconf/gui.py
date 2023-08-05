# encoding: UTF-8
# api: python
# type: ui
# category: io
# title: Config GUI
# description: Display plugins + options in setup window
# version: 0.7
# depends: python:pysimplegui (>= 4.0)
# priority: optional
# config: -
#
# Creates a PySimpleGUI options list. Scans a given list of *.py files
# for meta data, then populates a config{} dict and (optionally) a state
# map for plugins themselves.
#
#    jsoncfg = {}
#    pluginconf.gui.window(jsoncfg, {}, ["plugins/*.py"])
#
# Very crude, and not as many widgets as the Gtk/St2 implementation.
#


import PySimpleGUI as sg
import pluginconf
import glob, json, os, re, textwrap


# temporarily store collected plugin config: dicts
options = {}
plugins = {
    "global": {
        "id":"pluginconf", "title":"global settings", "version":"0.0",
        "type":"virtual", "category":"ui", "api":"python", "config": [
            {"name":"test", "type":"bool", "value":1, "description":"…"}
        ]
    }
}


#-- show configuation window
#
# · reads *.py files and crafts a settings dialog from meta data
# · updates config{} settings and plugin_states{} on saving
# · if files= is omitted, then plugins`→"global"→config[] should be prepopulated
#
def window(config={}, plugin_states={}, files=["*/*.py"], theme="DefaultNoMoreNagging", **kwargs):
    if theme:
        sg.theme(theme)
    if files:
        plugins = read_options(files)
    layout = plugin_layout(plugins.values(), config, plugin_states)
    layout.append([sg.T(" ")])
    #print(repr(layout))
    
    # pack window
    layout = [
        [sg.Column(layout, expand_x=1, expand_y=0, size=(575,680), scrollable="vertically", element_justification='left')],
        [sg.Column([[sg.Button("Cancel"), sg.Button("Save")]], element_justification='right')]
    ]
    if not "title" in kwargs:
        kwargs["title"] = "Options"
    if not "font" in kwargs:
        kwargs["font"] = "Sans 11"
    win = sg.Window(layout=layout, resizable=1, **kwargs)

    # wait for save/exit        
    event,data = win.read()
    win.close()
    if event=="Save":
        for k,v in data.items():
            if options.get(k):
                #@ToDo: handle array[key] names
                config[k] = cast.fromtype(data[k], options[k])
            elif type(k) is str and k.startswith('p:'):
                k = k.replace('p:', '')
                if plugins.get(k):
                    plugin_states[k] = v
        return True
    #print(config, plugin_states)
    
    
# craft list of widgets for each read plugin
def plugin_layout(ls, config, plugin_states):
    layout = []
    for plg in ls:
        #print(plg.get("id"))
        layout = layout + plugin_entry(plg, plugin_states)
        for opt in plg["config"]:
            if opt.get("name"):
                layout.append(option_entry(opt, config))
    return layout
    
# checkbox for plugin name
def plugin_entry(e, plugin_states):
    id = e["id"]
    return [
         [
             sg.Checkbox(
                  e.get("title", id), key='p:'+id, default=plugin_states.get(id, 0), tooltip=e.get("doc"), metadata="plugin",
                  font="bold", pad=(0,(8,0))
             ),
             sg.Text("({}/{})".format(e.get("type"), e.get("category")), text_color="#005", pad=(0,(8,0))),
             sg.Text(e.get("version"), text_color="#a72", pad=(0,(8,0)))
         ],
         [
             sg.Text(e.get("description", ""), tooltip=e.get("doc"), font=("sans", 10), pad=(26,(0,10)))
         ]
    ]

# widgets for single config option
def option_entry(o, config):
    #print(o)
    name = o.get("name", "")
    desc = wrap(o.get("description", name), 60)
    type = o.get("type", "str")
    help = o.get("help", None)
    if help:
        help = wrap(help, 60)
    options[name] = o
    val = config.get(name, o.get("value", ""))
    if o.get("hidden"):
        pass
    elif type == "str":
        return [
            sg.InputText(key=name, default_text=str(val), size=(20,1), pad=((50,0),5)),
            sg.Text(wrap(desc, 50), pad=(5,2), tooltip=help or name, justification='left', auto_size_text=1)
        ]
    elif type == "bool":
        return [
            sg.Checkbox(wrap(desc, 70), key=name, default=cast.bool(val), tooltip=name, pad=((40,0),2), auto_size_text=1)
        ]
    elif type == "int":
        return [
            sg.InputText(key=name, default_text=str(val), size=(6,1), pad=((50,0),3)),
            sg.Text(wrap(desc, 60), pad=(5,2), tooltip=help or name, auto_size_text=1)
        ]
    elif type == "select":
        #o["select"] = parse_select(o.get("select", ""))
        values = [v for v in o["select"].values()]
        return [
            sg.Combo(key=name, default_value=o["select"].get(val, val), values=values, size=(15,1), pad=((50,0),0), font="Sans 11"),
            sg.Text(wrap(desc, 47), pad=(5,2), tooltip=help or name, auto_size_text=1)
        ]
    elif type == "dict":  # or "table" rather ?
        return [
            sg.Table(values=config.get(name, ["", ""]), headings=o.get("columns", "Key,Value").split(","),
            num_rows=5, col_widths=30, def_col_width=30, auto_size_columns=False, max_col_width=150, key=name, tooltip=desc
            )
        ]
    return []


#-- read files, return dict of {id:pmd} for all plugins
def read_options(files):
    ls = [pluginconf.plugin_meta(fn=fn) for pattern in files for fn in glob.glob(pattern)]
    return dict(
        (meta["id"], meta) for meta in ls
    )


#-- map option types (from strings)
class cast:
    @staticmethod
    def bool(v):
        if v in ("1", 1, True, "true", "TRUE", "yes", "YES", "on", "ON"):
            return True
        return False
    @staticmethod
    def int(v):        
        return int(v)
    @staticmethod
    def fromtype(v, opt):
        if not opt.get("type"):
            return str(v)
        elif opt["type"] == "int":
            return cast.int(v)
        elif opt["type"] == "bool":
            return cast.bool(v)
        elif opt["type"] == "select":
            inverse = dict((v,k) for k,v in opt["select"].items())
            return inverse.get(v, v)
        else:
            return v

#-- textwrap for `description` and `help` option fields
def wrap(s, w=50):
    return "\n".join(textwrap.wrap(s, w)) if s else ""
