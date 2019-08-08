import pickle
import openpyxl
from local_settings_eclipse import db


def fetch_file(path):
    with open(path, 'rb') as fp:
        file = pickle.load(fp)

    return file


RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/"

wb = openpyxl.Workbook()
sheet = wb.active

titles = ["Assignee Id", "L1 Centrality", "L2-A Centrality", "L2-B Centrality", "L3 Centrality",
          "L4 Centrality",
          "Global Centrality A", "Global Centrality B", "Avg Fixed Time", "Reopened Percent",
          "Assignee Component", "Total Bugs", "First Closed Avg Time", "Priority/Bug", "Severity/Bug"]

sheet.append(titles)
sheet.append(["" for i in range(len(titles))])

with db:
    cur = db.cursor()
    cur.execute("SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed "
                "WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed)")

who = []
for i in cur.fetchall():
    who.append(i[0])

l1_centrality = fetch_file(RELATIVE_PATH + "layers/l1_centrality.txt")
l2_d1_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d1_centrality.txt")
l2_d2_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d2_centrality.txt")
l3_centrality = fetch_file(RELATIVE_PATH + "layers/l3_centrality.txt")
l4_centrality = fetch_file(RELATIVE_PATH + "layers/l4_centrality.txt")
global_d1_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/"
                                                  "definition_1/global_ev_dict.txt")
global_d2_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/"
                                                  "definition_2/global_ev_dict.txt")
avg_fixed_time = fetch_file(RELATIVE_PATH + "assignee/assignee_avg_fixed_time.txt")
reopened_percent = fetch_file(RELATIVE_PATH + "assignee/assignee_reopened.txt")
assignee_comp = fetch_file(RELATIVE_PATH + "assignee/assignee_component.txt")
tot_bugs = fetch_file(RELATIVE_PATH + "assignee/assignee_total_bugs.txt")
av_ft = fetch_file(RELATIVE_PATH + "assignee/assignee_avg_first_fixed_time.txt")
priority = fetch_file(RELATIVE_PATH + "assignee/assignee_priority_count.txt")
severity = fetch_file(RELATIVE_PATH + "assignee/assignee_severity_count.txt")


def get_priority_points(priority):
    points = 0
    for i in priority:
        if i == 'P1':
            points += priority[i]
        elif i == 'P2':
            points += priority[i] * 2
        elif i == 'P3':
            points += priority[i] * 3
        elif i == 'P4':
            points += priority[i] * 4
        else:
            points += priority[i] * 5

    return points


def get_severity_points(severity):
    points = 0
    for i in severity:
        if i == 'normal':
            points += severity[i] * 3
        elif i == 'critical':
            points += severity[i] * 5
        elif i == 'major':
            points += severity[i] * 4
        elif i == 'trivial':
            points += severity[i] * 1
        elif i == 'minor':
            points += severity[i] * 2
        elif i == 'blocker':
            points += severity[i] * 6

    return points


cnt = 0

for i in who:
    try:
        l1 = l1_centrality[i]
        l2_d1 = l2_d1_centrality[i]
        l2_d2 = l2_d2_centrality[i]
        l3 = l3_centrality[i]
        l4 = l4_centrality[i]
        gl_a = global_d1_centrality[i]
        gl_b = global_d2_centrality[i]
        avg = avg_fixed_time[i].days * 24 + avg_fixed_time[i].seconds / 3600
        rp = (reopened_percent[i][0] / reopened_percent[i][1]) * 100
        comp = assignee_comp[i]
        bugs = tot_bugs[i]
        aft = av_ft[i].days * 24 + av_ft[i].seconds / 3600
        pri = get_priority_points(priority[i]) / tot_bugs[i]
        sev = get_severity_points(severity[i]) / tot_bugs[i]

        row = [i, l1, l2_d1, l2_d2, l3, l4, gl_a, gl_b, avg, rp, comp, bugs, aft, pri, sev]

        sheet.append(row)
    except Exception:
        cnt += 1
        print(i)
        pass

wb.save("correlation_eclipse_1.xlsx")
print("Finished!")
print("Error count:", cnt)
