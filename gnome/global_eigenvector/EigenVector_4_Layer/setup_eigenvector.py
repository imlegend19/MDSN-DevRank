import pickle

url = '/home/imlegend19/PycharmProjects/Research - Data Mining/gnome/global_eigenvector_normal/EigenVector/' \
      'definition_2/global_eigenvector_fc.txt'

with open(url, 'rb') as fp:
    ge = pickle.load(fp)

print(ge)

ev_centrality = []
who = [x for x in range(1134)]

for i in range(1134):
    ev_centrality.append(ge[i].real + ge[i + 1134].real
                         + ge[i + (1134 * 2)].real + ge[i + (1134 * 3)].real)

z = [x for (y, x) in sorted(zip(ev_centrality, who), key=lambda pair: pair[0], reverse=True)]
# print(z)

ev_centrality.sort(reverse=True)
# print(ev_centrality)

with open('/home/imlegend19/PycharmProjects/Research - Data Mining/gnome/adjacency_matrix_normal/relative_id.txt',
          'rb') as fp:
    rel_id = pickle.load(fp)

relative_id = {v: k for k, v in rel_id.items()}

final_ev_who = {}
for i in range(1134):
    final_ev_who[relative_id[z[i]]] = abs(ev_centrality[i])

with open('global_ev_dict.txt', 'wb') as fp:
    pickle.dump(final_ev_who, fp)

print(final_ev_who)

print("Process Finished!")
