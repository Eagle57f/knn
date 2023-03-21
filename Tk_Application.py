import colorama
from os import path, system, listdir
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showwarning


class Tk_Application():
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
            if self.k_var.get() != "" and self.k_var.get().isdigit():
                self.k = int(self.k_var.get())
            if self.show_plot_var.get() == 1:
                self.show_plot = "True"
            else:
                self.show_plot = "False"
                
            if self.k_var.get().isdigit():
                try:
                    open(f"{path.dirname(__file__)}\\tables\\{self.file_name[:-4]}.csv", "r", encoding="utf8")
                    try:
                        app(k=self.k, file_name=self.file_name[:-4], show_plot=self.show_plot, colors=(self.RED, self.CYAN, self.LIGHTBLUE_EX, self.RESET, self.BLUE, self.MAGENTA), delimiter=self.delimiter)
                    except Exception:
                        system("cls")
                        showwarning(title="Error !", message=f"Error while reading '{self.file_name}' with delimiter '{self.delimiter}'")

                except FileNotFoundError:
                    showwarning(title="Error !", message=f"{self.file_name} not found. Maybe the file was deleted while this program is running? (Menu refreshed)")
                    self.optionmenu_var.set([file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0])
                    self.file_name_optionmenu['menu'].delete(0, 'end')
                    for item in [file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"]:
                        self.file_name_optionmenu['menu'].add_command(label=item, command=tk._setit(tk.StringVar(), item))
            else:
                showwarning(title="Error !", message="K value is not integer")
        
        self.root = tk.Tk()
        self.root.title("Settings")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)


        actions_menu = tk.Menu(menubar, tearoff=False)
        actions_menu.add_command(
            label='Launch',
            command=app_launch
        )
        actions_menu.add_separator()
        actions_menu.add_command(
            label='Exit',
            command=self.root.destroy
        )
        menubar.add_cascade(
            label="Actions",
            menu=actions_menu
        )

        menubar.add_command(
            label='Help',
            command=lambda: (system("cls"), print(app.__doc__))
        )

        

        self.k_frame = tk.Frame(self.root)
        self.k_frame.grid(row=0, column=0, sticky="we")
        self.k_label = tk.Label(self.k_frame, text="K:")
        self.k_label.pack(side="left")
        self.k_var = tk.StringVar(value=default_k)
        self.k_spinbox = ttk.Spinbox(self.k_frame, from_=1, to=9999, textvariable=self.k_var, width=5)
        self.k_spinbox.pack(side="left")
        
        
        def get_file_name_optionmenu(value):
            self.file_name = value
        

        self.file_name_frame = tk.Frame(self.root)
        self.file_name_frame.grid(row=1, column=0, sticky="we")
        self.file_name_label = tk.Label(self.file_name_frame, text="Filename:")
        self.file_name_label.pack(side="left")
        self.optionmenu_var = tk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0])
        self.file_name_optionmenu = tk.OptionMenu(self.file_name_frame,
                                                  self.optionmenu_var,
                                                  *[file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"],
                                                  command=get_file_name_optionmenu
                                                  )
        self.file_name_optionmenu.configure(width=15)
        self.file_name_optionmenu.pack(side="left", padx=5, pady=5)

        def refresh_file_name():
            self.optionmenu_var.set([file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"][0])
            self.file_name_optionmenu['menu'].delete(0, 'end')
            for item in [file for file in listdir(f"{path.dirname(__file__)}\\tables") if file[-4:] == ".csv"]:
                self.file_name_optionmenu['menu'].add_command(label=item, command=tk._setit(tk.StringVar(), item))

        self.file_name_refresh_button = tk.Button(self.file_name_frame, text="Refresh", width=10, command=refresh_file_name)
        self.file_name_refresh_button.pack(side="left", padx=5, pady=5)



        self.show_plot_frame = tk.Frame(self.root)
        self.show_plot_frame.grid(row=2, column=0, sticky=tk.W)
        self.show_plot_label = tk.Label(self.show_plot_frame, text="Show the plot:")
        self.show_plot_label.pack(side="left")
        self.show_plot_var = tk.IntVar(value=1)
        self.show_plot_checkbutton = tk.Checkbutton(self.show_plot_frame, variable=self.show_plot_var)
        self.show_plot_checkbutton.pack()
        

        self.use_colors_frame = tk.Frame(self.root)
        self.use_colors_frame.grid(row=3, column=0, sticky=tk.W)
        self.use_colors_label = tk.Label(self.use_colors_frame, text="Show the results in color:")
        self.use_colors_label.pack(side="left")
        self.use_colors_var = tk.IntVar(value=1)
        self.use_colors_checkbutton = tk.Checkbutton(self.use_colors_frame, variable=self.use_colors_var)
        self.use_colors_checkbutton.pack()
        
        
        
        def get_delimiter_optionmenu(value):
            self.delimiter = value
        
        self.delimiter_frame = tk.Frame(self.root)
        self.delimiter_frame.grid(row=5, column=0, sticky="we")
        self.delimiter_label = tk.Label(self.delimiter_frame, text=".csv file delimiter:")
        self.delimiter_label.pack(side="left", padx=5)
        self.optionmenu_var = tk.StringVar(value=";")
        self.delimiter_optionmenu = tk.OptionMenu(self.delimiter_frame,
                                                  self.optionmenu_var,
                                                  *[";", ","],
                                                  command=get_delimiter_optionmenu)
        self.file_name_optionmenu.configure(width=10)
        self.delimiter_optionmenu.pack(side="left", padx=5, pady=5)
        
        
        
        self.root.mainloop()