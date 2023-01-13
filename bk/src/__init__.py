    # -*- coding: utf-8 -*-
from fbrowser import *
import webbrowser
from settings import ISettings           # module for creation config window
from history import History              # module for creation log browser
from about import About                  # module for creation copyright
    
def about(root):
    """help&copyrights"""
    second_window = Toplevel(root)
    second_window.transient(root)
    second_window.title("Saxs-settings manager")
    frame=Frame(second_window)
    about_window = About(second_window)
    about_window.make_about_layout()
    frame.pack()

def history_manager(root):
    """Browse last action"""
    second_window = Toplevel(root)
    second_window.title("Saxs-settings manager")
    frame = Frame(second_window)
    History(second_window)
    frame.pack()   

def config_manager(root):
    """Browse/Setup configuration"""
    win = Toplevel(root)
    win.transient(root)
    win.title("Saxs-settings manager")
    frame = Frame(win)
    conf = ISettings(win)
    conf.make_generic_form()
    frame.pack()   

def pc_editor(root):
    """Browse/Setup configuration"""
    win = Toplevel(root)
    win.transient(root)
    win.title("Percept Criteria Editor")
    frame = Frame(win)
    conf = ISettings(win)
    conf.make_pc_params_form()
    frame.pack()   

def nb_editor(root):
    """Browse/Setup configuration"""
    win = Toplevel(root)
    win.transient(root)
    win.title("Session Edditor")
    frame = Frame(win)
    conf = ISettings(win)
    conf.make_nb_session_form()
    frame.pack()   

def main():
    root = Tk()
    # disable maximize button
    root.resizable(0,0)
    # start menu creation
    m = Menu(root)     
    # menu object creation
    root.config(menu=m)
    # create main interface  
    mw = MainWidget(root)
    # first menu item
    fm = Menu(m, tearoff=0)
    m.add_cascade(label = "File", menu=fm)
    fm.add_command(label = "Refresh", command=lambda *m: mw.init_presets())
    fm.add_command(label = "Exit",command=lambda *m: mw.quit())
    # second menu item
    cm = Menu(m, tearoff=0) 
    m.add_cascade(label = "Setting", menu=cm)
    cm.add_command(label = "Config", command=lambda *c: config_manager(root))
    cm.add_command(label = "History", command=lambda *h:history_manager(root))
    cm.add_command(label = "PC-params", command=lambda *pc:pc_editor(root))
    cm.add_command(label = "Netbox", command=lambda *ftp:nb_editor(root))
    # third menu item
    hm = Menu(m, tearoff=0)
    m.add_cascade(label="Help", menu=hm)
    hm.add_command(label="Contents", command=lambda: webbrowser.open_new(cfg.paths["doc_data_path"]))
    hm.add_command(label="About", command=lambda *a: about(root))
    root.title('SAXS - Estimation of VFDF')
    root.mainloop()
    
main()
