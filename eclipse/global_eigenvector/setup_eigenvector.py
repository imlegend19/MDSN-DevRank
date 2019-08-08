import pickle

url = '/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/global_eigenvector/EigenVector/' \
      'definition_2/global_eigenvector_fc.txt'

TOTAL_WHO = 146

with open(url, 'rb') as fp:
    ge = pickle.load(fp)

print(ge)

ev_centrality = []
who = [x for x in range(TOTAL_WHO)]

for i in range(TOTAL_WHO):
    ev_centrality.append(ge[i].real + ge[i + TOTAL_WHO].real
                         + ge[i + (TOTAL_WHO * 2)].real)

z = [x for (y, x) in sorted(zip(ev_centrality, who), key=lambda pair: pair[0], reverse=True)]
# print(z)

ev_centrality.sort(reverse=True)
# print(ev_centrality)

with open('/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/adjacency_matrix/relative_id.txt',
          'rb') as fp:
    rel_id = pickle.load(fp)

relative_id = {v: k for k, v in rel_id.items()}

final_ev_who = {}
for i in range(TOTAL_WHO):
    final_ev_who[relative_id[z[i]]] = abs(ev_centrality[i])

with open('global_ev_dict.txt', 'wb') as fp:
    pickle.dump(final_ev_who, fp)

print(final_ev_who)

print("Process Finished!")
