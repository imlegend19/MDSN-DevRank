import pickle
from urllib import request
with open("not_downloaded_bugs.txt",'rb') as fp:
    list_bugs=pickle.load(fp)
cnt=len(list_bugs)
for i in list_bugs:

        print("Remaining",cnt)
        list=i.split("=")
        id=list[1]
        print(id)
        request.urlretrieve(i,"bug_html/"+str(id)+".html")
        cnt-=1

