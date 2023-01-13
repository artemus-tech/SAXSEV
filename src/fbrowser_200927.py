# -*- coding: utf-8 -*-
"""
start import features for interface 
http://docs.python.org/3/library/tkinter.html
"""
import os
import glob
"""import features for interface"""
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
"""import ui-components"""
from layout import LayoutMaker           # module to generate layouts
"""import general modules for calculation"""
import cast as ct                        # module with general physicl/math stuff
import icast as ict                      # module with interface assets
import numpy as np                       # http://www.numpy.org/
import config as cfg                     # module for storage config in ini-file
from pltconf import  plt                 # module for storage ploting config 
"""import special modules for estimation"""
from percept_criteria import PerceptCriteria  # module for evaluation  Percept Criteria
from res_vfdf import VFDF               # module for restore vfdf by experimental/model indicatrix
from surface_area import Surface        # module for surface area estimation
from grid_corrector import GridCorrector   # module for correct Rg arguments grid 
from grid_generator import GridGenerator   # module for generation Rg arguments grid 
import sp_vrija_no_volumeComplex_2N200723 as vrij
import sp_intens as teor
import datetime   

def getter_indi_wrap(fn):
    """check if indicatrix is stored"""
    def getter_indi_method(self):
        buf = self.indi_is_uploaded
        fn(self)
        if buf:
            self.indi_is_uploaded = True
    return getter_indi_method

