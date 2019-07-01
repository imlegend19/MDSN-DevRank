import pickle
from local_settings import db

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/edges/"
TOTAL = 0
relative_ids = {}

with db:
    cur = db.cursor()
    print("Fetching relative id's...")
    cur.execute("SELECT id, who_id FROM who_ids_commenting_on_more_than_10_bugs")

    for i in cur.fetchall():
        relative_ids[i[1]] = i[0]
        TOTAL += 1


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
    path = RELATIVE_PATH + "layer" + str(i) + "_edges.txt"

    print("Fetching edges...")
    with open(path, "rb") as fp:
        edges = pickle.load(fp)

    print("Creating matrix...")
    matrix = []
    for j in range(TOTAL):
        matrix.append([0 for _ in range(TOTAL)])

    print("Creating adjacency matrix...")
    for j in edges:
        x, y = j[0], j[1]
        matrix[relative_ids[x]][relative_ids[y]] = 1

    print("Calculating transpose...")
    matrix_new = transpose(matrix)

    print("Dumping matrix...")
    with open('A' + str(i) + '.txt', 'wb') as file:
        pickle.dump(matrix_new, file)

print("Process Complete!")
