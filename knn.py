import matplotlib.pyplot as plt
import csv
import math
import colorama

colorama.init()

class Application():
    def __init__(self, show_plot:bool=True):
        
        self.data = []
        self.x = list(csv.DictReader(open("table.csv", "r", encoding="utf8"), delimiter=";"))[-1]
        
        def plot():
                x = [x[2][0] for x in self.data]
                y = [y[2][1] for y in self.data]
                names = list(dict.fromkeys([x[0] for x in self.data]))
                colors = ["green", "red", "blue", "yellow"]
                name_colors = []
                for name in [x[0] for x in self.data]:
                    name_colors.append(colors[names.index(name)])
                    
                points_list = list(zip(x, y, name_colors))

                plt.scatter(x = [int(x[0]) for x in points_list], y = [int(y[1]) for y in points_list], c = [c[2] for c in points_list])
                plt.show()
        
        def distance_to_x(x, caracts):
            s = 0
            for i in range(len(caracts)):
                s += (int(x[i]) - int(caracts[i]))**2
            return math.sqrt(s)
        
        def knn(k):
            result_dict = {}
            i = 0
            for name, dist, caracts in self.data:
                if name not in "xX/?" and i<k:
                    i+=1
                    result_dict[name] = 0
            i = 0
            for name, dist, caracts in self.data:
                if name not in "xX/?" and i<k:
                    i+=1
                    result_dict[name] += dist

            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]))
            output_text = ""
            for n, v in [(name, result_dict[name]) for name in result_dict.keys()]:
                output_text += f"{colorama.Fore.CYAN}{n}: {colorama.Fore.WHITE}{v}\n"
            print(
f'''
{colorama.Fore.RED}Output: {colorama.Fore.BLUE}{colorama.Style.BRIGHT}{list(result_dict.keys())[0]}{colorama.Style.RESET_ALL}
{colorama.Fore.RED}Possibilités: {colorama.Fore.BLUE}{", ".join(list(result_dict.keys()))}

{colorama.Fore.MAGENTA}Résultats par possibilité:
{output_text}
'''
)
        
        
        with open("table.csv", "r", encoding="utf8") as self.csv_file_path:
            self.csv_file = csv.DictReader(self.csv_file_path, delimiter=";")

            for line in self.csv_file:
                if line[list(line.keys())[-1]] != "x":
                    name, *caracts = line.keys()
                    self.data.append((line[name], distance_to_x([self.x[caract] for caract in caracts], [line[caract] for caract in caracts]), [line[caract] for caract in caracts]))

            self.data.sort(key=lambda a: a[1])

            if show_plot:
                plot()
            knn(2)
            
            
Application()