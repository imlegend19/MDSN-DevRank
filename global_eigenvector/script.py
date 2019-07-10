import pickle
import bz2

import numpy as np

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/"
INFLUENCE_MATRIX = "influence_matrix/"
ADJACENCY_MATRIX = "adjacency_matrix/"


def fetch_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def fetch_adj_mat(column):
    if column == 0:
        return A1
    elif column == 1:
        return A2
    elif column == 2:
        return A3
    elif column == 3:
        return A4
    elif column == 4:
        return A5
    elif column == 5:
        return A6


def scalar_multiplication(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                matrix[i][j] = scalar

    return matrix


print("Fetching files...")
A1 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A1_fc.txt"))
A2 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A2_fc.txt"))
A3 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A3_fc.txt"))
A4 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A4_fc.txt"))
A5 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A5_fc.txt"))
A6 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A6_fc.txt"))
influence_matrix = np.array(fetch_file(RELATIVE_PATH + INFLUENCE_MATRIX + "influence_matrix_fc.txt"))

krp = []
for i in range(6):
    krp.append([0 for _ in range(6)])

for i in range(6):
    for j in range(6):
        print("Ongoing w" + str(i) + str(j))
        if i == j:
            krp[i][j] = fetch_adj_mat(j)
        else:
            krp[i][j] = fetch_adj_mat(j) * influence_matrix[i][j]

print("Clearing variables...")
A1 = None
A2 = None
A3 = None
A4 = None
A5 = None
A6 = None
influence_matrix = None

print("Setting up kr_product...")
kr_product = np.array(krp, dtype=np.float)
krp.clear()

print("Calculating eigenvector...")
e = np.linalg.eig(kr_product)

e_val = e[0]
e_vec = e[1]

print("Total eigenvalues:", len(e_val))

print("Saving compressed eigenvector...")
for i in range(len(e_vec)):
    compressed_file = bz2.BZ2File("global_ev_" + str(i) + "_fc.txt", 'wb')
    pickle.dump(e_vec[i], compressed_file)

print("Saving eigenvalues...")
count = 1
for i in e_val:
    print("Ongoing", count)
    with open("eigenvalue_" + str(count) + "_fc.txt", "wb") as fp:
        pickle.dump(i, fp, protocol=2)

    count += 1

print("Process finished!")
