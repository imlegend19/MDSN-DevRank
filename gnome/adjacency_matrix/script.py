import pickle

import numpy as np

from local_settings import db

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/edges/definition_2/"
TOTAL = 0
relative_ids = {}

with db:
    cur = db.cursor()
    print("Fetching relative id's...")
    cur.execute("SELECT distinct who_id FROM test_comment_fixed_closed")

    who_ids = []
    for i in cur.fetchall():
        who_ids.append(i[0])

    who_ids.sort()

    for i in who_ids:
        relative_ids[i] = TOTAL
        TOTAL += 1

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

    # print("Dumping matrix...")
    # with open('A' + str(i) + '_fc.txt', 'wb') as file:
    #     pickle.dump(matrix_new, file)

    e_val, e_vec = np.linalg.eig(np.array(matrix_new))

    max_e_val = max(e_val)
    print(max_e_val)
    ind = list(e_val).index(max_e_val)

    pev = e_vec[ind] / np.linalg.norm(e_vec[ind])

    print(sum(pev))


print("Process Complete!")