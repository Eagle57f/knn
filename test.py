import tabulate

t = tabulate.tabulate((["efkoef", 1, True], ), tablefmt='grid')

print(t)

import os, csv
file_name = "table"
with open(f"{os.path.dirname(__file__)}\\{file_name}.csv", "r", encoding="utf8") as csv_file_path:
    csv_file = csv.DictReader(csv_file_path, delimiter=";")
    
    print([i for i in csv_file])
    
    print([i for i in csv_file])