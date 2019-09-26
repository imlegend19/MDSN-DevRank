import pickle


def open_file(path):
    with open(path, 'rb') as f:
        ed = pickle.load(f)

    return ed


if __name__ == '__main__':
    PATH = "definition_1/"
    PATH2 = "definition_2/"

    l1 = open_file(PATH + "layer1_edges_fc.txt")
    l2 = open_file(PATH + "layer2_edges_fc.txt")
    l3 = open_file(PATH + "layer3_edges_fc.txt")
    l4 = open_file(PATH + "layer4_edges_fc.txt")
    l2_d2 = open_file(PATH2 + "layer2_edges_fc.txt")

    edges = set(list(l1) + list(l2) + list(l3) + list(l4) + list(l2_d2))

    print(len(edges))
    print(len(l1), len(l2), len(l3), len(l4), len(l2_d2))

    with open("edges_comb.txt", 'wb') as fp:
        pickle.dump(list(edges), fp)
