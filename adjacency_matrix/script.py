import pickle

RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/edges/"

for i in range(1, 5):
    path = RELATIVE_PATH + "layer" + str(i) + "_edges.txt"

    print("Fetching edges...")
    with open(path, "rb") as fp:
        edges = pickle.load(fp)

    print("Fetching relative edges...")
    path = RELATIVE_PATH + "relative_id.txt"
    with open(path, "rb") as fp:
        relative_edges = pickle.load(fp)

    total = len(edges)

    print("Creating matrix...")
    matrix = []
    for j in range(total):
        matrix.append([0 for _ in range(total)])

    print("Creating adjacency matrix...")
    for j in edges:
        x, y = j[0], j[1]
        matrix[relative_edges[x]][relative_edges[y]] = 1

    print("Dumping matrix...")
    with open('A1.txt', 'wb') as file:
        pickle.dump(matrix, file)
