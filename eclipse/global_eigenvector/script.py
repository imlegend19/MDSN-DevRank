import pickle
import numpy as np
from scipy.linalg import eigh as largest_eigh

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/"
INFLUENCE_MATRIX = "influence_matrix/definition_1/"
ADJACENCY_MATRIX = "adjacency_matrix/definition_1/"


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
    # elif column == 3:
    #     return A4


print("Fetching files...")
A1 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A1_fc.txt"))
A2 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A2_fc.txt"))
A3 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A3_fc.txt"))
# A4 = np.array(fetch_file(RELATIVE_PATH + ADJACENCY_MATRIX + "A4_fc.txt"))
influence_matrix = np.array(fetch_file(RELATIVE_PATH + INFLUENCE_MATRIX + "influence_matrix_fc.txt"))

print(influence_matrix.shape)

krp = []

for i in range(3):
    wa1 = A1 * influence_matrix[i][0]
    wa2 = A2 * influence_matrix[i][1]
    wa3 = A3 * influence_matrix[i][2]
    # wa4 = A4 * influence_matrix[i][3]

    print(influence_matrix[i][0])
    print(influence_matrix[i][1])
    print(influence_matrix[i][2])
    # print(influence_matrix[i][3])

    for j in range(4121):
        row = []

        row.extend(wa1[j])
        row.extend(wa2[j])
        row.extend(wa3[j])
        # row.extend(wa4[j])

        krp.append(row)

print("Clearing variables...")
A1 = None
A2 = None
A3 = None
influence_matrix = None

# print("Calculating eigenvalues...")
# e = np.linalg.eigvals(krp)
#
# mx_eigenvalue = max(e)

val, vec = largest_eigh(krp, eigvals=(4121 - 10, 4120))

# pev = e_vec[ind] / np.linalg.norm(e_vec[ind])
#
# print(pev.shape)
#
# print(pev)
# print(sum(map(lambda x: x.real * x.real, pev)))
#
# print("Saving eigenvector...")
# with open("global_eigenvector_fc.txt", 'wb') as fp:
#     pickle.dump(pev, fp)
#
print("Saving principal eigenvalue...")
with open("principal_eigenvalue_fc.txt", "wb") as fp:
    pickle.dump(mx_eigenvalue, fp)

print("Process finished!")
