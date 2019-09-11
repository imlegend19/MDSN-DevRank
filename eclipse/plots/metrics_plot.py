import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ax1 = plt.subplot(231)
ax2 = plt.subplot(232)
ax3 = plt.subplot(233)
ax4 = plt.subplot(234)
ax5 = plt.subplot(235)
ax6 = plt.subplot(236)

ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
ax5.xaxis.set_major_locator(MaxNLocator(integer=True))
ax6.xaxis.set_major_locator(MaxNLocator(integer=True))

year = [2001, 2002, 2003, 2004, 2005]
plot_37 = [[168.722778356, 49.374445544, 270.135560464, 5090.782517787125, 3169.008889696],
           [22169.418893224, 1052.036404918, 8040.649722742, 11978.88612898112, 1167.692790332],
           [0.0, 0.0, 0.0, 0.8620689655172413, 8.695652173913043],
           [1.0, 1.0, 1.0, 11.0, 1.0], [5.0, 3.0, 3.0, 54.0, 3.0], [6.0, 4.0, 2.0, 99.0, 4.0]
           ]

plot_37[2].reverse()
plot_37[3].reverse()

plot_34 = [[761.4376683732115, 973.2233061730893, 2395.0125702545, 10467.07500246, 3884.482794164],
           [21764.34569714579, 14357.20688497186, 9029.664121701668, 18967.76241361733, 3906.597792656],
           [3.047619047619047, 2.483069977426636, 1.219512195121951, 0.0, 0.0],
           [1.0, 1.0, 2.0, 1.0, 1.0], [284.0, 320.0, 26.0, 9.0, 3.0], [301.0, 313.0, 31.0, 6.0, 3.0]
           ]

plot_34[4].reverse()
plot_34[5].reverse()

plot_39 = [[774.436671816, 29.621393386, 15.61529027, 3003.337086003, 1512.766389502],
           [28398.475977403, 15059.186397838, 45.235294766, 5538.052921509, 13454.43890044],
           [0.0, 0.0, 0.0, 0.0, 21.42857142857143],
           [1.0, 1.0, 1.0, 1.0, 1.0], [5.0, 2.0, 3.0, 5.0, 2.0], [8.0, 4.0, 4.0, 6.0, 0.0]
           ]

plot_39[2].reverse()
plot_39[5].reverse()

plot_18 = [[463.260005808, 4172.9591437525, 938.5609048265, 10219.69774013914, 14063.639731534],
           [22134.141393802, 6776.465779693612, 6166.8952098495, 11119.03698427086, 15598.707091899],
           [0.0, 3.10880829015544, 5.594405594405594, 0.0, 0.0],
           [1.0, 1.0, 1.0, 2.0, 1.0], [3.0, 107.0, 23.0, 22.0, 4.0], [3.0, 96.0, 26.0, 13.0, 8.0]
           ]

plot_18[4].reverse()

plot_481 = [[56770.277786, 3052.138753311, 496.176114452, 286.481406874, 276.653621234],
            [58763.39862023, 23315.686814905, 909.83195231, 9716.790016632, 276.792510234],
            [0.0, 0.0, 11.11111111111111, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0], [3.0, 6.0, 6.0, 3.0, 3.0], [0.0, 7.0, 9.0, 4.0, 4.0]
            ]

ax1.plot(year, plot_37[0], marker='o')
ax1.plot(year, plot_34[0], marker='o')
ax1.plot(year, plot_39[0], marker='o')
ax1.plot(year, plot_18[0], marker='o')
ax1.plot(year, plot_481[0], marker='o')

ax2.plot(year, plot_37[1], marker='o')
ax2.plot(year, plot_34[1], marker='o')
ax2.plot(year, plot_39[1], marker='o')
ax2.plot(year, plot_18[1], marker='o')
ax2.plot(year, plot_481[1], marker='o')

ax3.plot(year, plot_37[2], marker='o')
ax3.plot(year, plot_34[2], marker='o')
ax3.plot(year, plot_39[2], marker='o')
ax3.plot(year, plot_18[2], marker='o')
ax3.plot(year, plot_481[2], marker='o')

ax4.plot(year, plot_37[3], marker='o')
ax4.plot(year, plot_34[3], marker='o')
ax4.plot(year, plot_39[3], marker='o')
ax4.plot(year, plot_18[3], marker='o')
ax4.plot(year, plot_481[3], marker='o')

ax5.plot(year, plot_37[4], marker='o')
ax5.plot(year, plot_34[4], marker='o')
ax5.plot(year, plot_39[4], marker='o')
ax5.plot(year, plot_18[4], marker='o')
ax5.plot(year, plot_481[4], marker='o')

ax6.plot(year, plot_37[5], marker='o')
ax6.plot(year, plot_34[5], marker='o')
ax6.plot(year, plot_39[5], marker='o')
ax6.plot(year, plot_18[5], marker='o')
ax6.plot(year, plot_481[5], marker='o')

ax1.set_xticks(year)
ax1.set_title('Avg Fixed')
ax1.set_xticklabels(year, rotation=30)

ax2.set_xticks(year)
ax2.set_title('Avg Closed')
ax2.set_xticklabels(year, rotation=30)

ax3.set_xticks(year)
ax3.set_title('Reopened %')
ax3.set_xticklabels(year, rotation=30)

ax4.set_xticks(year)
ax4.set_title('Total Components')
ax4.set_xticklabels(year, rotation=30)

ax5.set_xticks(year)
ax5.set_title('Avg Priority Points')
ax5.set_xticklabels(year, rotation=30)

ax6.set_xticks(year)
ax6.set_title('Avg Severity Points')
ax6.set_xticklabels(year, rotation=30)

labels = ['Assignee 37', 'Assignee 34', 'Assignee 39', 'Assignee 18', 'Assignee 481']
plt.figlegend(labels, ncol=len(labels),
              loc='lower center', fontsize='small', shadow=True)

plt.figure().tight_layout()

# plt.savefig('images/netbeans_metrics.png', bbox_inches='tight')

plt.show()
