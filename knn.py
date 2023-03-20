import matplotlib.pyplot as plt
import csv
import math
import colorama
from matplotlib.lines import Line2D
import tabulate
from collections import OrderedDict
from os import path, system, getenv, listdir
import numpy as np
import dotenv
import tkinter as tk
import customtkinter as ctk


colorama.init()

dotenv.load_dotenv("settings.env", verbose=True)

default_delimiter = getenv('default_delimiter')

default_k = getenv('default_k')
default_filename = getenv("default_filename")
default_plot_show = getenv("default_plot_show")

show_tkinter = getenv("show_tkinter")
use_custon_tkinter = getenv("use_custon_tkinter")





class Application():
    """
    The .svg file must be is this form:
    
    
        The first column must be the names of the possibilities
            ▼
    +=================+==============+==============+==============+
    ‖ Name            ‖   Caracter 1 |   Caracter 2 |   Caracter n ‖   <- The first row must be the titles of the columns
    +=================+==============+==============+==============+
    ‖ aaaaaaaaaaa     ‖       50     |    2.8124    |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       22     |    2.84454   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ aaaaaaaaaaa     ‖       2*0     |    3.69878   |      ...    ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       31     |    3.69878   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       24     |    3.69878   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ x               ‖       50     |    3.69878   |      ...     ‖   <- The last row must be the searched item, 
    +=================+==============+==============+==============+      which name must be x or X or / or ?
    """
    def __init__(self, k:int=int(default_k) if isinstance(default_k, int) else 5,
                 file_name:str=default_filename if isinstance(default_filename, str) and default_filename != "" else "iris-2d",
                 show_plot:bool=default_plot_show if isinstance(default_plot_show, str) else "True",
                 colors:tuple=(colorama.Fore.RESET)
                 ):
        
        RED, CYAN, LIGHTBLUE_EX, RESET, BLUE, MAGENTA = colors
        
        
        system("cls")
        plt.close()
            
        
        self.data = []
        
        
        def plot(mode):
            
            x = [x[2][0] for x in self.data]
            y = [y[2][1] for y in self.data]
            if mode == "3d":
                z = [z[2][2] for z in self.data]
            names = list(dict.fromkeys([x[0] for x in self.data]))

            colors = ["black", "green", "red", "blue", "yellow", "brown", "orange"]
            name_colors = []

            for name in [x[0] for x in self.data]:
                name_colors.append(colors[names.index(name)])

            if mode == "2d":
                points_list = list(zip(x, y, name_colors))
                ax = plt.axes()
                self.scatter = plt.scatter(x = [float(x[0]) for x in points_list], y = [float(y[1]) for y in points_list], c = [c[2] for c in points_list])
                circle = plt.Circle((float(self.x[list(self.x.keys())[1]]), float(self.x[list(self.x.keys())[2]])), radius=self.data[k][1], alpha=0.1)
                plt.gca().add_artist(circle)
                ax.set_aspect("equal")

            elif mode == "3d":
                points_list = list(zip(x, y, z, name_colors))
                ax = plt.axes(projection ="3d")
                self.scatter = ax.scatter3D(xs = [float(x[0]) for x in points_list], ys = [float(y[1]) for y in points_list], zs = [float(z[2]) for z in points_list], c = [c[3] for c in points_list])

                pi = np.pi
                cos = np.cos
                sin = np.sin
                phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
                x = self.data[k][1]*sin(phi)*cos(theta) + float(self.x[list(self.x.keys())[1]])
                y = self.data[k][1]*sin(phi)*sin(theta) + float(self.x[list(self.x.keys())[2]])
                z = self.data[k][1]*cos(phi) + float(self.x[list(self.x.keys())[3]])
                ax.plot_surface(x, y, z, rstride=1, cstride=1, color='c', alpha=0.1, linewidth=0)
                ax.set_aspect("equal")
            



            custom_lines = [Line2D([], [], color='w', markerfacecolor=colors[i], marker='o', markersize=8) for i in range(len(list(OrderedDict.fromkeys([name[0] for name in self.data]))))]
            
            data_sigle_name = []
            for name, *args in self.data:
                data_sigle_name.append(name)
                
            i = 0
            for point in self.data[:k+1]:
                if i<=k:
                    if mode == "2d":
                        plt.plot((float(self.x[list(self.x.keys())[1]]), float(point[2][0])), (float(self.x[list(self.x.keys())[2]]), float(point[2][1])), '--', color=name_colors[i], alpha=0.4)
                    elif mode == "3d":
                        plt.plot((float(self.x[list(self.x.keys())[1]]), float(point[2][0])), (float(self.x[list(self.x.keys())[2]]), float(point[2][1])), (float(self.x[list(self.x.keys())[3]]), float(point[2][2])) , '--', color=name_colors[i], alpha=0.4)
                    i+=1

            plt.legend(custom_lines, list(OrderedDict.fromkeys(data_sigle_name)))
            
            plt.show()
        
        def distance_to_x(x, caracts):
            s = 0
            for i in range(len(caracts)):
                s += (float(x[i]) - float(caracts[i]))**2
            return math.sqrt(s)
        
        def knn(k):
            result_dict = {}
            result_number = {}
            i = 0
            for name, dist, caracts in self.data:
                if name not in "xX/?" and i<k:
                    i+=1
                    result_dict[name] = 0
                    result_number[name] = 0
            i = 0
            for name, dist, caracts in self.data:
                if name not in "xX/?" and i<k:
                    i+=1
                    result_dict[name] += dist
                    result_number[name] += 1
            for name in result_dict.keys():
                result_dict[name] /= result_number[name]
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]))
            
            output_text = [[f"{colorama.Style.BRIGHT}{CYAN}Name{RESET}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{LIGHTBLUE_EX}Points{RESET}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{BLUE}Distance{RESET}{colorama.Style.RESET_ALL}"]]
            
            for n, v in [(name, result_dict[name]) for name in result_dict.keys()]:
                output_text.append((f"{CYAN}{n}{RESET}", f"{LIGHTBLUE_EX}{result_number[n]}{RESET}", f"{BLUE}{v}{RESET}"))

            characts_list = []
            cols = 4
            x_keys = list(self.x.keys())[1:]
            x_keys_len = len(x_keys)//cols
            if len(x_keys) % cols !=0:
                x_keys_len+=1
            for i in range(x_keys_len):
                characts_list.append(x_keys[i*cols:(i+1)*cols])

            print(
f'''
{RED}K: {BLUE}{k}
{RED}Output: {BLUE}{colorama.Style.BRIGHT}{list(result_dict.keys())[0]}{colorama.Style.RESET_ALL}

{RED}Possibilities: {BLUE}{", ".join(list(result_dict.keys()))}
{RED}Characteristics:\n{BLUE}{tabulate.tabulate(characts_list, tablefmt='grid')}

{MAGENTA}Results by possibility:{RESET}'''
)
            print(tabulate.tabulate(output_text,headers='firstrow',tablefmt='grid'))
            
        
        
        with open(f"{path.dirname(__file__)}\\tables\\{file_name}.csv", "r", encoding="utf8") as self.csv_file_path:
            self.csv_file = csv.DictReader(self.csv_file_path, delimiter=default_delimiter if isinstance(default_delimiter,str) and default_delimiter != "" else ";")
            self.csv_file = [i for i in self.csv_file]
            self.x = self.csv_file[-1]
            for line in self.csv_file:
                if line[list(line.keys())[-1]] != "x":
                    name, *caracts = line.keys()
                    self.data.append((line[name], distance_to_x([self.x[caract] for caract in caracts], [line[caract] for caract in caracts]), [line[caract] for caract in caracts]))

            self.data.sort(key=lambda a: a[1])
            
            if k>len(self.data):
                k = len(self.data)-1
            
            knn(k)
            if show_plot == "True":
                if len(self.x)-1 <= 2:
                    plot("2d")
                elif len(self.x)-1 == 3:
                    plot("3d")
                else:
                    print(f"\n\n{RED}More than 3 characteristics: cannot be displayed in a 2D  or 3D graphic{RESET}")
            

            

