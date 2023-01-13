# -*- coding: utf-8 -*-
from tkinter import *

class LayoutMaker():
    def __init__(self, lbl_width=16, entry_width=16, entry_file_width=24, combo_width=12, btn_width=16, btn_field_width=10):
        """initialize presets"""
        self.__lbl_width = lbl_width
        self.__entry_width = entry_width
        self.__combo_width = combo_width
        self.__btn_width = btn_width
        self.__btn_field_width = btn_field_width
        self.__entry_file_width = entry_file_width
        self.__entry_width = entry_width

    def __make_lbl(self, parent, pos, lbl_text, lbl_width, v_pad):
        """add label to grid cell"""
        __lbl = Label(parent, width=lbl_width, text=lbl_text, anchor=W)
        __lbl.grid(row=pos, column=0, padx=0, pady=v_pad, sticky=W) 
        return __lbl    

    def make_entry_grid(self, parent, pos, lbl_text, entry_width=None, lbl_width=None, v_pad=4, state=NORMAL):
        """add entry with label grid cell"""
        if entry_width is None:
            entry_width=self.__entry_width 
        if lbl_width is None:
            lbl_width=self.__lbl_width 
        self.__make_lbl(parent, pos, lbl_text, lbl_width, v_pad)
        __entry = Entry(parent, width=entry_width, state=state)
        __entry.grid(row=pos, column=1, padx=(4,0), pady=v_pad, sticky=W)
        return __entry

    def make_combo_grid(self, parent, pos, lbl_text, options, default=None, lbl_width=None, combo_width=None, v_pad=4):
        """add combo to grid cell"""
        if lbl_width is None:
            lbl_width=self.__lbl_width 
        if combo_width is None:
            combo_width=self.__combo_width 
        if default is None:
            default = options[0]
            
        self.__make_lbl(parent, pos, lbl_text, lbl_width, v_pad)
        __combo = ttk.Combobox(parent, state = 'readonly', width=combo_width)
        __combo["values"] = options 
        __combo.set(default)  
        __combo.grid(row=pos, column=1, padx=4,  pady=v_pad, sticky=W)
        return __combo

    def make_btn_grid(self, parent, row, column, btn_text, cmd, btn_width=None, btn_padx=4, btn_pady=4):
        """add button to grid cell"""
        if btn_width is None:
            btn_width=self.__btn_width 
        __btn = Button(parent, text=btn_text , command = cmd, width=btn_width)
        __btn.grid(row=row, column=column, padx=btn_padx, pady=btn_pady, sticky=E)
        return __btn

    def make_file_entry(self, parent, pos, lbl_text, cmd, btn_width=None, btn_text="Browse", v_pad=4, entry_file_width=None, lbl_width=None):
        """add browse file field"""
        if btn_width is None:
            btn_width=self.__btn_field_width 
        if entry_file_width is None:
            __entry_file_width = self.__entry_file_width 
        if lbl_width is None:
            lbl_width = self.__lbl_width 

        __entry = self.make_entry_grid(parent, pos, lbl_text, __entry_file_width, lbl_width, v_pad)
        __btn = self.make_btn_grid(parent, pos, 2, btn_text, cmd, btn_width, btn_padx=1, btn_pady = v_pad)
        return [__entry,__btn]

    def make_checkbox(self, parent, pos, lbl_text, cmd=None):
        """add checkbox field"""
        __var = IntVar()
        __chb = Checkbutton(parent, text=lbl_text, variable=__var, anchor=W, borderwidth=1)
        if cmd!=None:
            __chb.bind("<Button-1>", cmd)
        __chb.grid(row = pos, column=1, padx=0, pady=0, sticky=W, columnspan=2)   
        return [__chb, __var]

    def make_pc_checkboxbar(self, parent, pos, lbl_text, cmd=None, var=None):
        """add checkbox field"""
        __var = IntVar()
        if var!=None:
            __chb = Checkbutton(parent, text=lbl_text, variable=var, anchor=W, borderwidth=1)
        else:
            __chb = Checkbutton(parent, text=lbl_text, variable=__var, anchor=W, borderwidth=1)
        if cmd!=None:
            __chb.bind("<Button-1>", cmd)
        __chb.grid(row = pos, column=0, padx=0, pady=0, sticky=W, columnspan=2) 
        return [__chb, __var]


    def make_lbl_frame(self, parent, lbl_frame_text):
        return LabelFrame(parent, text=lbl_frame_text, relief=RAISED, borderwidth=1, pady=8, padx = 8)
    
    def make_pc_entry_grid(self, parent, pos, lbl_text, entry_width=None, lbl_width=None, v_pad=4):
        if entry_width is None:
            entry_width=self.__entry_width 
        if lbl_width is None:
            lbl_width=self.__lbl_width 
        self.__make_lbl(parent, pos, lbl_text.upper(), lbl_width, v_pad)
        __entry1 = Entry(parent, width=entry_width)
        __entry1.grid(row=pos, column=1, padx=(4,0), pady=v_pad, sticky=W)
        __entry2 = Entry(parent, width=entry_width)
        __entry2.grid(row=pos, column=2, padx=(4,0), pady=v_pad, sticky=W)
        __entry3 = Entry(parent, width=entry_width)
        __entry3.grid(row=pos, column=3, padx=(4,0), pady=v_pad, sticky=W)
        return __entry1,__entry2,__entry3

    def make_pc_label_grid(self, parent, lbl0_text, lbl1_text, lbl2_text, lbl3_text, lbl_width=None, v_pad=4):
        if lbl_width is None:
            lbl_width=self.__lbl_width 
        __lbl0 = Label(parent, width=lbl_width, text=lbl0_text.upper())
        __lbl0.grid(row=0, column=0, padx=0, pady=v_pad,sticky=W) 
        __lbl1 = Label(parent, width=lbl_width, text=lbl1_text.upper())
        __lbl1.grid(row=0, column=1, padx=0, pady=v_pad,sticky=W) 
        __lbl2 = Label(parent, width=lbl_width, text=lbl2_text.upper())
        __lbl2.grid(row=0, column=2, padx=0, pady=v_pad,sticky=W) 
        __lbl3 = Label(parent, width=lbl_width, text=lbl3_text.upper())
        __lbl3.grid(row=0, column=3, padx=0, pady=v_pad,sticky=W)   