import pickle
import numpy as np

RELATIVE_PATH = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/"
INFLUENCE_MATRIX = "influence_matrix/definition_2/"
ADJACENCY_MATRIX = "adjacency_matrix/definition_2/"
TOTAL_WHO = 1905


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


print("Fetching files...")
A1 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A1_fc.txt"))
A2 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A2_fc.txt"))
A3 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A3_fc.txt"))
A4 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A4_fc.txt"))
influence_matrix = np.array(fetch_file(RELATIVE_PATH + INFLUENCE_MATRIX + "influence_matrix_fc.txt"))

print(influence_matrix.shape)

krp = []

for i in range(4):
    wa1 = A1 * influence_matrix[i][0]
    wa2 = A2 * influence_matrix[i][1]
    wa3 = A3 * influence_matrix[i][2]
    wa4 = A4 * influence_matrix[i][3]

    print(influence_matrix[i][0])
    print(influence_matrix[i][1])
    print(influence_matrix[i][2])
    print(influence_matrix[i][3])

    for j in range(TOTAL_WHO):
        row = []

        row.extend(wa1[j])
        row.extend(wa2[j])
        row.extend(wa3[j])
        row.extend(wa4[j])

        krp.append(row)

print("Clearing variables...")
A1 = None
A2 = None
A3 = None
A4 = None
influence_matrix = None

print("Setting up kr_product...")
kr_product = np.array(krp, dtype=np.float)
krp.clear()

print(kr_product.shape)
print(kr_product)

print("Calculating eigenvalues...")
e = np.linalg.eig(kr_product)

e_val = e[0]
e_vec = e[1]

mx_ev_index = list(e_val).index(max(e_val))
print(mx_ev_index)

pev = e_vec[mx_ev_index] / np.linalg.norm(e_vec[mx_ev_index])

print(pev.shape)

print(sum(map(lambda x: x.real * x.real, pev)))

print("Saving eigenvector...")
with open("global_eigenvector_fc.txt", 'wb') as fp:
    pickle.dump(pev, fp)

print("Saving principal eigenvalue...")
with open("principal_eigenvalue_fc.txt", "wb") as fp:
    pickle.dump(e_val[mx_ev_index], fp)

print("Process finished!")