class MainWidget:
    def __init__(self,root):
        """initialize presets"""   
        self.root = root
        # create layout for main dialog sections
        frame = Frame(root, width=800, height=600)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, pad=10)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(5, pad=10)
        # insert sections into main dialog
        self.make_menubar(frame)
        # packing
        frame.pack()
        # initialize widgets vars
        self.init_presets()
        # get project location
        self.cwd = os.getcwd()
        # set interface icon
        if os.name is 'nt':
            self.root.iconbitmap('./images/calc.ico')
        return
      
    def init_presets(self):
        # clear message lists
        self.vfdf_err_message = []
        self.surface_err_message = []
        self.indi_err_message = []
        self.view_err_message = []
        self.mode_err_message = None
        # reset buffer vars
        self.alpha_optimum = None
        self.vfdf = None
        self.rg = None
        self.indicatrix_arg = None
        # path
        self.vfdf_auto_selected_path = None
        self.ivfdf_auto_selected_path = None

        #reset flags
        self.indi_is_uploaded = False
        self.indi_ambiguity_is_uploaded = False
        self.scattering_intens_ambiguity = None
        self.vfdf_is_uploaded = False
        self.vfdf_ambiguity_is_uploaded = False
        self.vfdf_eval_input_is_uploaded = False
        self.vfdf_isset = False
        self.vfdf_path = None
        self.vfdf_manual_selected_path = None
        self.pc_file_name = None
        # reset text fields
        ict.set_location(self.indi_path_entry, "")
        ict.set_location(self.grid_path_entry, "")
        ict.set_location(self.vfdf_path_entry, "") 
        ict.set_location(self.pc_path_entry, "")
        ict.set_location(self.surface_entry, "")
        ict.set_location(self.surface_ambiguity_entry,"")  
        ict.set_location(self.vfdf_selected_path_entry, "")
        ict.set_location(self.anisometer_factor_entry,"")
        ict.set_location(self.alpha_user_select_entry,"")
        ict.set_location(self.alpha_result_entry,"")
        # set params for plot
        self.view_alpha = None
        self.view_fi = None
        self.view_fi0 = None 
        # toggle check buttons
        self.show_intens = self.should_show_intens.get()
        self.by_alpha = self.should_use_alpha_opt.get()
        self.to_q = self.to_scat_vect.get()

        if self.show_intens:
            self.show_intens_chb.toggle()
        if self.by_alpha:
            self.use_alpha_chb.toggle()  
        if not self.to_q:
            self.to_scat_vect_chb.toggle()  
        # reset shapes dropdown list      
        self.shapes_combo.current(0)
        # filenamses
        self.gid_generated_filename = "rg_grid_generated.dat"
        self.gid_corrected_filename = "rg_grid_corrected.dat"
        self.grid_correct_path=None
        self.grid_path = None
        self.pc_keys=['IMPMIN','STABIL','DISCRP','POSITIV', 'SYSDEV', 'VALCEN', 'ALPHA','TOTAL', 'ERRDEV', 'OSCIL']

    def make_menubar(self,frame): 
        """generate main dialog window"""  
        lm_main = LayoutMaker()
        # first section for indicatrix loading;Rg-grid genertion                        
        menubar1 = lm_main.make_lbl_frame(frame,lbl_frame_text="SAXS INPUT")
        # Load Intensity&Scattering vector
        self.indi_path_entry, _ = lm_main.make_file_entry(menubar1, pos=0, lbl_text="Indicatrix", cmd=self.get_indicatrix)
        # Scattering vecotr/angle user choise
        self.to_scat_vect_chb, self.to_scat_vect = lm_main.make_checkbox(menubar1, pos=1, lbl_text="Convert THETTA to q automatically",cmd=self.get_q)
        # Button for Loading Rg-Grid
        self.grid_path_entry, _ = lm_main.make_file_entry(menubar1, pos=2, lbl_text="Rg-Grid", cmd=self.upload_datagrid, v_pad=(4,0)) 
        lm_main.make_btn_grid(menubar1, row=3, column=2, btn_text="Generate", cmd=self.generate_datagrid, btn_width=10, btn_padx=1, btn_pady=0)
        # Textbox to set Anisometric factor
        self.anisometer_factor_entry = lm_main.make_entry_grid( menubar1, pos=4, lbl_text="Anisometric factor") 
        # create shape selector for distribution estimation
        self.shapes_combo = lm_main.make_combo_grid(menubar1, pos=5, lbl_text="Particle shape", options=cfg.shapes)
        # second section for Svergun params and VFDF operation
        menubar2 = lm_main.make_lbl_frame(frame, lbl_frame_text="VFDF - ESTIMATION")
        # Set location for distribution collection
        self.vfdf_path_entry, _ = lm_main.make_file_entry(menubar2, pos=0, lbl_text="VFDF-collection", cmd=self.get_vfdf_collection,v_pad=(4,0)) 
        lm_main.make_btn_grid(menubar2, row=1, column=2, btn_text="Estimate", cmd=self.eval_vfdf,btn_width=10, btn_pady=0, btn_padx=1,)
        # Modified Svergun Percept Criteria
        self.pc_path_entry, _ = lm_main.make_file_entry(menubar2, pos=2, lbl_text="Percept Criteria", cmd=self.get_pc, v_pad=(4,0))
        # Button estimate
        lm_main.make_btn_grid(menubar2, row=3, column=1, btn_text="Estimate", cmd=self.eval_pc, btn_pady=0,btn_padx=1, btn_width=10)
        # Button Preview
        lm_main.make_btn_grid(menubar2, row=3, column=2, btn_text="Preview", cmd=self.view_pc,btn_pady=0, btn_padx=1, btn_width=10)
        # Text fields for alpha selected by use and compared
        self.alpha_user_select_entry = lm_main.make_entry_grid(menubar2, pos=4, lbl_text="Selected alpha")
        self.alpha_result_entry = lm_main.make_entry_grid(menubar2, pos=5, lbl_text="Optimal alpha")
        # Third section for evaluating SpecificSurface and Rg-Grid correction
        menubar3 = lm_main.make_lbl_frame(frame, lbl_frame_text="VFDF - SELECTION")
        # vfdf-path field with label
        self.vfdf_selected_path_entry, self.select_vfdf_btn = lm_main.make_file_entry(menubar3, pos=2, lbl_text="VFDF-instance", cmd=self.select_vfdf, v_pad=0)
        # Button UpLoad
        lm_main.make_btn_grid(menubar3, row=3, column=2, btn_text="Upload", cmd=self.upload_vfdf, btn_pady=0, btn_padx=1, btn_width=10)
        # Use alpha selected by user from Percept Criteria Plot
        self.use_alpha_chb, self.should_use_alpha_opt = lm_main.make_checkbox(menubar3, pos=4, lbl_text="Use optimum value of alpha-param", cmd=self.__switch_alpha_optima)
        # Show intensity checkbox
        self.show_intens_chb, self.should_show_intens = lm_main.make_checkbox(menubar3, pos=5, lbl_text="Show intensity on the same plot")
        # Button Preview
        lm_main.make_btn_grid(menubar3, row=6, column=1, btn_text="Preview", cmd=self.view_vfdf, btn_pady=(4,12), btn_padx=1, btn_width=10)
        # Button Correct
        lm_main.make_btn_grid(menubar3, row=6, column=2, btn_text="Correct", cmd=self.correct_vfdf, btn_pady=(4,12), btn_padx=1, btn_width=10)
        #ict.make_btn_grid(menubar3, row=8, column=1, btn_text="Estimate", cmd=self.eval_surface_area, btn_pady=2, btn_width=10)
        self.surface_entry, _ = lm_main.make_file_entry(menubar3, pos=7, btn_text="Estimate", lbl_text="Surface area", cmd=self.eval_surface_area, v_pad=(4,0))
        # Third section for evaluating SpecificSurface and Rg-Grid correction
        self.surface_ambiguity_entry  = lm_main.make_entry_grid( menubar3, pos=8, lbl_text="Ambiguity")
        # pack main dialog       
        menubar1.pack(fill = X, expand = True, padx = 5, pady = 5)    
        menubar2.pack(fill = X, expand = True, padx = 5, pady = 5)    
        menubar3.pack(fill = X, expand = True, padx = 5, pady = 5)
        return
        
    def __check_indicatrix_format(self, M):
        """check format of inptut indcatrix matrix"""
        if ict.is_matrix(M):
            if not ict.is_column_exist(M, 0):
                self.indi_is_uploaded = False
                self.indi_err_message.append("There is no scatterind angle")
            if not ict.is_column_exist(M, 1):
                self.indi_is_uploaded = False
                self.indi_err_message.append("There is no intensity")
            if not ict.is_column_exist(M, 2):
                self.indi_is_uploaded = False
                self.indi_err_message.append("There is no angle ambiguity")
            if not ict.is_column_exist(M, 3):
                #self.indi_is_uploaded = False
                self.indi_ambiguity_is_uploaded = False
                self.indi_err_message.append("There is no intensity ambiguity")
        else:
            self.indi_ambiguity_is_uploaded = False
            self.indi_is_uploaded = False
            self.indi_err_message.append("File must have matrix structure")
        return
           
    def get_q(self, evt):
        if self.indicatrix_arg is not None:
            #self.q = ct.scat_vect(self.indicatrix_arg) if self.to_scat_vect.get() else self.indicatrix_arg
            if self.to_scat_vect.get():
                self.q = ct.scat_vect(self.indicatrix_arg)
            else:
                self.q = self.indicatrix_arg
        
        
        
    @getter_indi_wrap
    def get_indicatrix(self):
        """start method for uploading indicatrix vector"""
        self.indi_path = askopenfilename(filetypes = [("allfiles","*"),("pythonfiles","*.py")], initialdir=cfg.paths["input_data_path"])
        # clear list of missing vectors
        self.indi_err_message[:]=[]
        if self.indi_path:
            M = np.loadtxt(self.indi_path)
            # set status of data uploading
            self.indi_is_uploaded = True
            self.indi_ambiguity_is_uploaded = True
            self.__check_indicatrix_format(M)
            if self.indi_is_uploaded:
                #self.scattering_angle = M[:,0]
                self.indicatrix_arg = M[:,0]
                #self.q = ct.scat_vect(M[:,0]) if self.to_scat_vect.get() else M[:,0]
                if self.to_scat_vect.get():
                    self.q = ct.scat_vect(self.indicatrix_arg)
                else:
                    self.q = self.indicatrix_arg

                self.scattering_intens = M[:,1]
                self.scattering_angle_ambiguity = M[:,2]

                if self.indi_ambiguity_is_uploaded:
                    self.scattering_intens_ambiguity = M[:,3]
                else:            
                    self.scattering_intens_ambiguity = None
                ict.set_location(self.indi_path_entry, self.indi_path)
            else:
                messagebox.showwarning(
                    "Upload indicatrix",
                    "\n".join(self.indi_err_message)
                )        
            # save record to log
            ict.save_log(cfg.paths["log_file_path"],"Upload saxs indicatrix " + self.indi_path)     
        return

    def __set_grid(self):
        """set rg-vector value"""
        grid = np.loadtxt(self.grid_path, usecols=[0,])
        self.rg = np.unique(grid)
             
    def upload_datagrid(self):
        """start method for uploading vector of radius geration"""    
        self.grid_path = askopenfilename(filetypes = [("allfiles","*"),("pythonfiles","*.py")],initialdir=cfg.paths["input_data_path"])
        if self.grid_path:
            self.__set_grid()
            ict.set_location(self.grid_path_entry,self.grid_path)
            ict.save_log(cfg.paths["log_file_path"], "Upload Rg args grid " + self.grid_path )
        return

    def generate_datagrid(self):
        """start method for generate grid of radius arguments"""
        if self.indi_is_uploaded:
            self.grid_path = os.path.join(cfg.paths["input_data_path"],self.gid_generated_filename) #+ "\\rg_grid_gen.dat"              
            # get current Figure instance
            fig = plt.figure()
            # Plot Distribution
            fig.add_subplot(111)  
            # to set focus into plot window
            fig.canvas.get_tk_widget().focus_force()
            # set window title
            fig.canvas.set_window_title('Setup : Rg-Grid for VFDF-evaluation')
            # set labels
            plt.ylabel('VFDF, $\mathregular{arb.u.}$')
            plt.xlabel('Radius of gyration, $\mathregular{nm}$')
            # init Grid Generator
            gg = GridGenerator(self.q, res_grid_path = self.grid_path)
            # connect to click button_press_event
            plt.connect('button_press_event', gg.on_click)
            # connect to click motion_notify_event
            plt.connect('motion_notify_event', gg.on_move)
            # connect to close plot window event
            plt.connect('close_event', gg.on_close)


            # save to log
            ict.save_log(cfg.paths["log_file_path"], "Generate Rg args grid ")
            # show plot
            plt.show()
        else:
            messagebox.showwarning(
                "DataGrid Generator",
                "You must upload Indicatrix-data at first"
            )
        return                       

    def __switch_alpha_optima(self, evt):
        """Disable or Enable vfdf-load button"""
        if self.should_use_alpha_opt.get() < 1:
            self.vfdf_selected_path_entry.config(state = DISABLED)
            self.select_vfdf_btn.config(state = DISABLED)
        else:
            self.vfdf_selected_path_entry.config(state = NORMAL)
            self.select_vfdf_btn.config(state = NORMAL)
      
    def __check_eval_vfdf_input_data(self):
        """check necessary input and params existance"""        
        if not self.anisometer_factor:
            self.vfdf_eval_input_is_uploaded = False
            self.vfdf_err_message.append("Anisometer factor is not defined")
        if not self.indi_is_uploaded:
            self.vfdf_err_message.append("Indicatrix data was not uploadded")
            self.vfdf_eval_input_is_uploaded = False
        if not self.choise:
            self.vfdf_err_message.append("Shape was not selected")
            self.vfdf_eval_input_is_uploaded = False
        if  not ct.np_arr_is_exists(self.rg):
            self.vfdf_err_message.append("Rg-grid was not uploaded")
            self.vfdf_eval_input_is_uploaded = False

    def __generate_vfdf_ivfdf_files(self):
        """Evaluate vfdf/ivfdf-collections"""
        K = VFDF(self.scattering_intens, self.q, self.rg, self.scattering_intens_ambiguity)
        if self.choise == "ellipsoid":
            K.restore_ell(self.anisometer_factor)
        if self.choise == "paralellipiped":
            K.restore_par(self.anisometer_factor)
        if self.choise == "cilindr":
            K.restore_cil(self.anisometer_factor)
        return  K.vfdf_dir

                    
    def eval_vfdf(self):
        """Evaluate VFDF"""
        os.chdir(cfg.paths["output_data_path"])
        self.vfdf_err_message[:]=[]
        self.vfdf_eval_input_is_uploaded=True
        self.anisometer_factor = ict.get_float_from_entry(self.anisometer_factor_entry)
        self.choise = ict.get_string_from_combo(self.shapes_combo)

        self.__check_eval_vfdf_input_data()
                 
        if self.vfdf_eval_input_is_uploaded:
            self.vfdf_dir = self.__generate_vfdf_ivfdf_files()
            self.vfdf_path = os.path.abspath(self.vfdf_dir)
            ict.set_location(self.vfdf_path_entry, self.vfdf_path) 
            ict.save_log(cfg.paths["log_file_path"], "VFDF estimation , particle shape:" + self.choise+";anisometric factor:" + str(self.anisometer_factor))
        else:
            messagebox.showwarning(
                "Eval distribution",
                "\n".join(self.vfdf_err_message)
            )        
        os.chdir(self.cwd)
        return   

    def __generate_pc_file(self):
        os.chdir(self.vfdf_path)
        # create pc-object
        pc = PerceptCriteria()
        # get pc-dictionary
        pc_dict = pc.get_pc_dict()
        pc_list = []
        # sort by keys
        for key in self.pc_keys:
            pc_list.append(pc_dict[key])
        pc_matrix = np.transpose(pc_list)
        # generate name
        pc_file_name = self.vfdf_dir + "@" + "_".join(self.pc_keys) + ".txt"
        # get full path
        pc_path = os.path.join(cfg.paths["output_data_path"], pc_file_name)
        # save results
        np.savetxt(pc_path, pc_matrix)
        os.chdir(self.cwd) 
        return [pc_path, pc_file_name]
        
    def eval_pc(self):
        """percept criteria evaluation"""
        if self.vfdf_path:
            self.vfdf_dir = ict.get_dir_name(self.vfdf_path)
            self.pc_path, self.pc_file_name = self.__generate_pc_file()
            ict.set_location(self.pc_path_entry, self.pc_path)
            # destroy PerceptCriteria object
            ict.save_log(cfg.paths["log_file_path"], "Percept Criteria estimation is started")
        else:
            messagebox.showwarning(
                "Estimate percept criteria",
                "You must set directory with collection of vfdf"
            )
        return
    
    def get_vfdf_collection(self):
        """start method for uploading restored vfdf"""    
        vfdf_path = askdirectory(initialdir=cfg.paths["output_data_path"])
        if vfdf_path:
            self.vfdf_path = vfdf_path
            self.vfdf_dir = ict.get_dir_name(self.vfdf_path) 
            ict.set_location(self.vfdf_path_entry,self.vfdf_path)
        return 

    def __get_vfdf_collection_by_pc_name(self, pc_name):
        """get vfdf-path&vfdf-dir"""
        self.vfdf_dir = pc_name.split("@")[0]
        self.vfdf_path = os.path.join(cfg.paths["output_data_path"], self.vfdf_dir)
        
    def get_pc(self):
        """start method load file with Percept Criteria"""
        self.pc_path = askopenfilename(filetypes = [("allfiles","*"),("pythonfiles","*.py")], initialdir=cfg.paths["output_data_path"])
        if self.pc_path:
            self.pc_file_name = os.path.basename(self.pc_path)
            ict.set_location(self.pc_path_entry, self.pc_path)
            ict.save_log(cfg.paths["log_file_path"], "loading PC-file " + self.pc_path)
            self.__get_vfdf_collection_by_pc_name(self.pc_file_name)
        return 

    def __check_vfdf_ambiguity(self, vfdf_matrix, isset,message):
        """check vfdf ambiguity vector existance"""
        if ict.is_matrix(vfdf_matrix):
            if not ict.is_column_exist(vfdf_matrix, 5):
                isset[0] = False
                message.append("VFDF ambiguity vector is not exist")
        else:
            isset[0] = False
            self.vfdf_err_message.append("VFDF-file must have matrix structure")
        return        
        
    def __check_vfdf_format(self, vfdf_matrix, isset, message):
        """check format in input vfdf matrix"""
        if ict.is_matrix(vfdf_matrix):
            if not ict.is_column_exist(vfdf_matrix, 0):
                isset[0] = False
                message.append("Rg vector is not exist")
            if not ict.is_column_exist(vfdf_matrix, 3):
                isset[0] = False
                message.append("VFDF vector is not exist")
        else:
            isset[0] = False
            message.append("VFDF-file must have matrix structure")
        return
      
    def __set_initial_dir(self):
        """set vfdf-file location"""
        if self.vfdf_manual_selected_path:
            initial_dir = ict.get_full_dir_path(self.vfdf_manual_selected_path)
        elif self.vfdf_path:
            initial_dir = self.vfdf_path
        else:                               
            initial_dir = cfg.paths["output_data_path"]
        return initial_dir

    def select_vfdf(self):
        """start method selection of  restore vfdf"""    
        self.vfdf_err_message[:]=[]
        vfdf_path = askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.py")], initialdir = self.__set_initial_dir())
        if vfdf_path:
            self.vfdf_manual_selected_path = vfdf_path         
            vfdf_matrix = np.loadtxt(self.vfdf_manual_selected_path)
            self.vfdf_is_uploaded = [True]
            self.vfdf_ambiguity_is_uploaded = [True]

            self.__check_vfdf_format(vfdf_matrix, self.vfdf_is_uploaded,self.vfdf_err_message)
                      
            if self.vfdf_is_uploaded[0]:
                self.__set_vfdf_matrix(vfdf_matrix)
                self.__set_vfdf_selected_dir(self.vfdf_manual_selected_path)
                ict.set_location(self.vfdf_selected_path_entry, self.vfdf_manual_selected_path)
            else:
                messagebox.showwarning(
                    "Wrong format of input data",
                    "\n".join(self.vfdf_err_message)
                )        
            ict.save_log(cfg.paths["log_file_path"], "loading vfdf-file " + self.vfdf_manual_selected_path)
        return 

    def __set_vfdf_selected_dir(self, path):
        """set selected vfdf location, only to extract plot title"""
        self.__vfdf_selected_dir = ict.get_full_dir_path(path)
            
    def find_optima( self, alpha ):
        """Looking for alpha - optimum"""
        params = self.pc_file_name[0:self.pc_file_name.rfind("@")].split("_")

        anisometric_factor = float(params[-1])
        shape = params[-2]

        self.vfdf_dir = cfg.options["vfdf_dir_pref"] + "_" + shape + "_" + str(anisometric_factor)
        correspond_path = os.path.join(cfg.paths["output_data_path"],self.vfdf_dir)
        
        if not os.path.exists(correspond_path):
            self.alpha_optimum = '#Error_PC#'
            messagebox.showwarning(
                "Warning",
                "There is no corresponding vfdf-dirrectory for this PC-file"
            )
            return

        os.chdir(correspond_path)
        
        alpha_arr = [ct.get_alpha_from_filename(vfdf_filename) for vfdf_filename in glob.glob('vfdf*.txt')]
        opt = alpha_arr[0]      
        alpha_opt_diff = abs(opt - alpha)         
        for i in range(len(alpha_arr)-1):                                                                            
            if  alpha_opt_diff > abs(alpha_arr[i] - alpha):
                alpha_opt_diff = abs(alpha_arr[i] - alpha)
                opt = alpha_arr[i]
        self.alpha_optimum = opt
        os.chdir(self.cwd)
        return opt    

    def __on_click(self,event):
        """click event to select alpha using percept criteria"""
        for axes in event.canvas.figure.axes:
            # to prevent merge modes with adding points procedure
            if axes.get_navigate_mode() is None:
                if event.xdata is not None and event.ydata is not None :
                    self.alpha_user_select_entry.configure(state=NORMAL)
                    self.alpha_user_select_entry.delete(0, END)
                    self.alpha_user_select_entry.insert(0, event.xdata)
                    plt.close()
                    alpha_opt = float(event.xdata)
                    self.find_optima(alpha_opt)  
                    self.alpha_result_entry.configure(state=NORMAL)
                    self.alpha_result_entry.delete(0, END)
                    self.alpha_result_entry.insert(0,self.alpha_optimum)
                    return {"xcord":event.x, "ycord":event.y, "xdata":event.xdata, "ydata":event.ydata}

    def view_pc(self):
        """Percept criteria visualisation"""
        os.chdir(cfg.paths["output_data_path"])  
        if self.pc_file_name:
            # assign vars to store Percept Criteria
            stabil = ct.get_vect_svparams(self.pc_file_name, "STABIL")
            positiv = ct.get_vect_svparams(self.pc_file_name, "POSITIV")
            valcen = ct.get_vect_svparams(self.pc_file_name, "VALCEN")
            oscil = ct.get_vect_svparams(self.pc_file_name, "OSCIL")
            discrp = ct.get_vect_svparams(self.pc_file_name, "DISCRP")
            alpha = ct.get_vect_svparams(self.pc_file_name, "ALPHA")
            total = ct.get_vect_svparams(self.pc_file_name, "TOTAL")
            sysdev = ct.get_vect_svparams(self.pc_file_name, "SYSDEV")
            errdev = ct.get_vect_svparams(self.pc_file_name, "ERRDEV")
            impmin = ct.get_vect_svparams(self.pc_file_name, "IMPMIN")
            # create plot-object
            fig = plt.figure()
            # to set focus into plot window
            fig.canvas.get_tk_widget().focus_force()
            # to set window title
            fig.canvas.set_window_title('Percept Criteria')
            # set handler for button_press_event
            fig.canvas.mpl_connect('button_press_event', self.__on_click)
            ##here
            plt.grid(True)                                     
            plt.ylim(0,2)
            plt.semilogx()            
            plt.ylabel('Criteria')
            plt.xlabel('ALPHA')
            # plot percept criteria plot
            if cfg.disp.get('stabil') == '1':
                plt.plot(alpha, stabil, "gs-", markersize=8, label="STABIL")
            if cfg.disp.get('positiv') == '1':
                plt.plot(alpha, positiv, "b+-", markersize=8, label="POSITIV")
            if cfg.disp.get('positiv') == '1':
                plt.plot(alpha, 1-positiv, "ko-", markersize=8, label="1-POSITIV")
            if cfg.disp.get('valcen') == '1':
                plt.plot(alpha, valcen,   "r*-", markersize=8, label="VALCEN")
            if cfg.disp.get('oscil') == '1':
                plt.plot(alpha, oscil, "bx-", markersize=8, label="OSCIL")
            if cfg.disp.get('discrp') == '1':
                plt.plot(alpha, discrp, "go-", markersize=8, label="DISCRP")
            if cfg.disp.get('sysdev') == '1':
                plt.plot(alpha, sysdev, "bo-", markersize=8, label="SYSDEV")
            if cfg.disp.get('errdev') == '1':
                plt.plot(alpha, errdev, "co-", markersize=8, label="ERRDEV")
            if cfg.disp.get('impmin') == '1':
                plt.plot(alpha, impmin, "mo-", markersize=8, label="IMPMIN")
            plt.plot(alpha, total, "ro-", markersize=8, label="TOTAL")
            plt.plot(alpha, 1-total, "wo-", markersize=8, label="1-TOTAL")
 
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.tight_layout()
            plt.subplots_adjust(right=0.657)
            plt.show()
        else:
            messagebox.showwarning(
                "View Percept Criteria",
                "You must upload percept criteria file"
            )
        os.chdir(self.cwd)  
        return
    
    def __set_params_text(self):
        """compile mathematical text expression"""
        txt = r'$\alpha='
        txt += str(('{:.2e}').format(self.view_alpha))
        txt +='$\n' 
        txt += r'$\Phi='
        txt += str(round(self.view_fi,3))
        txt +='$\n' 
        txt += r'$\Phi_+='
        txt += str(round(self.view_fi0,3))
        txt += r'$'
        return plt.annotate(txt, 
                     xy=(1.05, 0.95),
                     xycoords="axes fraction",
                     horizontalalignment='left',
                     verticalalignment='top', 
                     bbox=dict(boxstyle='square,pad=0.5',facecolor='white'))


    def plot_vfdf(self, rg_data, vfdf_data):
        """view vfdf"""
        plt.title(ict.make_title(self.__vfdf_selected_dir))
        plt.grid(True)                                    
        plt.semilogx()            
        plt.ylabel('VFDF, $\mathregular{arb.u.}$')
        plt.xlabel('Radius of gyration, $\mathregular{nm}$')
        plt.plot(rg_data, vfdf_data, "ro-",markersize=5)
        plt.tight_layout()
        self.__set_params_text()
        plt.subplots_adjust(right=0.657)
        return

    def plot_vfdf_ivfdf(self,fig, ivfdf_matrix, rg_data, vfdf_data):
        """view vfdf&ivfdf on one plot"""
        plt.subplot(311)
        self.plot_vfdf(rg_data, vfdf_data)
        plt.subplot(312)
        plt.grid(True)                                   
        plt.loglog() 
        plt.xlabel('length of the scattering vector, $\mathregular{nm^{-1}}$')
        plt.ylabel('Intensity, $\mathregular{arb.u.}$')
        plt.title("Intensities")
        plt.plot(ivfdf_matrix[:,0] ,ivfdf_matrix[:,1], "k-", linewidth=2, markersize=8, label=r'$I^{(\alpha)}_+$')
        plt.plot(ivfdf_matrix[:,0], ivfdf_matrix[:,2] ,"r+-", linewidth=2, markersize=4, label=r'$I^{(\alpha)}$')
        plt.plot(ivfdf_matrix[:,0], ivfdf_matrix[:,3] ,"o",mfc='none', markersize=3, label=r'$I^{src}$')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.subplot(313)
        plt.grid(True)                                    
        plt.semilogx() 
        plt.title("Intensities ambiguities")
        plt.plot(ivfdf_matrix[:,0], (ivfdf_matrix[:,1] - ivfdf_matrix[:,3])/ivfdf_matrix[:,4]  ,"kx-",markersize=8, label=r'${\delta}I^{(\alpha)}_+$')
        plt.plot(ivfdf_matrix[:,0], (ivfdf_matrix[:,2] - ivfdf_matrix[:,3])/ivfdf_matrix[:,4]  ,"rd-",mec='r',mfc='none',markersize=8, label=r'${\delta}I^{(\alpha)}$')
        plt.xlabel('length of the scattering vector, $\mathregular{nm^{-1}}$')
        plt.ylabel('Ambiguities, $\mathregular{arb.u.}$')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.subplots_adjust(right=0.657, bottom=0.08,hspace=0.6)
        return     
    
    def __set_view_params(self, path):
        """set params to display on plot"""
        __view_params_valid=True
        # extract alpha
        self.view_alpha = ct.get_alpha_from_filename(path)
        if not self.view_alpha:
            self.view_err_message.append("alpha not found")
            __view_params_valid=False
        # extract fi
        self.view_fi = ct.get_param_from_filename_by_key(path, "fi")
        if not self.view_fi:
            self.view_err_message.append("fi not found")        
            __view_params_valid=False
        # extract fiplus
        self.view_fi0 = ct.get_param_from_filename_by_key(path,"fiplus")
        if not self.view_fi0:
            self.view_err_message.append("fiplus not found")
            __view_params_valid=False
        return __view_params_valid
    
    def __validate_view_params(self,path):
        """error message for params validation"""
        self.view_err_message[:]=[]
        if not self.__set_view_params(path):
            messagebox.showwarning(
                "Wrong format of VFDF filename",
                "\n".join(self.view_err_message)
            )
            return False
        return True

    def __get_filename_by_alpha(self, opt, patern="i[vfdf*.txt"): 
        """starts method for compare file names of intensity and distribution function"""
        for filename in glob.glob(patern):           
            if  opt == ct.get_alpha_from_filename(filename):
                return filename
        return None
    
    def __get_vfdf_by_alpha(self):
        """find vfdf-matrix by alpha optimum"""
        os.chdir(self.vfdf_path)      
        vfdf_matrix = None
        vfdf_auto_selected_filename = self.__get_filename_by_alpha(self.alpha_optimum, patern="vfdf*.txt")
        if vfdf_auto_selected_filename:
            if self.__validate_view_params(vfdf_auto_selected_filename):
                vfdf_matrix = np.loadtxt(vfdf_auto_selected_filename)
                DT = str(datetime.datetime.now()).replace(":", "_")  
                if not os.path.exists("./vrija"+DT+"/"):
                    os.makedirs("./vrija"+DT+"/")

                vrij.NDF = vfdf_matrix[:,7]
                vrij.vector_rg = vfdf_matrix[:,6]
                vrij.norm = np.trapz(vrij.NDF, vrij.vector_rg)
                vrij.RMIN = np.min(vrij.vector_rg)
                vrij.RMAX = np.max(vrij.vector_rg)

                Iteor=[]
                teor.NDF = vfdf_matrix[:,7]
                teor.vector_rg = vfdf_matrix[:,6]
                teor.RMIN = np.min(vrij.vector_rg)
                teor.RMAX = np.max(vrij.vector_rg)
                
                for q in self.q:
                    #I.append(A*full_intens(q))
                    Iteor.append(teor.full_intens(q))
                teorNAME ="./vrija"+DT+"/teorIntens"+"_alfa="+str(self.alpha_optimum) + '.txt'
                print(teorNAME)
                np.savetxt( teorNAME,np.array([self.q,np.array(Iteor)]).T)
 
                Distr_Name = "./vrija"+DT+"/selected_Rg_VFDF_VFDFPOS_R_NDR"+"_alfa="+str(self.alpha_optimum) + '.txt'
                np.savetxt( Distr_Name,np.array([vfdf_matrix[:,0],vfdf_matrix[:,1],vfdf_matrix[:,3],vfdf_matrix[:,6],vfdf_matrix[:,7]]).T)
                
                #ИЗМЕНИТЬ ВВОД
                M_src_intens = np.loadtxt("c:\Work\НАУКА\ArtemVKuchko\Saxsev\input\TEST200920\intensity_vrija_for_FV(rg)_with_shape=6_scale=2.5_NC=0.4_shape=6.0_scale=2.5.txt")
                src_intens = M_src_intens[:,1] 
                vrij.NC = 0.4 #ИЗМЕНИТЬ ВВОД
                vrij.c = np.pi*vrij.NC/(6.0*vrij.get_Vmean())
                vrija = []
                for q in self.q:
                    vrija.append(vrij.sum_intens_vrija(q))
                    print(q)
                mono="./vrija"+DT+"/no_volume_vrija_"+"NC="+str(vrij.NC)+"_alfa="+str(self.alpha_optimum) + '.txt'
                print(mono)
                np.savetxt( mono,np.array([self.q,np.array(vrija),np.sqrt(vrija)]).T)
                    
                strFactorPR = np.array(vrija)/np.array(Iteor)
                divider = np.mean(strFactorPR[-5:]) 
                strFactor = strFactorPR/divider
                OutstrFactor ="./vrija"+DT+"/strFactor_"+"NC="+str(vrij.NC)+"_alfa="+str(self.alpha_optimum) + '.txt'
                
                strflist = []
                for strf in strFactor:
                    if strf <= 0:
                        strflist.append (1.0)
                    else:
                        strflist.append (strf)
                strFactor = strflist
                
                
                print(OutstrFactor)
                np.savetxt( OutstrFactor,np.array([self.q,strFactor]).T)

                reduce_scattering_intens = src_intens/strFactor
                redScattInt="./vrija"+DT+"/Q_reduce_scattering_intens_"+"NC="+str(vrij.NC)+"_alfa="+str(self.alpha_optimum) + '.txt'
                print(redScattInt)
                np.savetxt( redScattInt,np.array([self.q,reduce_scattering_intens,np.sqrt(reduce_scattering_intens),np.sqrt(reduce_scattering_intens)]).T)     
                  
                SRCScattInt="./vrija"+DT+"/"+os.path.basename(self.indi_path)
                print(SRCScattInt)
                np.savetxt( SRCScattInt,np.array([self.q,self.scattering_intens,np.sqrt(self.scattering_intens),np.sqrt(self.scattering_intens)]).T)               
                
                PC_file = np.loadtxt(self.pc_path)
                file_PC_name ="./vrija"+DT+"/" + self.pc_file_name
                print(file_PC_name)
                np.savetxt( file_PC_name,PC_file.T)               
                
                self.__set_vfdf_selected_dir(self.vfdf_path)
        else:
            messagebox.showwarning(
                "Loading IVFDF",
                "VFDF-file corresponding for this alpha not found"
            )        
        os.chdir(self.cwd)
        return vfdf_matrix       

    def __get_ivfdf_by_alpha(self):
        """find ivfdf-matrix by alpha optimum"""
        os.chdir(self.vfdf_path)
        ivfdf_matrix = None
        ivfdf_auto_selected_filename = self.__get_filename_by_alpha(self.alpha_optimum, patern="i[vfdf*.txt")
        if ivfdf_auto_selected_filename:
            ivfdf_matrix = np.loadtxt(ivfdf_auto_selected_filename)
        else:
            messagebox.showwarning(
                "Loading IVFDF",
                "IVFDF-file corresponding for this alpha not found"
            )                 
        os.chdir(self.cwd)
        return ivfdf_matrix

    def __get_auto_selected_vfdf_ivfdf_paths(self):
        """get ivfdf&vfdf path to upload on server"""
        os.chdir(self.vfdf_path)      
        vfdf_location_path = os.path.dirname(self.vfdf_path)
        ivfdf_auto_selected_filename = self.__get_filename_by_alpha(self.alpha_optimum, patern="i[vfdf*.txt")
        vfdf_auto_selected_filename = self.__get_filename_by_alpha(self.alpha_optimum, patern="vfdf*.txt")
        vfdf_auto_selected_path = os.path.join(vfdf_location_path, vfdf_auto_selected_filename)
        ivfdf_auto_selected_path = os.path.join(vfdf_location_path, ivfdf_auto_selected_filename)
        os.chdir(self.cwd)
        return [vfdf_auto_selected_path,ivfdf_auto_selected_path]

    def __get_manual_selected_vfdf_ivfdf_paths(self):
        """get ivfdf&vfdf path to upload on server"""
        vfdf_location_path = os.path.dirname(self.vfdf_manual_selected_path) 
        os.chdir(vfdf_location_path)
        alpha = ct.get_alpha_from_filename(self.vfdf_manual_selected_path)
        vfdf_auto_selected_path = None
        ivfdf_auto_selected_path = None
        if alpha:
            ivfdf_auto_selected_filename = self.__get_filename_by_alpha(alpha, patern="i[vfdf*.txt")
            vfdf_auto_selected_filename = self.__get_filename_by_alpha(alpha, patern="vfdf*.txt")
            vfdf_auto_selected_path = os.path.join(vfdf_location_path, vfdf_auto_selected_filename)
            ivfdf_auto_selected_path = os.path.join(vfdf_location_path, ivfdf_auto_selected_filename)
        else:
            messagebox.showwarning(
                "Upload",
                "Bad File selected"
            )
        os.chdir(self.cwd)
        return [vfdf_auto_selected_path,ivfdf_auto_selected_path]


     
    def __get_ivfdf_by_vfdf(self):
        """compare ivfdf to selected vfdf"""
        os.chdir(self.__vfdf_selected_dir)
        ivfdf_matrix=None        
        alpha = ct.get_alpha_from_filename(self.vfdf_manual_selected_path)
        ivfdf_manual_selected_path = self.__get_filename_by_alpha(alpha)
        if ivfdf_manual_selected_path:
            ivfdf_matrix = np.loadtxt(ivfdf_manual_selected_path)
        else:    
            messagebox.showwarning(
                "Loading IVFDF",
                "IVFDF-file corresponding for selecting VFDF not found"
            )
        os.chdir(self.cwd)
        return ivfdf_matrix                           

    def __check_mode_auto(self):
        """check current mode: if vfdf would be selected by alpha  optimum"""
        if self.should_use_alpha_opt.get():
            if self.alpha_optimum:
                return True
            else:
                self.mode_err_message="Alpha optimum was not selected"
        return False

    def __check_mode_manual(self):
        """check current mode: if manual uploaded vfdf would be used"""
        if not self.should_use_alpha_opt.get():
            if self.vfdf_is_uploaded:
                return True
            else:
                self.mode_err_message = "VFDF data was not set"
        return False         
     
    def view_vfdf(self):
        """start method for viewing single distribution function"""
        is_auto = self.__check_mode_auto()
        is_manual = self.__check_mode_manual()
        if is_auto:
            vfdf_matrix = self.__get_vfdf_by_alpha()
        if is_manual:
            vfdf_matrix = self.__get_vfdf_from_memory()
        if not is_auto and not is_manual:    
            messagebox.showwarning(
                "Plot pdf",
                self.mode_err_message
            )
            return  
        if ct.np_arr_is_exists(vfdf_matrix):
            VRg = vfdf_matrix[:,0]
            VDF = vfdf_matrix[:,4]
            # get current Figure instance
            fig = plt.figure()
            # to set focus into plot window
            fig.canvas.get_tk_widget().focus_force()
            # to set windw title
            fig.canvas.set_window_title('Result Volume Fraction Distribution function')
            # set title of graphic itself
            if self.should_show_intens.get(): 
                if is_auto:
                    ivfdf_matrix = self.__get_ivfdf_by_alpha()
                if is_manual:
                    ivfdf_matrix = self.__get_ivfdf_by_vfdf()
                if not ct.np_arr_is_exists(ivfdf_matrix):    
                    return
                self.plot_vfdf_ivfdf(fig, ivfdf_matrix, VRg, VDF)
            else:
                self.plot_vfdf(VRg, VDF)
            plt.show()
        return
    
    def correct_vfdf(self):
        """method for correcting Rg-grid"""
        is_auto = self.__check_mode_auto()
        is_manual = self.__check_mode_manual()
        if is_auto:
            vfdf_matrix = self.__get_vfdf_by_alpha()
        if is_manual:
            vfdf_matrix = self.__get_vfdf_from_memory()
        if not is_auto and not is_manual:    
            messagebox.showwarning(
                "Correct pdf",
                self.mode_err_message
            )
            return  
        if  ct.np_arr_is_exists(vfdf_matrix):
            VRg = vfdf_matrix[:,0]
            VDF = vfdf_matrix[:,3]
            # get current Figure instance
            fig = plt.figure()
            # Plot Distribution
            fig.add_subplot(111)  
            # to set focus into plot window
            fig.canvas.get_tk_widget().focus_force()
            # set window title
            fig.canvas.set_window_title('Setup : Rg-Grid for VFDF-evaluation')
            # set labels
            plt.ylabel('VFDF, $\mathregular{arb.u.}$')
            plt.xlabel('Radius of gyration, $\mathregular{nm}$')
            # set subplot
            vfdf = fig.add_subplot(111)  
            vfdf.grid(True)                                    
            vfdf.semilogx()            
            # Create Object to correction Rg-Grid        
            self.grid_correct_path = os.path.join(cfg.paths["input_data_path"], self.gid_corrected_filename)              
            gc = GridCorrector(VRg, VDF, res_grid_path = self.grid_correct_path)
            # connect to click button_press_event
            plt.connect('button_press_event', gc.on_click)
            # connect to click motion_notify_event
            plt.connect('motion_notify_event', gc.on_move)
            # save to log
            ict.save_log(cfg.paths["log_file_path"], "Correct Rg args grid ")
            # show plot
            plt.show() 
        return

    def upload_vfdf(self):
        """method for uploading result vfdf"""
        is_auto = self.__check_mode_auto()
        is_manual = self.__check_mode_manual()
        if is_auto:
            vfdf_path, ivfdf_path = self.__get_auto_selected_vfdf_ivfdf_paths()
            #vfdf_matrix = self.__get_vfdf_by_alpha()
        if is_manual:
            #vfdf_matrix = self.__get_vfdf_from_memory()
            vfdf_path, ivfdf_path = self.__get_manual_selected_vfdf_ivfdf_paths()
        if not is_auto and not is_manual:    
            messagebox.showwarning(
                "Uploading VFDF data",
                self.mode_err_message
            )
            return  
        if not vfdf_path and not ivfdf_path:    
            messagebox.showwarning(
                "Upload pdf",
                "Can not find VFDF/IVFDF files"
            )
            return  
        elif not ivfdf_path and vfdf_path:
            messagebox.showwarning(
                "Upload ivfdf",
                "Can not find IVFDF"
            )
            return  
        elif not vfdf_path and ivfdf_path:
            messagebox.showwarning(
                "Upload vfdf",
                "Can not find VFDF"
            )
            return  
        self.do_login(vfdf_path)
        ict.save_log(cfg.paths["log_file_path"], "Uploading VFDF on server")
        return
        
    def __check_eval_surface_area(self,vfdf_matrix):
        """check necessary input and params existance"""        
        if not self.anisometer_factor:
            self.vfdf_isset[0] = False
            self.surface_err_message.append("Anisometer factor is not defined")
        if not self.choise:
            self.surface_err_message.append("Shape is not set")
            self.vfdf_isset[0] = False
        self.__check_vfdf_ambiguity(vfdf_matrix, self.vfdf_isset, self.surface_err_message)
                       
    def __get_vfdf_from_memory(self):
        """get vfdf which was manual uploaded"""
        self.__set_vfdf_selected_dir(self.vfdf_manual_selected_path)
        if self.__validate_view_params(self.vfdf_manual_selected_path):
            return self.vfdf
        return None
        
    def __set_vfdf_matrix(self, vfdf_matrix):
        """memorize vfdf which was manual uploaded"""
        self.vfdf = vfdf_matrix             
        
    def eval_surface_area(self):
        """end method for compare file names of intensity and distribution function"""
        self.surface_err_message[:]=[]
        self.vfdf_isset = [True]
        self.anisometer_factor = ict.get_float_from_entry(self.anisometer_factor_entry)
        self.choise = ict.get_string_from_combo(self.shapes_combo)
        
        is_auto = self.__check_mode_auto()
        is_manual = self.__check_mode_manual()
        if is_auto:
            vfdf_matrix = self.__get_vfdf_by_alpha()
        if is_manual:
            vfdf_matrix = self.__get_vfdf_from_memory()
        if not is_auto and not is_manual:    
            messagebox.showwarning(
                "Eval specific surface",
                self.mode_err_message
            )
            return           
        self.__check_eval_surface_area(vfdf_matrix)
                        
        if self.vfdf_isset[0]:
            rg = vfdf_matrix[:,0]
            vfdf = vfdf_matrix[:,3]
            vfdf_ambiguity = vfdf_matrix[:,5]
                                
            surface = Surface(rg, vfdf, vfdf_ambiguity)
            if self.choise == "ellipsoid":
                S = surface.ell(self.anisometer_factor)
            if self.choise == "paralellipiped":
                S = surface.par(self.anisometer_factor)
            if self.choise == "cilindr":
                S = surface.cil(self.anisometer_factor)
            # insert evaluated data into field
            ict.set_location(self.surface_entry, str(S))
            # insert scattering_intens_ambiguity into field
            ict.set_location(self.surface_ambiguity_entry, str(surface.amb))  
            # write to log
            ict.save_log(cfg.paths["log_file_path"], "specific surface area estimation, particle shape:" + self.choise + ";anisometric coef:" + str(self.anisometer_factor))
        else:
            messagebox.showwarning(
                "Eval specific surface",
                "\n".join(self.surface_err_message)
            )                
        return

    def quit(self):
        """close main dialog"""
        self.root.destroy()

    def nb_upload(self, filepath, url,login):
        #ct.ftp_upload(filepath, '92.53.114.211','artemus_saxsev','SAXSEV')
        params = self.params_translate(filepath)
        ct.ftp_upload(filepath, cfg.nb["url"], cfg.nb["login"],self.password_entry.get())

        params = self.params_translate(filepath)
        ct.ftp_translate_params("params.txt", cfg.nb["url"], cfg.nb["login"],self.password_entry.get(), params)
        ct.send_request()
        return

    def do_login(self, path):
        win = Toplevel(self.root)
        win.transient(self.root)
        win.title("Enter Password")
        lm_main = LayoutMaker()
        conn_menu = lm_main.make_lbl_frame(win ,lbl_frame_text="CONNECTO TO SERVER")
        self.password_entry = lm_main.make_entry_grid(conn_menu, pos=0, lbl_text="Password") 
        lm_main.make_btn_grid(conn_menu, row=1, column=1, btn_text="Connect", cmd=lambda: self.nb_upload(path, cfg.nb["url"], cfg.nb["login"]), btn_pady=0,btn_padx=1, btn_width=10)
        conn_menu.pack(fill = X, expand = True, padx = 5, pady = 5)    
        frame = Frame(win)
        frame.pack()   

    def params_translate(self, filepath):
        src_file = os.path.basename(filepath)
        params = src_file[0:src_file.rfind("@")].split('_') 
        Rg = params[len(params)-1].replace('Rg[','').replace(']','')
        RgMin , RgMax = Rg.split(',')
        RgMin = 'RgMin=' + RgMin
        RgMax = 'RgMax=' + RgMax  
        return ['type=' + params[0], 'alpha=' + params[1], params[2], params[3], RgMin,RgMax ]
     

