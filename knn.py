import matplotlib.pyplot as plt
import csv
import math
import colorama
from matplotlib.lines import Line2D
import tabulate
from collections import OrderedDict
from os import path, system

colorama.init()

class Application():
    def __init__(self, show_plot:bool=True, k:int=5):
        system("cls")
        
        self.data = []
        self.x = list(csv.DictReader(open(f"{path.dirname(__file__)}\\Iris.csv", "r", encoding="utf8"), delimiter=";"))[-1]
        
        def plot():
                x = [x[2][0] for x in self.data]
                y = [y[2][1] for y in self.data]
                names = list(dict.fromkeys([x[0] for x in self.data]))

                colors = ["black", "green", "red", "blue", "yellow", "brown", "orange"]
                name_colors = []

                for name in [x[0] for x in self.data]:
                    name_colors.append(colors[names.index(name)])


                points_list = list(zip(x, y, name_colors))


                self.scatter = plt.scatter(x = [float(x[0]) for x in points_list], y = [float(y[1]) for y in points_list], c = [c[2] for c in points_list])
                
                circle = plt.Circle((float(self.x[list(self.x.keys())[1]]), float(self.x[list(self.x.keys())[2]])), radius=self.data[k][1], alpha=0.1)
                plt.gca().add_artist(circle)


                custom_lines = [Line2D([], [], color='w', markerfacecolor=colors[i], marker='o', markersize=8) for i in range(len(list(OrderedDict.fromkeys([name[0] for name in self.data]))))]
                
                data_sigle_name = []
                for name, *args in self.data:
                    data_sigle_name.append(name)
                 
                i = 0
                for point in self.data[:k+1]:
                    if i<=k:

                        plt.plot((float(self.x[list(self.x.keys())[1]]), float(point[2][0])), (float(self.x[list(self.x.keys())[2]]), float(point[2][1])), '--', color=name_colors[i], alpha=0.4)
                        i+=1

                plt.legend(custom_lines, list(OrderedDict.fromkeys(data_sigle_name)))
                
                plt.show(),
        
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
            print(
f'''
{colorama.Fore.RED}K: {colorama.Fore.BLUE}{k}
{colorama.Fore.RED}Output: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}{list(result_dict.keys())[0]}{colorama.Style.RESET_ALL}

{colorama.Fore.RED}Possibilities: {colorama.Fore.BLUE}{", ".join(list(result_dict.keys()))}
{colorama.Fore.RED}Characteristics: {colorama.Fore.BLUE}{", ".join(list(self.x.keys())[1:])}

{colorama.Fore.MAGENTA}Results by possibility:{colorama.Fore.WHITE}'''
)
            print(tabulate.tabulate(output_text,headers='firstrow',tablefmt='grid'))
            
        
        
        with open(f"{path.dirname(__file__)}\\Iris.csv", "r", encoding="utf8") as self.csv_file_path:
            self.csv_file = csv.DictReader(self.csv_file_path, delimiter=";")
            for line in self.csv_file:
                if line[list(line.keys())[-1]] != "x":
                    name, *caracts = line.keys()
                    self.data.append((line[name], distance_to_x([self.x[caract] for caract in caracts], [line[caract] for caract in caracts]), [line[caract] for caract in caracts]))

            self.data.sort(key=lambda a: a[1])
            knn(k)
            if show_plot:
                if len(self.x)-1 <= 2:
                    plot()
                else:
                    print(f"\n\n{colorama.Fore.RED}More than 2 characteristics: cannot be displayed in a 2D graphic{colorama.Fore.WHITE}")
            
            
            
Application(k=20, show_plot=True)


