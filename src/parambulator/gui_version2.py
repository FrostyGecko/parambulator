#%% Initialize Libraries
#### Import Native/Standard Modules
import numpy as np
import datetime as dt
import pandas as pd
import calendar   
import os
import json
import random
import re
import collections

##### Import GUI Modules
import tkinter as tk 
from tkinter import filedialog, messagebox, ttk, colorchooser

#### Import Plotting Modules
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from itertools import cycle
import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def center(win):
  """
  centers a tkinter window
  :param win: the main window or Toplevel window to center
  """
  win.update_idletasks()
  width                 = win.winfo_width()
  frm_width             = win.winfo_rootx() - win.winfo_x()
  win_width             = width + 2 * frm_width
  height                = win.winfo_height()
  titlebar_height       = win.winfo_rooty() - win.winfo_y()
  win_height            = height + titlebar_height + frm_width
  x                     = win.winfo_screenwidth() // 2 - win_width // 2
  y                     = win.winfo_screenheight() // 2 - win_height // 2
  win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
  win.deiconify()

#%% APPLICATION DataVis
class DataVis(tk.Tk):
    #%%% Build GUI
    def __init__(self):
        super().__init__()
        # self.minsize(width=400, height=25)
        self.wm_title('DataVis - Version 0.1 - Release 20241030')
        self.current_directory  = os.path.dirname(__file__)
        
        #### Defaults
        self.config_file_loaded = False
        self.config_filepath    = 'config/config.json'
        self.dpi_level          = 100
        self.index              = 5

        #### Configuration
        self.self_SetDefaultView()
        self.self_BuildTabs()
        self.self_GridConfig()
        self.self_Build_Tab_DataManagement()
        self.self_LoadConfigurationFile()
        self.self_SetDefaults()
        self.self_Build_Tab_CustomPlot()
        
        #### Data Management
        self.dataframe_set = False
        
        #### Set/Call EOL Function
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.bring_to_front()
        ####
        self.self_WriteTextToDataManagementLog("Dune Successfully Loaded\n Hello Human!\n")
         
    def self_SetDefaults(self):
        #### Set Process Controls              
        #### Plotting Defaults
        self.plot_start_datetime    = dt.datetime(2024, 11, 1,0,0,0)
        self.plot_stop_datetime     = dt.datetime(2025, 11, 1,0,0,0)
        self.vars_checked           = []
        self.low_low                = self.configuration['defaults']["low_temp_warning"]
        self.low                    = self.configuration['defaults']["low_temp_caution"]
        self.high                   = self.configuration['defaults']["high_temp_caution"]
        self.high_high              = self.configuration['defaults']["high_temp_warning"]
        
        self.linestyles     = self.configuration['defaults']["linestyles"]
        self.color_dict     = mcolors.TABLEAU_COLORS
        self.colors         = list(self.color_dict.keys())
        self.markers        = self.configuration['defaults']["markers"]
        self.datatypes      = ["float","datetime","timestamp","timeseries","HRTIMESHADOWENTRYSEC","HRTIMESHADOWENTRYSEC"]
        self.x_axis_types   = ['datetime','timestamp','timeseries','float','unknown']
        self.dataset_types  = ['csv','GMAT-beta-angle-file','GMAT-eclipse-times-file','TD-QFLOW']
        
    def self_BuildTabs(self):
        #### Define Tab Notebook
        self.nb         = ttk.Notebook(self)
        self.nb.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        #### Define Tabs
        self.tab_DataManagement     = tk.Frame(self)
        self.nb.add(self.tab_DataManagement, text = 'Data Management')
        
        self.tab_CustomPlot        = tk.Frame(self)
        self.nb.add(self.tab_CustomPlot, text = 'Custom Plot')

        #### Build Tab List
        self.tab_list   = []
        self.tab_list.append(self.tab_DataManagement)
        self.tab_list.append(self.tab_CustomPlot)

    def self_GridConfig(self):       
        #### Configure Column Weightings
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)

    def self_SetDefaultView(self):
        #### Set Default Window Size on Opening
        # Get Active Screen Dimensions
        active_screen_width     = self.winfo_screenwidth()
        active_screen_height    = self.winfo_screenheight()
        
        # Calculate Geometry for window
        geometry_str            = str(round(active_screen_width*.85))+'x'+str(round(active_screen_height*.85))
        
        # Set self (Root) Geometry
        self.geometry(geometry_str)
        
    def self_LoadConfigurationFile(self,filepath=None,user_select=False,**args):
        if filepath is None:
            filepath = self.config_filepath
            
        if user_select is True:
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")],initialdir = self.current_directory)
            
        try:
            self.configuration      = self.load_config_file(filepath)
            self.config_file_loaded = True
            self.self_WriteTextToDataManagementLog(f'Configuration file loaded from {self.config_filepath}\n')
            self.self_WriteTextToDataManagementLog(f'{self.configuration}\n')
            self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.config(state='normal')
            self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.delete(1.0,tk.END)
            self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.insert(tk.END,self.config_filepath)
            self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.config(state='disabled')
            
        except Exception as e:
            self.self_WriteTextToDataManagementLog('ERROR: could not load configuration file\n {e}\n')
            self.nb.select(0)
            self.bring_to_front()
    
    #%% TAB: DataManagement
    def self_Build_Tab_DataManagement(self):
        #### Configuration SubFrame
        self.tab_DataManagement_SF_config   = ttk.Frame(self.tab_DataManagement,borderwidth=2, relief="solid")
        self.tab_DataManagement_SF_config.grid(row=0, column=0,sticky="nsew")
        
        self.tab_DataManagement_SF_config_config_sub_frame_label         = tk.Label(self.tab_DataManagement_SF_config,
                                               text='Configuration Management',
                                               font=("Arial",20,"bold italic underline"))
        self.tab_DataManagement_SF_config_config_sub_frame_label.grid(row=0,column=0,columnspan=3,sticky='news') 
        
        self.tab_DataManagement_SF_config_label_LoadedConfig = tk.Label(self.tab_DataManagement_SF_config,
                                              text="Imported Configuration File:",
                                              font=("Arial",16,"bold"))
        self.tab_DataManagement_SF_config_label_LoadedConfig.grid(row=1,column=0,sticky='news') 
        
        self.tab_DataManagement_SF_config_text_LoadedConfigFilepath     = tk.Text(self.tab_DataManagement_SF_config,height = 3)
        self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.grid(row=1,column=1,sticky='news') 
        self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.insert(tk.END, self.config_filepath)
        self.tab_DataManagement_SF_config_text_LoadedConfigFilepath.config(state='disabled')
        
        self.tab_DataManagement_SF_config_button_SelectNewConfig         =ttk.Button(self.tab_DataManagement_SF_config,
                                                command=lambda: self.self_LoadConfigurationFile(user_select=True),
                                                text="Select New Config File", )
        self.tab_DataManagement_SF_config_button_SelectNewConfig.grid(row=1,column=2,sticky='news')
        
        self.tab_DataManagement_SF_config_button_SetDefaultConfig         =ttk.Button(self.tab_DataManagement_SF_config,
                                                text="Set Current Config File as Default", )
        self.tab_DataManagement_SF_config_button_SetDefaultConfig.grid(row=2,column=1,columnspan=2,sticky='news')
    
        tk.Grid.columnconfigure(self.tab_DataManagement_SF_config,1,weight=1)
        
        #### Log Window Subframe
        self.tab_DataManagement_SF_log      = ttk.Frame(self.tab_DataManagement,borderwidth=2, relief="solid",width=100)
        self.tab_DataManagement_SF_log.grid(row=0, column=1,rowspan=2,sticky="nsew")
        
        self.tab_DataManagement_SF_log_text = tk.Text(self.tab_DataManagement_SF_log,state='disabled',width=100)
        self.tab_DataManagement_SF_log_text.grid(column=0, row=0,sticky="nsew")
        
        self.detached_window                = None
        self.detached_text_window           = None
        
        self.tab_DataManagement_SF_log_button_LogDetach =ttk.Button(self.tab_DataManagement_SF_log,command=self.self_DetachDataManagementSFLog,text="Detached Log Window", )
        self.tab_DataManagement_SF_log_button_LogDetach.grid(row=1,column=0,sticky='nsew')
        
        # Create a scrollbar and associate it with the Text widget
        scrollbar = tk.Scrollbar(self.tab_DataManagement_SF_log, orient="vertical", command=self.tab_DataManagement_SF_log_text.yview)
        scrollbar.grid(column=1, row=0, rowspan =2, sticky="ns")
        self.tab_DataManagement_SF_log_text.configure(yscrollcommand=scrollbar.set)
        
        tk.Grid.rowconfigure(self.tab_DataManagement_SF_log, 0, weight=1)
        tk.Grid.columnconfigure(self.tab_DataManagement_SF_log,0,weight=1)

                
        #### Configure Tab Grid Weights
        tk.Grid.rowconfigure(self.tab_DataManagement, 1, weight=1)
        tk.Grid.columnconfigure(self.tab_DataManagement,0,weight=1)
        tk.Grid.columnconfigure(self.tab_DataManagement,1,weight=1)
        
    def self_DetachDataManagementSFLog(self):
        self.detached_window = tk.Toplevel(self)
        self.detached_window.title("Detached Text Window")
        self.detached_text_window = tk.Text(self.detached_window)
        self.detached_text_window.grid(row=0,column=0,sticky='news')
        
        scrollbar = tk.Scrollbar(self.detached_window, orient="vertical", command=self.detached_text_window.yview)
        scrollbar.grid(row=0,column=1,sticky='ns')
        self.detached_text_window.configure(yscrollcommand=scrollbar.set)
        
        tk.Grid.columnconfigure(self.detached_window,0,weight=1)
        tk.Grid.rowconfigure(self.detached_window,0,weight=1)
        
        self.detached_text_window.insert(tk.END, self.tab_DataManagement_SF_log_text.get("1.0", tk.END))
        self.detached_text_window.config(state='disabled')
        
    def self_WriteTextToDataManagementLog(self,message):
        current_time    = dt.datetime.now()
        time_str        = current_time.strftime(self.configuration['config']['default_datetime'])
        message         = time_str+': '+message+"\n"
        
        self.tab_DataManagement_SF_log_text.config(state='normal')
        self.tab_DataManagement_SF_log_text.insert(tk.END,message)
        self.tab_DataManagement_SF_log_text.config(state='disabled')
        self.tab_DataManagement_SF_log_text.see(tk.END)
        
        if self.detached_text_window:
            self.detached_text_window.config(state='normal')
            self.detached_text_window.insert(tk.END, message)
            self.detached_text_window.config(state='disabled')
            self.detached_text_window.see(tk.END)
    
    #%% Workspace Management
    def save_workspace(self,auto=False):
        if not os.path.exists('workspaces/'):
            # Create the directory
            os.makedirs('workspaces/')
            
        if auto:

            current_time    = dt.datetime.now()
            time_str        = current_time.strftime('%Y%m%d%H%M%S')
            filepath       = f"workspaces/{time_str}_workspace.pkl"
            
        else:
            filepath = filedialog.asksaveasfilename(
                            defaultextension=".pkl",
                            filetypes=[("Pickle Files", "*.pkl")],
                            initialdir=self.configuration['default folders']['workspaces'],
                            initialfile="workspace.pkl",
                            title="Save File"
                            )
            
        try:
            self.dataframe.to_pickle(filepath)
            self.self_WriteTextToDataManagementLog(f"SUCCESS: Saved workspace to {filepath}\n")
        except Exception as e:
            self.self_WriteTextToDataManagementLog(f"FAILED: Failed to save workspace to {filepath}\n {e}\n")
            self.nb.select(0)
            self.bring_to_front()
            
    #%% Other Functions             
    def Window_Input_num(self,value,min_value = None,max_value = None,prompt = "Input New",setting = '',unit=''):
        WindowInput = tk.Tk()
        windowWidth = WindowInput.winfo_reqwidth()
        windowHeight = WindowInput.winfo_reqheight()
        positionRight = int(WindowInput.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(WindowInput.winfo_screenheight()/2 - windowHeight/2)
        WindowInput.geometry("+{}+{}".format(positionRight, positionDown))  

        WindowInput.withdraw()
        WindowInput.update_idletasks()
        
        prompt = 'Current '+setting+' '+str(value)+'. '+unit +' '+ prompt+' '+setting+' '+unit
        
        USER_INP = tk.simpledialog.askinteger(parent = WindowInput,title = '',prompt=prompt)
        WindowInput.destroy()
        
        if USER_INP is not None:
            if min_value is not None and USER_INP < min_value:
                tk.messagebox.showwarning(title='Error Box',message='ERROR: Cannot set '+setting+' less than '+str(min_value)+' '+unit)
                return value
            if max_value is not None and USER_INP > max_value:
                tk.messagebox.showwarning(title='Error Box',message='ERROR: Cannot set '+setting+' greater than '+str(max_value)+' '+unit)
                return value
            
            user_message = setting+' changed to '+str(USER_INP)+' '+unit
            tk.messagebox.showinfo(title='User Message', message=user_message)
            return USER_INP
        else:
            return value
      
    def OpenDatasetManagement(self):
        OpenDatasetManagementApp = DatasetManagement(self)
        OpenDatasetManagementApp.wait_window(OpenDatasetManagementApp)
        
    def load_config_file(self,config_filepath = 'config/config.json'):
        with open(config_filepath) as cf_file:
            config = json.loads(cf_file.read())
        return config

    def save_config_file(self,config):
        with open('config/config.json','w') as cf_file:
            json.dump(config,cf_file)
            
    def bring_to_front(self):
        self.lift()
        self.focus_force()
            
    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            will_close = 1
            
            if will_close == 1:
                self.save_workspace(auto=True)
                self.self_WriteTextToDataManagementLog('Quitting DUNE')
                current_time    = dt.datetime.now()
                time_str        = current_time.strftime('%Y%m%d%H%M%S')
                
                contents        = self.tab_DataManagement_SF_log_text.get("1.0", tk.END)
                
                if not os.path.exists('log/'):
                    # Create the directory
                    os.makedirs('log/')
                    
                with open(f"log/{time_str}.txt", "w") as f:
                    # Write the contents to the file
                    f.write(contents)
    
                self.destroy()
            else:
                pass
            
                 
#%% Launch App
if __name__ == '__main__':
    app = DataVis()
    center(app)
    app.mainloop()