import pickle
import openpyxl

print("Setting up excel sheet...")

with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_1/layer1_edges_fc.txt',
          'rb') as fp:
    e1 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_1/layer2_edges_fc.txt',
          'rb') as fp:
    e2d1 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_1/layer3_edges_fc.txt',
          'rb') as fp:
    e3 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_1/layer4_edges_fc.txt',
          'rb') as fp:
    e4 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_2/layer2_edges_fc.txt',
          'rb') as fp:
    e2d2 = list(pickle.load(fp))

print("Saving...")


lst = ['1', '2_d1', '2_d2', '3', '4']
func = [e1, e2d1, e2d2, e3, e4]

# for i in range(len(func)):
#     wb = openpyxl.Workbook()
#     sheet = wb.active
#
#     sheet.append(["Source", "Target"])
#
#     for j in func[i]:
#         sheet.append([j[0], j[1]])
#
#     print(len(func[i]))
#
#     wb.save("layer" + lst[i] + ".xlsx")

edges = set(list(e1) + list(e2d1) + list(e2d2) + list(e3) + list(e4))

wb = openpyxl.Workbook()
sheet = wb.active

sheet.append(["Source", "Target"])

for j in edges:
    sheet.append([j[0], j[1]])

print(len(edges))

wb.save("combined_edges.xlsx")
