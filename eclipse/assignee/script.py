import pickle
from dateutil import parser
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

    print(len(assignee_bug))
    print(assignee_bug)

    with open("assignee_bug.txt", 'wb') as fp:
        pickle.dump(assignee_bug, fp)

    print(len(assignee_bug))

    # url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="

    with open('bugs.txt', 'rb') as fp:
        samp = pickle.load(fp)

    bugs = set()
    for i in assignee_bug.values():
        for j in i:
            if j in samp:
                bugs.add(j)

    assignee_fixed_time = {}
    assignee_reopened_cnt = {}
    assignee_first_fixed_time = {}

    main_cnt = len(bugs)
    ndbugs = []
    for i in bugs:
        print("Ongoing bug:", i, "Remaining :", main_cnt)
        main_cnt -= 1
        try:
            with open('bug_html/' + str(i) + '.html', 'r') as fp:
                html = fp.read()

            soup = BeautifulSoup(html, features="html.parser")

            div = soup.find("div", attrs={"id": "bugzilla-body"})
            table = div.find("table")

            headings = [th.get_text() for th in table.find("tr").find_all("th")]
        except Exception:
            ndbugs.append(i)

        # print(headings)

        data = []
        for row in table.find_all("tr")[1:]:
            dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
            data.append(dataset)
            # print(dataset)

        # print(data)

        if 'EST' in data[0][1]:
            assigned_time = parser.parse(data[0][1], tzinfos={'EST': -5 * 3600})
        else:
            assigned_time = parser.parse(data[0][1], tzinfos={'EDT': -5 * 3600})

        it = -1
        try:
            while True:
                if len(data[it]) == 5:
                    if 'CLOSED' in data[it]:
                        break
                    else:
                        it -= 1
                elif len(data[it]) == 3:
                    if 'CLOSED' in data[it]:
                        it -= 1
                        while True:
                            if len(data[it]) == 5:
                                break
                            else:
                                it -= 1
                        break
                    else:
                        it -= 1

            if 'EST' in data[it][1]:
                finished_time = parser.parse(data[it][1], tzinfos={'EST': -5 * 3600})
            else:
                finished_time = parser.parse(data[it][1], tzinfos={'EDT': -5 * 3600})

            assignee = None
            for j in assignee_bug:
                if i in assignee_bug[j]:
                    assignee = j
                    break

            if assignee in assignee_fixed_time:
                time = assignee_fixed_time[assignee][0] + (finished_time - assigned_time)
                cnt = assignee_fixed_time[assignee][1] + 1

                assignee_fixed_time[assignee] = [time, cnt]
            else:
                assignee_fixed_time[assignee] = [finished_time - assigned_time, 1]

        except IndexError:
            pass

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

        if 'EST' in data[0][1]:
            assigned_time = parser.parse(data[0][1], tzinfos={'EST': -5 * 3600})
        else:
            assigned_time = parser.parse(data[0][1], tzinfos={'EDT': -5 * 3600})

        try:
            for k in data:
                if len(k) == 5:
                    if 'EST' in k[1]:
                        finished_time = parser.parse(k[1], tzinfos={'EST': -5 * 3600})
                    else:
                        finished_time = parser.parse(k[1], tzinfos={'EDT': -5 * 3600})
                if 'CLOSED' in k:
                    if len(k) == 3:
                        break
                    else:
                        if 'EST' in k[1]:
                            finished_time = parser.parse(k[1], tzinfos={'EST': -5 * 3600})
                        else:
                            finished_time = parser.parse(k[1], tzinfos={'EDT': -5 * 3600})
                        break
        except Exception:
            if len(data[-1]) == 3:
                if 'EST' in data[-2][1]:
                    finished_time = parser.parse(data[-2][1], tzinfos={'EST': -5 * 3600})
                else:
                    finished_time = parser.parse(data[-2][1], tzinfos={'EDT': -5 * 3600})
            else:
                if 'EST' in data[-1][1]:
                    finished_time = parser.parse(data[-1][1], tzinfos={'EST': -5 * 3600})
                else:
                    finished_time = parser.parse(data[-1][1], tzinfos={'EDT': -5 * 3600})

        assignee = None
        for j in assignee_bug:
            if i in assignee_bug[j]:
                assignee = j
                break

        if assignee in assignee_first_fixed_time:
            time = assignee_first_fixed_time[assignee][0] + (finished_time - assigned_time)
            cnt = assignee_first_fixed_time[assignee][1] + 1

            assignee_first_fixed_time[assignee] = [time, cnt]
        else:
            assignee_first_fixed_time[assignee] = [finished_time - assigned_time, 1]

    print("Saving...")

    print(len(ndbugs))

    with open('assignee_fixed_time.txt', 'wb') as fp:
        pickle.dump(assignee_fixed_time, fp)

    with open("assignee_reopened.txt", 'wb') as fp:
        pickle.dump(assignee_reopened_cnt, fp)

    af_avg = {}
    for i in assignee_first_fixed_time:
        af_avg[i] = assignee_first_fixed_time[i][0] / assignee_first_fixed_time[i][1]

    with open('assignee_avg_first_fixed_time.txt', 'wb') as fp:
        pickle.dump(af_avg, fp)

    # cnt = len(bugs)
    # for i in bugs:
    #     try:
    #         print("Remaining", cnt)
    #         request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
    #
    #     except Exception:
    #         url_not_downloaded = url + str(i)
    #         not_downloaded_bugs.append(url_not_downloaded)
    #         print(not_downloaded_bugs)
    #
    #     cnt -= 1

print("Process Finished!")
