# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.font
import config as cfg
import cast as ct
import webbrowser
from hyperlink_manager import HyperlinkManager

class About:
    def __init__(self, root):
        """initialize"""
        self.root=root
        self.root.resizable(0,0) 

    def __os_bug_fix(self, path, tab):   
        """rewrite file, because some linux-distributive does not support passing url which contains anchor""" 
        label ="/*[#active_tab#]*/" 
        content = ct.file_get_contents(path)  
        res = content.split(label)
        res[1]="window.location.replace(document.URL+'#tabs|SAXSEV:" + tab+ "');"
        end_page = label.join(res)
        ct.file_put_contents(path, end_page)
        return path

    def open_user_manual(self):
        """user's guide button handler"""
        webbrowser.open_new(self.__os_bug_fix(cfg.paths["doc_data_path"],"user_manual"))
        return

    def open_developer_manual(self):
        """developer's guide button handler"""
        webbrowser.open_new(self.__os_bug_fix(cfg.paths["doc_data_path"],"developer_manual"))
        return

    def make_about_layout(self):
        """defines the text area"""
        #frame = Frame(self.root)
        frame=Frame(self.root)     
        frame.columnconfigure(0, pad=0)
        frame.columnconfigure(1, pad=10)
        frame.columnconfigure(2, pad=10)
        custom_font = tkinter.font.Font ( family="Helvetica", size=8)
        # add diploma image
        img = PhotoImage(file = "./images/credits.gif")
        __lbl = Label(frame, image = img)
        __lbl.image=img
        # add credits
        __lbl.grid(row=0, column=0, padx=2, pady=(4,0), sticky=E)
        __lbl = Label(frame, text="SAXSEV 2.1.1\nAll rights reserved \u00A9 2014\nKuchko A.V.\nSmirnov A.V.",justify=LEFT)
        __lbl.grid(row=0, column=1, padx=(0,4), pady=4, sticky=W)
        # link contained description
        text = Text(frame, width=36, height=8, wrap=WORD, font=custom_font)        
        text.tag_config("blockquote", lmargin1=8,lmargin2=4,spacing1=4,spacing3=4,spacing2=2)
        hyperlink=HyperlinkManager(text)
        text.insert(INSERT,"The Results and the main principles of estimation Volume Fraction Distribution Function with SAXSEV 2.1 was introduced in ", "blockquote")
        text.insert(INSERT, "J. Nanosystems", hyperlink.add(lambda *o:webbrowser.open_new("http://nanojournal.ifmo.ru/en/articles/volume3/3-3/physics/paper06/")))
        text.insert(END,"\n")
        text.insert(INSERT, "If you need help, visit ","blockquote")
        text.insert(INSERT, "http://ev.saxslab.org/feedback", hyperlink.add(lambda *o:webbrowser.open_new("http://ev.saxslav.org/feedback")))
        text.grid(row=1, column=0, padx=4, pady=4, columnspan=3, rowspan=4, sticky=W)
        # make textarea read-only        
        text.config(state=DISABLED)
        # buttons visit site/close dialog
        __btn = Button(frame, text="Home page", command = lambda:webbrowser.open_new("http://ev.saxslab.org"), width=16)
        __btn.grid(row=1, column=2, padx=4, pady=2,sticky=E)
        __btn = Button(frame, text="User's Guide", command = lambda: self.open_user_manual(), width=16)
        __btn.grid(row=2, column=2, padx=4, pady=2,sticky=E)       
        __btn = Button(frame, text="Developer's Guide", command = lambda: self.open_developer_manual(), width=16)
        __btn.grid(row=3, column=2, padx=4, pady=2,sticky=E)       
        __btn = Button(frame, text="Cancel", command = lambda *q: self.root.destroy(), width=16)
        __btn.grid(row=4, column=2, padx=4, pady=2,sticky=E) 
        frame.pack()
        return
