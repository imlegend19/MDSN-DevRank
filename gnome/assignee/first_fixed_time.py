import pickle
from urllib import request
from local_settings_gnome import db
from bs4 import BeautifulSoup
from dateutil import parser


def calculate():
    assignee_first_fixed_time = {}
    assignee_pet_name = []

    for i in assignee_bug.values():
        for j in i:

            # print("Remaining", cnt)
            # request.urlretrieve(url + str(j), "bug_html/" + str(j) + ".html")

            # cnt -= 1
            # print("Ongoing", j)

            with open('bug_html/' + str(j) + '.html', 'rb') as fp:
                html = fp.read()

            soup = BeautifulSoup(html, features="html.parser")

            div = soup.find("div", attrs={"id": "bugzilla-body"})
            table = div.find("table")

            # headings = [th.get_text() for th in table.find("tr").find_all("th")]
            # print(headings)

            data = []
            for row in table.find_all("tr")[1:]:
                dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
                data.append(dataset)

            print(data)
            assignee_pet_name.append(data[0][0])

            assigned_time = parser.parse(data[0][1])

            try:
                for k in data:
                    if len(k) == 5:
                        finished_time = parser.parse(k[1])
                    if 'CLOSED' in k:
                        if len(k) == 3:
                            break
                        else:
                            finished_time = parser.parse(k[1])
                            break
            except Exception:
                if len(data[-1]) == 3:
                    finished_time = parser.parse(data[-2][1])
                else:
                    finished_time = parser.parse(data[-1][1])

            assignee = list(assignee_bug.keys())[list(assignee_bug.values()).index(i)]

            if assignee in assignee_first_fixed_time:
                time = assignee_first_fixed_time[assignee][0] + (finished_time - assigned_time)
                cnt = assignee_first_fixed_time[assignee][1] + 1

                assignee_first_fixed_time[assignee] = [time, cnt]
            else:
                assignee_first_fixed_time[assignee] = [finished_time - assigned_time, 1]

    with open('assignee_first_fixed_time.txt', 'wb') as fp:
        pickle.dump(assignee_first_fixed_time, fp)


with db:
    print("Connected to db...")

    cur = db.cursor()
    cur.execute("SELECT DISTINCT assigned_to FROM test_bug_fixed_closed")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0].strip())

    print(assignees)
    cur.execute("SELECT DISTINCTROW who_id, who FROM test_comment_fixed_closed")
    who_id_who = {}
    for i in cur.fetchall():
        who_id_who[i[1].strip()] = i[0]

    no_comment_assignee = []

    print("Filtering assignee...")
    segregated_assignees = {}
    for i in assignees:
        if i in who_id_who.keys():
            segregated_assignees[i] = who_id_who[i]
        else:
            no_comment_assignee.append(i)

    print(segregated_assignees)
    print(len(segregated_assignees))

    # with open("assignee_who.txt", 'wb') as fp:
    #     pickle.dump(segregated_assignees, fp)

    print(segregated_assignees)

    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bug_fixed_closed")

    assignee_bug = {}
    for i in cur.fetchall():
        if i[1].strip() in assignee_bug:
            lst = assignee_bug[i[1].strip()]
            lst.append(i[0])
            assignee_bug[i[1].strip()] = lst
        else:
            assignee_bug[i[1].strip()] = [i[0]]

    print(len(assignee_bug))
    print(assignee_bug)

    # with open("assignee_bug.txt", 'wb') as fp:
    #     pickle.dump(assignee_bug, fp)

    for i in list(assignee_bug):
        if i not in segregated_assignees.keys():
            assignee_bug.pop(i)

    print(len(assignee_bug))

    # url = "https://bugzilla.gnome.org/show_activity.cgi?id="
    #
    # cnt = 0
    #
    # for i in assignee_bug.values():
    #     cnt += len(i)
    #
    # assignee_reopened_cnt = {}
    #
    # for i in assignee_bug.values():
    #     for j in i:
    #         print("Ongoing", j)
    #
    #         with open('bug_html/' + str(j) + '.html', 'rb') as fp:
    #             html = fp.read()
    #
    #         soup = BeautifulSoup(html, features="html.parser")
    #
    #         div = soup.find("div", attrs={"id": "bugzilla-body"})
    #         table = div.find("table")
    #
    #         headings = [th.get_text() for th in table.find("tr").find_all("th")]
    #
    #         # print(headings)
    #
    #         data = []
    #         for row in table.find_all("tr")[1:]:
    #             dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
    #             data.append(dataset)
    #
    #         assignee = list(assignee_bug.keys())[list(assignee_bug.values()).index(i)]
    #
    #         for k in data:
    #             if 'REOPENED' in k:
    #                 if segregated_assignees[assignee] in assignee_reopened_cnt:
    #                     reopened = assignee_reopened_cnt[segregated_assignees[assignee]][0]
    #                     tot = assignee_reopened_cnt[segregated_assignees[assignee]][1]
    #                     assignee_reopened_cnt[segregated_assignees[assignee]] = [reopened + 1, tot + 1]
    #                 else:
    #                     assignee_reopened_cnt[segregated_assignees[assignee]] = [1, 1]
    #             else:
    #                 if segregated_assignees[assignee] in assignee_reopened_cnt:
    #                     reopened = assignee_reopened_cnt[segregated_assignees[assignee]][0]
    #                     tot = assignee_reopened_cnt[segregated_assignees[assignee]][1]
    #                     assignee_reopened_cnt[segregated_assignees[assignee]] = [reopened, tot + 1]
    #                 else:
    #                     assignee_reopened_cnt[segregated_assignees[assignee]] = [0, 1]
    #
    # assignee_reopened_percent = {}
    #
    # print("Setting up percent dict...")
    # mx = [0, 0]
    # for i in assignee_reopened_cnt:
    #     percent = (assignee_reopened_cnt[i][0] / assignee_reopened_cnt[i][1]) * 100
    #     assignee_reopened_percent[i] = percent
    #
    #     if percent > mx[1]:
    #         mx = [i, percent]
    #
    # print(assignee_reopened_percent)
    # print(mx)
    #
    # with open("assignee_reopened.txt", 'wb') as fp:
    #     pickle.dump(assignee_reopened_percent, fp)

    calculate()

    print("Finished!")
