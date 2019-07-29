import pickle
from urllib import request

with open("not_downloaded_bugs.txt", 'rb') as fp:
    list_bugs = pickle.load(fp)
cnt = len(list_bugs)
for i in list_bugs:
    print("Remaining", cnt)
    lst = i.split("=")
    d = lst[1]
    print(id)
    request.urlretrieve(i, "bug_html/" + str(d) + ".html")
    cnt -= 1
