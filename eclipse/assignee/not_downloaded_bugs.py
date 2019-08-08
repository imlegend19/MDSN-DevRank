import pickle
from urllib import request

with open("not_downloaded_bugs.txt", 'rb') as fp:
    list_bugs = pickle.load(fp)

url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="

cnt = len(list_bugs)
for i in list_bugs:
    print("Remaining", cnt)

    request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
    cnt -= 1
