import pickle
from local_settings_eclipse import db
import openpyxl

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/edges/2009-2010/definition_1/"


def fetch_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def get_layer_who(layer):
    lw = set()
    for i in layer:
        lw.add(i[0])
        lw.add(i[1])

    return lw


def get_isolated_who(layer, dev):
    iw = []
    for i in dev:
        if i not in layer:
            iw.append(i)

    return set(iw)


l1 = get_layer_who(fetch_file(RELATIVE_PATH + 'layer1_edges_fc.txt'))
l2 = get_layer_who(fetch_file(RELATIVE_PATH + 'layer2_edges_fc.txt'))
l3 = get_layer_who(fetch_file(RELATIVE_PATH + 'layer3_edges_fc.txt'))
l4 = get_layer_who(fetch_file(RELATIVE_PATH + 'layer4_edges_fc.txt'))

with db:
    cur = db.cursor()
    cur.execute("SELECT DISTINCT who FROM test_longdescs_fixed_closed GROUP BY who")

    w = []
    for i in cur.fetchall():
        w.append(i[0])

    cur.execute('SELECT DISTINCT who, COUNT(DISTINCT bug_id) FROM longdescs GROUP BY who')
    dev = {}
    for i in cur.fetchall():
        dev[i[0]] = i[1]

    who = {}
    for i in w:
        who[i] = dev[i]

iso_l1 = get_isolated_who(l1, who.keys())
iso_l2 = get_isolated_who(l2, who.keys())
iso_l3 = get_isolated_who(l3, who.keys())
iso_l4 = get_isolated_who(l4, who.keys())

wb = openpyxl.Workbook()
sheet = wb.active

titles = ["Isolated Who", "Bug Count"]

sheet.append(titles)
sheet.append(["" for i in range(len(titles))])

print(len(iso_l1))
print(len(iso_l2))
print(len(iso_l3))
print(len(iso_l4))

isolated_who = list(iso_l1.union(iso_l2, iso_l3, iso_l4))

for i in range(len(isolated_who)):
    sheet.append([isolated_who[i], who[isolated_who[i]]])

wb.save("isolated_who.xlsx")
print("Finished!")
