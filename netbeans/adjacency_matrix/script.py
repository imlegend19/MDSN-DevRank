import pickle

from local_settings_netbeans import db

RELATIVE_PATH = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_2/"
TOTAL = 0
relative_ids = {}

with db:
    cur = db.cursor()
    print("Fetching relative id's...")
    cur.execute("select distinct who from test_longdescs_fixed_closed")

    who_ids = []
    for i in cur.fetchall():
        who_ids.append(i[0])

    who_ids.sort()

    for i in who_ids:
        relative_ids[i] = TOTAL
        TOTAL += 1

print(TOTAL)

print("Saving relative id's...")
with open("relative_id.txt", 'wb') as fp:
    pickle.dump(relative_ids, fp)


def transpose(a):
    b = []
    for j in range(TOTAL):
        b.append([0 for _ in range(TOTAL)])

    for i in range(TOTAL):
        for j in range(TOTAL):
            b[i][j] = a[j][i]

    return b


print("Matrix dimensions:", TOTAL, "x", TOTAL)

for i in range(1, 5):
    path = RELATIVE_PATH + "layer" + str(i) + "_edges_fc.txt"

    print("Fetching edges_normal...")
    with open(path, "rb") as fp:
        edges = pickle.load(fp)

    print("Creating matrix...")
    matrix = []
    for j in range(TOTAL):
        matrix.append([0 for _ in range(TOTAL)])

    print("Creating adjacency matrix...")
    for j in edges:
        x, y = j[0], j[1]
        # print(x, y)
        matrix[relative_ids[x]][relative_ids[y]] = 1

    print("Calculating transpose...")
    matrix_new = transpose(matrix)

    print("Dumping matrix...")
    with open('A' + str(i) + '_fc.txt', 'wb') as file:
        pickle.dump(matrix_new, file)

print("Process Complete!")
