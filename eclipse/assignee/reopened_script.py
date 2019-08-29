import pickle
from bs4 import BeautifulSoup
from local_settings_eclipse import db

not_downloaded_bugs = []
with db:
    print("Connected to db...")

    cur = db.cursor()

    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed")

    assignee_bug = {}
    for i in cur.fetchall():
        if i[1] in assignee_bug:
            lst = set(assignee_bug[i[1]])
            lst.add(i[0])
            assignee_bug[i[1]] = list(lst)
        else:
            assignee_bug[i[1]] = [i[0]]

    # print(len(assignee_bug))
    # print(assignee_bug)
    #
    # with open("assignee_bug.txt", 'wb') as fp:
    #     pickle.dump(assignee_bug, fp)

    bugs = set()
    for i in assignee_bug.values():
        for j in i:
            bugs.add(j)

    assignee_reopened_cnt = {}

    main_cnt = len(bugs)
    for i in bugs:
        print("Ongoing bug:", i, "Remaining :", main_cnt)
        main_cnt -= 1

        with open('bug_html/' + str(i) + '.html', 'r') as fp:
            html = fp.read()

        soup = BeautifulSoup(html, features="html.parser")

        div = soup.find("div", attrs={"id": "bugzilla-body"})
        table = div.find("table")

        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        # print(headings)

        data = []
        for row in table.find_all("tr")[1:]:
            dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
            data.append(dataset)
            # print(dataset)

        assignee = None
        for j in assignee_bug:
            if i in assignee_bug[j]:
                assignee = j
                break

        for k in data:
            if 'REOPENED' in k:
                if assignee in assignee_reopened_cnt:
                    reopened = assignee_reopened_cnt[assignee][0]
                    tot = assignee_reopened_cnt[assignee][1]
                    assignee_reopened_cnt[assignee] = [reopened + 1, tot + 1]
                else:
                    assignee_reopened_cnt[assignee] = [1, 1]
            else:
                if assignee in assignee_reopened_cnt:
                    reopened = assignee_reopened_cnt[assignee][0]
                    tot = assignee_reopened_cnt[assignee][1]
                    assignee_reopened_cnt[assignee] = [reopened, tot + 1]
                else:
                    assignee_reopened_cnt[assignee] = [0, 1]

    print("Saving...")
    with open("assignee_reopened.txt", 'wb') as fp:
        pickle.dump(assignee_reopened_cnt, fp)

    print(assignee_reopened_cnt)

    print("Process Complete!")
