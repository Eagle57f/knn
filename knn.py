import matplotlib.pyplot as plt
import csv
import math
import colorama
from matplotlib.lines import Line2D
import tabulate
from collections import OrderedDict
from os import path, system
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

colorama.init()

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
    def __init__(self, k:int=5, file_name:str="table", show_plot:bool=True):
        system("cls")

            
        
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
            
            output_text = [[f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Name{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}Points{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{colorama.Fore.BLUE}Distance{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}"]]
            
            for n, v in [(name, result_dict[name]) for name in result_dict.keys()]:
                output_text.append((f"{colorama.Fore.CYAN}{n}{colorama.Fore.WHITE}", f"{colorama.Fore.LIGHTBLUE_EX}{result_number[n]}{colorama.Fore.WHITE}", f"{colorama.Fore.BLUE}{v}{colorama.Fore.WHITE}"))

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
{colorama.Fore.RED}K: {colorama.Fore.BLUE}{k}
{colorama.Fore.RED}Output: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}{list(result_dict.keys())[0]}{colorama.Style.RESET_ALL}

{colorama.Fore.RED}Possibilities: {colorama.Fore.BLUE}{", ".join(list(result_dict.keys()))}
{colorama.Fore.RED}Characteristics:\n{colorama.Fore.BLUE}{tabulate.tabulate(characts_list, tablefmt='grid')}

{colorama.Fore.MAGENTA}Results by possibility:{colorama.Fore.WHITE}'''
)
            print(tabulate.tabulate(output_text,headers='firstrow',tablefmt='grid'))
            
        
        
        with open(f"{path.dirname(__file__)}\\tables\\{file_name}.csv", "r", encoding="utf8") as self.csv_file_path:
            self.csv_file = csv.DictReader(self.csv_file_path, delimiter=";")
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
            if show_plot:
                if len(self.x)-1 <= 2:
                    plot("2d")
                elif len(self.x)-1 == 3:
                    plot("3d")
                else:
                    print(f"\n\n{colorama.Fore.RED}More than 3 characteristics: cannot be displayed in a 2D  or 3D graphic{colorama.Fore.WHITE}")
            
            
            


system("cls")
print("Example: execute Application(k=80, show_plot=True, file_name='iris')")


while True:
    response = input(f"\n{colorama.Fore.BLUE}Commande:  ")
    if response == "exit":
        break
    elif response == "help":
        system("cls")
        print(f"{colorama.Fore.RESET}", end="")
        print(Application.__doc__)
        print("Example: execute Application(k=80, show_plot=True, file_name='iris')")
    elif "execute" in response:
        system("cls")
        print(f"{colorama.Fore.RESET}", end="")
        print(response[8:])
        exec(response[8:])
    elif response == "2d":
        system("cls")
        print(f"{colorama.Fore.RESET}", end="")
        Application(k=80, show_plot=True, file_name='iris')
    elif response == "3d":
        system("cls")
        print(f"{colorama.Fore.RESET}", end="")
        Application(k=5)