class Tk_Application():
    def __init__(self):
        self.show_plot = "True"

        try:
            self.file_name = [file for file in listdir(f"{path.dirname(__file__)}\\tables")][0]
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
            if self.k_entry.get() != "" and self.k_entry.get().isdigit():
                self.k = int(self.k_entry.get())
            if self.show_plot_var.get() == 1:
                self.show_plot = "True"
            else:
                self.show_plot = "False"
            Application(k=self.k, file_name=self.file_name[:-4], show_plot=self.show_plot, colors=(self.RED, self.CYAN, self.LIGHTBLUE_EX, self.RESET, self.BLUE, self.MAGENTA))
        
        
        self.root = tk.Tk()
        self.root.title("Settings")
        self.root.geometry("200x115")
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
            command=lambda: (system("cls"), print(Application.__doc__))
        )

        

        self.k_frame = tk.Frame(self.root)
        self.k_frame.grid(row=0, column=0, sticky="we")
        self.k_label = tk.Label(self.k_frame, text="K:")
        self.k_label.pack(side="left")
        self.k_entry = tk.Entry(self.k_frame)
        self.k_entry.pack(side="right", padx=10)
        
        
        def get_file_name_optionmenu(value):
            self.file_name = value
        

        self.file_name_frame = tk.Frame(self.root)
        self.file_name_frame.grid(row=1, column=0, sticky="we")
        self.file_name_label = tk.Label(self.file_name_frame, text="Filename:")
        self.file_name_label.pack(side="left")
        optionmenu_var = tk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables")][0])
        self.file_name_optionmenu = tk.OptionMenu(self.file_name_frame,
                                                  optionmenu_var,
                                                  *[file for file in listdir(f"{path.dirname(__file__)}\\tables")],
                                                  command=get_file_name_optionmenu
                                                  )
        self.file_name_optionmenu.pack(side="left", padx=5, pady=5)



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
        
        
        
        self.root.mainloop()
    
    

