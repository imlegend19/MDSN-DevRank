import pickle

import openpyxl


def fetch_file(path):
    with open(path, 'rb') as fp:
        file = pickle.load(fp)

    return file


RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/gnome/"

wb = openpyxl.Workbook()
sheet = wb.active

titles = ["Assignee Id", "L1 Centrality", "L2-A Centrality", "L2-B Centrality", "L3 Centrality",
          "Global Centrality A", "Global Centrality B", "Avg Fixed Time", "Reopened Percent",
          "Assignee Component", "Total Bugs", "Average First Closed Time", "Priority", "Severity"]

sheet.append(titles)
sheet.append(["" for i in range(len(titles))])

who_assignee = {v: k for k, v in fetch_file(RELATIVE_PATH + "assignee/assignee_who.txt").items()}

who = []
for i in who_assignee:
    who.append(i)

l1_centrality = fetch_file(RELATIVE_PATH + "layers/l1_centrality.txt")
l2_d1_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d1_centrality.txt")
l2_d2_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d2_centrality.txt")
l3_centrality = fetch_file(RELATIVE_PATH + "layers/l3_centrality.txt")
global_d1_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector_normal/EigenVector/"
                                                  "definition_1/global_ev_dict.txt")
global_d2_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector_normal/EigenVector/"
                                                  "definition_1/global_ev_dict.txt")
avg_fixed_time = fetch_file(RELATIVE_PATH + "assignee/assignee_avg_fixed_time.txt")
reopened_percent = fetch_file(RELATIVE_PATH + "assignee/assignee_reopened.txt")
assignee_comp = fetch_file(RELATIVE_PATH + "assignee/assignee_component.txt")
tot_bugs = fetch_file(RELATIVE_PATH + "assignee/assignee_total_bugs.txt")
avg_first_time = fetch_file(RELATIVE_PATH + "assignee/assignee_avg_first_fixed_time.txt")
priority = fetch_file(RELATIVE_PATH + "assignee/assignee_priority_count.txt")
severity = fetch_file(RELATIVE_PATH + "assignee/assignee_severity_count.txt")


def get_priority_points(priority):
    """
    Normal = 2
    Low = 1
    High = 3
    Urgent = 4
    Immediate = 5
    """
    points = 0
    for i in priority:
        if i == 'Low':
            points += priority[1]
        elif i == 'Normal':
            points += priority[i] * 2
        elif i == 'High':
            points += priority[i] * 3
        elif i == 'Urgent':
            points += priority[i] * 4
        else:
            points += priority[i] * 5

    return points


def get_severity_points(severity):
    """
    normal = 3
    critical = 5
    major = 4
    trivial = 1
    minor = 2
    blocker = 6
    """
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


for i in who:
    w_a = who_assignee[i]

    try:
        l1 = l1_centrality[i]
        l2_d1 = l2_d1_centrality[i]
        l2_d2 = l2_d2_centrality[i]
        l3 = l3_centrality[i]
        gl_a = global_d1_centrality[i]
        gl_b = global_d2_centrality[i]

        avg = avg_fixed_time[i].days * 24 + avg_fixed_time[i].seconds / 3600
        rp = reopened_percent[i]
        comp = assignee_comp[i]
        bugs = tot_bugs[i]
        avg_ft = avg_first_time[i].days * 24 + avg_first_time[i].seconds / 3600
        pri = get_priority_points(priority[i])
        sev = get_severity_points(severity[i])

        row = [i, l1, l2_d1, l2_d2, l3, gl_a, gl_b, avg, rp, comp, bugs, avg_ft, pri, sev]

        sheet.append(row)
    except Exception:
        pass

wb.save("correlation_gnome_1.xlsx")
print("Finished!")
