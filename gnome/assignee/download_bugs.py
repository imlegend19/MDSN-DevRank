import pickle
from urllib import request

with open("ndbugs.txt", 'rb') as fp:
    list_bugs = pickle.load(fp)

url = "https://bugzilla.gnome.org/show_activity.cgi?id="

nd = []

cnt = len(list_bugs)
for i in list_bugs:
    print("Remaining", cnt)

    try:
        request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
        cnt -= 1
    except Exception:
        nd.append(i)

print(nd)