class CTk_Application():
    def __init__(self):
        self.show_plot = "True"

        try:
            self.file_name = [file for file in listdir(f"{path.dirname(__file__)}\\tables")][0]
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
            if self.k_entry.get() != "" and self.k_entry.get().isdigit():
                self.k = int(self.k_entry.get())
            if self.show_plot_var.get() == 1:
                self.show_plot = "True"
            else:
                self.show_plot = "False"
            Application(k=self.k, file_name=self.file_name[:-4], show_plot=self.show_plot, colors=(self.RED, self.CYAN, self.LIGHTBLUE_EX, self.RESET, self.BLUE, self.MAGENTA))
            

        self.root = ctk.CTk()
        self.root.title("Settings")
        self.root.geometry("300x160")
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
        self.help_button = ctk.CTkButton(self.optionmenu_frame, text="Help", command=lambda:(system("cls"), print(Application.__doc__)))
        self.help_button.pack(side="right", padx=5, pady=5)


        self.k_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.k_frame.grid(row=1, column=0, sticky="we")
        self.k_label = ctk.CTkLabel(self.k_frame, text="K:")
        self.k_label.pack(side="left", padx=5)
        self.k_entry = ctk.CTkEntry(self.k_frame)
        self.k_entry.pack(side="right", padx=5)
        
        
        def get_file_name_optionmenu(value):
            self.file_name = value
        
        self.file_name_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.file_name_frame.grid(row=2, column=0, sticky="we")
        self.file_name_label = ctk.CTkLabel(self.file_name_frame, text="Filename:")
        self.file_name_label.pack(side="left", padx=5)
        optionmenu_var = ctk.StringVar(value=[file for file in listdir(f"{path.dirname(__file__)}\\tables")][0])
        self.file_name_optionmenu = ctk.CTkOptionMenu(self.file_name_frame,
                                       values=[file for file in listdir(f"{path.dirname(__file__)}\\tables")],
                                       command=get_file_name_optionmenu,
                                       variable=optionmenu_var)
        self.file_name_optionmenu.pack(side="left", padx=5, pady=5)


        self.show_plot_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.show_plot_frame.grid(row=3, column=0, sticky=tk.W)
        self.show_plot_label = ctk.CTkLabel(self.show_plot_frame, text="Show the plot:")
        self.show_plot_label.pack(side="left", padx=5)
        self.show_plot_var = ctk.IntVar(value=1)
        self.show_plot_switch = ctk.CTkSwitch(self.show_plot_frame, variable=self.show_plot_var, text="")
        self.show_plot_switch.pack()
        
        
        self.use_colors_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        self.use_colors_frame.grid(row=4, column=0, sticky=tk.W)
        self.use_colors_label = ctk.CTkLabel(self.use_colors_frame, text="Show the results in color:")
        self.use_colors_label.pack(side="left", padx=5)
        self.use_colors_var = ctk.IntVar(value=1)
        self.use_colors_checkbutton = ctk.CTkSwitch(self.use_colors_frame, variable=self.use_colors_var)
        self.use_colors_checkbutton.pack()

        
        self.root.mainloop()
        
      



system("cls")
if use_custon_tkinter == "True":
    CTk_Application()
else:
    Tk_Application()
