import colorama
from os import path, system, listdir


import customtkinter as ctk

# ------------------------------------------
from Custom_CTkMessagebox import CTkMessagebox
from Custom_CTkSpinbox import CTkSpinbox
# ------------------------------------------


class CTk_Application():
    def __init__(self, app, default_k):
        self.show_plot = "True"
        self.delimiter = ";"

        try:
            self.file_name = [file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0]
        except IndexError:
            print("No .csv file(s) in /tables")
            exit()
        except FileNotFoundError:
            print("No 'tables' folder")
            exit()

        self.k = 20
        self.RED = colorama.Fore.RED
        self.CYAN = colorama.Fore.CYAN
        self.LIGHTBLUE_EX = colorama.Fore.LIGHTBLUE_EX
        self.RESET = colorama.Fore.RESET
        self.BLUE = colorama.Fore.BLUE
        self.MAGENTA = colorama.Fore.MAGENTA
        
        def app_launch():
            if self.use_colors_var.get() == 0:
                self.RED = self.CYAN = self.LIGHTBLUE_EX = self.RESET = self.BLUE = self.MAGENTA = colorama.Fore.RESET
            else:
                self.RED = colorama.Fore.RED
                self.CYAN = colorama.Fore.CYAN
                self.LIGHTBLUE_EX = colorama.Fore.LIGHTBLUE_EX
                self.RESET = colorama.Fore.RESET
                self.BLUE = colorama.Fore.BLUE
                self.MAGENTA = colorama.Fore.MAGENTA
            if self.k_spinbox.get() != "" and str(self.k_spinbox.get()).isdigit():
                self.k = int(self.k_spinbox.get())
            if self.show_plot_var.get() == 1:
                self.show_plot = "True"
            else:
                self.show_plot = "False"
            
            if str(self.k_spinbox.get()).isdigit():
                try:
                    open(f"{path.dirname(__file__)}\\tables\\{self.file_name[:-4]}.csv", "r", encoding="utf8")
                    try:
                        app(k=self.k, file_name=self.file_name[:-4], show_plot=self.show_plot, colors=(self.RED, self.CYAN, self.LIGHTBLUE_EX, self.RESET, self.BLUE, self.MAGENTA), delimiter=self.delimiter)
                    except Exception:
                        CTkMessagebox(title="", message=f"Error while reading '{self.file_name}' with delimiter '{self.delimiter}'.\nMaybe the delimiter is wrong or the file isn't correct.", border_color="#efb700", border_width=2,
                                        icon="warning", corner_radius=0, width=400, button_width=120)
                except FileNotFoundError:
                    CTkMessagebox(title="", message=f"{self.file_name} not found. Maybe the file was deleted while this program is running? (Menu refreshed)", border_color="#efb700", border_width=2,
                                        icon="warning", corner_radius=0, width=400, button_width=120)
                    self.file_name_optionmenu.configure(values=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"], variable=ctk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0]))
                    
            else:
                CTkMessagebox(title="", message="K value is not integer", border_color="#efb700", border_width=2,
                                        icon="warning", corner_radius=0, width=400, button_width=120)

        self.root = ctk.CTk()
        self.root.title("Settings")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        
        
        def get_optionmenu(value):
            self.optionmenu.set("Actions")
            if value == "Launch":
                app_launch()
            elif value == "Exit":
                self.root.destroy()


        self.optionmenu_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.optionmenu_frame.grid(row=0, column=0, sticky="nw")
        self.optionmenu = ctk.CTkOptionMenu(master=self.optionmenu_frame,
                                       values=["Launch", "Exit"],
                                       command=get_optionmenu)
        self.optionmenu.pack(side="left", padx=5, pady=5)
        self.optionmenu.set("Actions")
        self.help_button = ctk.CTkButton(self.optionmenu_frame, text="Help", command=lambda:(system("cls"), print(app.__doc__)))
        self.help_button.pack(side="right", padx=5, pady=5)


        self.k_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.k_frame.grid(row=1, column=0, sticky="we")
        self.k_label = ctk.CTkLabel(self.k_frame, text="K:")
        self.k_label.pack(side="left", padx=5)
        self.k_var = ctk.StringVar(value=default_k)
        self.k_spinbox = CTkSpinbox(self.k_frame, width=110, step_size=1)
        self.k_spinbox.pack(side="left", padx=5)
        self.k_spinbox.set(default_k)
        
        
        def get_file_name_optionmenu(value):
            self.file_name = value
        
        self.file_name_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.file_name_frame.grid(row=2, column=0, sticky="we")
        self.file_name_label = ctk.CTkLabel(self.file_name_frame, text="Filename:")
        self.file_name_label.pack(side="left", padx=5)
        self.file_name_optionmenu_var = ctk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0])
        self.file_name_optionmenu = ctk.CTkOptionMenu(self.file_name_frame,
                                       values=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"],
                                       command=get_file_name_optionmenu,
                                       variable=self.file_name_optionmenu_var,
                                       dynamic_resizing=False)
        self.file_name_optionmenu.pack(side="left", padx=5, pady=5)
        self.file_name_refresh_button = ctk.CTkButton(self.file_name_frame, text="Refresh", width=70,
                                                      command=lambda:self.file_name_optionmenu.configure(values=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"],
                                                                                                  variable=ctk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0])))
        self.file_name_refresh_button.pack(side="left", padx=5, pady=5)


        self.show_plot_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.show_plot_frame.grid(row=3, column=0, sticky=ctk.W)
        self.show_plot_label = ctk.CTkLabel(self.show_plot_frame, text="Show the plot:")
        self.show_plot_label.pack(side="left", padx=5)
        self.show_plot_var = ctk.IntVar(value=1)
        self.show_plot_switch = ctk.CTkSwitch(self.show_plot_frame, variable=self.show_plot_var, text="")
        self.show_plot_switch.pack()
        
        
        self.use_colors_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.use_colors_frame.grid(row=4, column=0, sticky=ctk.W)
        self.use_colors_label = ctk.CTkLabel(self.use_colors_frame, text="Show the results in color:")
        self.use_colors_label.pack(side="left", padx=5)
        self.use_colors_var = ctk.IntVar(value=1)
        self.use_colors_checkbutton = ctk.CTkSwitch(self.use_colors_frame, variable=self.use_colors_var, text="")
        self.use_colors_checkbutton.pack()
        
        
        
        def get_delimiter_optionmenu(value):
            self.delimiter = value
        
        self.delimiter_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.delimiter_frame.grid(row=5, column=0, sticky="we")
        self.delimiter_label = ctk.CTkLabel(self.delimiter_frame, text=".csv file delimiter:")
        self.delimiter_label.pack(side="left", padx=5)
        self.delimiter_optionmenu_var = ctk.StringVar(value=";")
        self.delimiter_optionmenu = ctk.CTkOptionMenu(self.delimiter_frame,
                                       values=[";", ","],
                                       command=get_delimiter_optionmenu,
                                       variable=self.delimiter_optionmenu_var,
                                       dynamic_resizing=False,
                                       width=50)
        self.delimiter_optionmenu.pack(side="left", padx=5, pady=5)

        
        self.root.mainloop()