import pickle
import openpyxl

print("Setting up excel sheet...")
wb = openpyxl.Workbook()
sheet = wb.active

with open('/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_1/layer1_edges_fc.txt',
          'rb') as fp:
    e1 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_1/layer2_edges_fc.txt',
          'rb') as fp:
    e2d1 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_1/layer3_edges_fc.txt',
          'rb') as fp:
    e3 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_1/layer4_edges_fc.txt',
          'rb') as fp:
    e4 = list(pickle.load(fp))

with open('/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_2/layer2_edges_fc.txt',
          'rb') as fp:
    e2d2 = list(pickle.load(fp))

edges = list(set(e1 + e2d1 + e2d2 + e3 + e4))

for i in edges:
    sheet.append([i[0], i[1]])

print("Saving...")
wb.save("combined_edges.xlsx")
