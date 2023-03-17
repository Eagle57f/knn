import matplotlib.pyplot as plt
import csv
import math
import colorama
from matplotlib.lines import Line2D
import tabulate
from collections import OrderedDict
from os import path

colorama.init()

class Application():
    def __init__(self, show_plot:bool=True, k:int=5):
        
        self.data = []
        self.x = list(csv.DictReader(open(f"{path.dirname(__file__)}\\table.csv", "r", encoding="utf8"), delimiter=";"))[-1]
        
        def plot():
                x = [x[2][0] for x in self.data]
                y = [y[2][1] for y in self.data]
                names = list(dict.fromkeys([x[0] for x in self.data]))

                colors = ["green", "red", "blue", "yellow"]
                name_colors = []
                for name in [x[0] for x in self.data]:
                    name_colors.append(colors[names.index(name)])

                points_list = list(zip(x, y, name_colors))


                self.scatter = plt.scatter(x = [int(x[0]) for x in points_list], y = [int(y[1]) for y in points_list], c = [c[2] for c in points_list])
                
                circle = plt.Circle((int(self.x[list(self.x.keys())[1]]), int(self.x[list(self.x.keys())[2]])), radius=self.data[k][1], alpha=0.3)
                plt.gca().add_artist(circle)


                custom_lines = [Line2D([], [], color='w', markerfacecolor=name_colors[i], marker='o', markersize=8) for i in range(len({name[0] for name in self.data}))]
                
                data_sigle_name = []
                for name, *args in self.data:
                    data_sigle_name.append(name)
                
                plt.legend(custom_lines, list(OrderedDict.fromkeys(data_sigle_name)))
                
                plt.show()
        
        def distance_to_x(x, caracts):
            s = 0
            for i in range(len(caracts)):
                s += (int(x[i]) - int(caracts[i]))**2
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
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]))
            
            output_text = [[f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Name{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}Points{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}", f"{colorama.Style.BRIGHT}{colorama.Fore.BLUE}Distance{colorama.Fore.WHITE}{colorama.Style.RESET_ALL}"]]
            
            for n, v in [(name, result_dict[name]) for name in result_dict.keys()]:
                output_text.append((f"{colorama.Fore.CYAN}{n}{colorama.Fore.WHITE}", f"{colorama.Fore.LIGHTBLUE_EX}{result_number[n]}{colorama.Fore.WHITE}", f"{colorama.Fore.BLUE}{v}{colorama.Fore.WHITE}"))
            print(
f'''
{colorama.Fore.RED}K: {colorama.Fore.BLUE}{k}
{colorama.Fore.RED}Output: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}{list(result_dict.keys())[0]}{colorama.Style.RESET_ALL}
{colorama.Fore.RED}Possibilités: {colorama.Fore.BLUE}{", ".join(list(result_dict.keys()))}

{colorama.Fore.MAGENTA}Résultats par possibilité:{colorama.Fore.WHITE}'''
)
            print(tabulate.tabulate(output_text,headers='firstrow',tablefmt='grid'))
            
        
        
        with open(f"{path.dirname(__file__)}\\table.csv", "r", encoding="utf8") as self.csv_file_path:
            self.csv_file = csv.DictReader(self.csv_file_path, delimiter=";")

            for line in self.csv_file:
                if line[list(line.keys())[-1]] != "x":
                    name, *caracts = line.keys()
                    self.data.append((line[name], distance_to_x([self.x[caract] for caract in caracts], [line[caract] for caract in caracts]), [line[caract] for caract in caracts]))

            self.data.sort(key=lambda a: a[1])
            knn(k)
            if show_plot:
                plot()
            
            
            
Application(k=2, show_plot=True)



"""
TODO: add a legend -> https://qastack.fr/programming/19125722/adding-a-legend-to-pyplot-in-matplotlib-in-the-simplest-manner-possible
"""
