# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.font
import os
import icast as ict
import config as cfg
                      
class History:
    def __init__(self, root):
        """initialize"""
        frame = Frame(root)
        self.txtfr(frame)
        frame.pack()
        if(os.path.isfile(cfg.paths["log_file_path"])):          
            self.text.insert(END,ict.read_log(cfg.paths["log_file_path"]))
        else:
            open(cfg.paths["log_file_path"], 'w+')
        return

    def txtfr(self, frame):
        """defines the text area"""
        textfr = Frame(frame)

        scroll_horizontal = Scrollbar(textfr, orient = HORIZONTAL)
        scroll_vertical = Scrollbar(textfr, orient=VERTICAL)

        self.custom_font = tkinter.font.Font ( family="Helvetica", size=16, weight="bold" )
        self.text = Text(textfr, height = 20, width = 80, wrap=NONE, background='white',xscrollcommand=scroll_horizontal.set, yscrollcommand=scroll_vertical.set,font = self.custom_font)

        scroll_horizontal.config(command=self.text.xview)
        scroll_horizontal.pack(side = BOTTOM,fill = X)

        scroll_vertical.config(command=self.text.yview)
        scroll_vertical.pack(side = RIGHT,fill = Y)

        self.text.pack(side = LEFT)
        textfr.pack(side = TOP)
        return