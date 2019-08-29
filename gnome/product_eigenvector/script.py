import pickle
import openpyxl
from gnome.layers.layer1 import layer1
from gnome.layers.layer3 import layer3
from gnome.layers.layer4 import layer4

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/edges_normal/definition_2/"
TIME_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/bug_time/product_avg_time.txt"
PRODUCTS = [90, 186, 214, 76, 13, 34, 279, 39, 239, 87]

wb = openpyxl.Workbook()
sheet = wb.active

sheet.append(["Product", "Average Time", "Layer 1", "Layer 3", "Layer 4"])
sheet.append(["" for i in range(5)])

with open(TIME_PATH, 'rb') as fp:
    avg_time = pickle.load(fp)

print(avg_time)

for i in PRODUCTS:
    print("Ongoing product :", i)
    l1_ec = layer1(i)
    l3_ec = layer3(i)
    l4_ec = layer4(i)

    sheet.append([i, avg_time[i], l1_ec, l3_ec, l4_ec])

print("Saving...")
wb.save("product_avg.xlsx")
