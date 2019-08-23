import pickle
from urllib import request

nd_ids = ["nd7135", "nd28928", "nd49435", "nd82038", "nd122415", "nd169305", "nd214041"]

nd_len = []
for i in nd_ids:
    with open(i + ".txt", 'rb') as fp:
        x = pickle.load(fp)

    nd_len.append(len(x))

for i in range(len(nd_len)):
    print(nd_ids[i], ":", nd_len[i])

print("Total:", sum(nd_len))

with open("nd169305.txt", 'rb') as fp:
    x = pickle.load(fp)
    url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="

    for i in x:
        print(i)
        request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
