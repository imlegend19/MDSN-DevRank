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
plot_6 = [[0.18541, 0.15509, 0.18997, 0.16839, 0.15791], [0.10309, 0.10602, 0.16261, 0.11443, 0.10587],
          [0.10988, 0.12006, 0.18416, 0.13202, 0.12371], [0.12804, 0.12213, 0.16144, 0.12327, 0.1168],
          [0.09656, 0.09609, 0.1094, 0.10069, 0.08774], [117.0, 3.0, 4.0, 129.0, 4.0], [324.0, 6.0, 6.0, 336.0, 12.0]]
plot_258 = [[0.07588, 0.05183, 0.10493, 0.10245, 0.10379], [0.0826, 0.03678, 0.11797, 0.10382, 0.10082],
            [0.08322, 0.04667, 0.14642, 0.09385, 0.11195], [0.09478, 0.10737, 0.07839, 0.11888, 0.11531],
            [0.09603, 0.0958, 0.10905, 0.10025, 0.0869], [75.0, 1.0, 2.0, 33.0, 2.0], [156.0, 6.0, 6.0, 72.0, 6.0]]
plot_285 = [[0.09598, 0.07167, 0.14125, 0.08826, 0.15155], [0.09868, 0.10022, 0.13099, 0.11485, 0.10335],
            [0.10641, 0.10408, 0.13601, 0.11861, 0.1141], [0.10706, 0.08191, 0.16311, 0.12018, 0.11612],
            [0.09656, 0.09324, 0.12004, 0.10051, 0.08774], [6.0, 8.0, 3.0, 97.0, 2.0], [12.0, 24.0, 6.0, 252.0, 12.0]]
plot_190 = [[0.02333, 0.04177, 0.02676, 0.07557, 0.12613], [0.02293, 0.09467, 0.02161, 0.11123, 0.10225],
            [0.02523, 0.07107, 0.02229, 0.11245, 0.11578], [0.05691, 0.09487, 0.06547, 0.11218, 0.11388],
            [0.09604, 0.09454, 0.10019, 0.10025, 0.08774], [27.0, 6.0, 3.0, 119.0, 6.0], [54.0, 12.0, 6.0, 246.0, 12.0]]
plot_123 = [[0.15025, 0.12428, 0.06762, 0.11688, 0.1339], [0.10424, 0.10469, 0.12652, 0.11144, 0.10589],
            [0.11118, 0.11498, 0.1517, 0.11599, 0.10975], [0.12264, 0.1178, 0.08962, 0.12393, 0.11875],
            [0.09656, 0.0963, 0.12004, 0.10025, 0.08774], [216.0, 115.0, 2.0, 294.0, 187.0],
            [438.0, 258.0, 6.0, 714.0, 402.0]]

ax1.plot(year, plot_6[0], marker='o')
ax1.plot(year, plot_258[0], marker='o')
ax1.plot(year, plot_285[0], marker='o')
ax1.plot(year, plot_190[0], marker='o')
ax1.plot(year, plot_123[0], marker='o')

ax2.plot(year, plot_6[1], marker='o')
ax2.plot(year, plot_258[1], marker='o')
ax2.plot(year, plot_285[1], marker='o')
ax2.plot(year, plot_190[1], marker='o')
ax2.plot(year, plot_123[1], marker='o')

ax3.plot(year, plot_6[2], marker='o')
ax3.plot(year, plot_258[2], marker='o')
ax3.plot(year, plot_285[2], marker='o')
ax3.plot(year, plot_190[2], marker='o')
ax3.plot(year, plot_123[2], marker='o')

ax4.plot(year, plot_6[3], marker='o')
ax4.plot(year, plot_258[3], marker='o')
ax4.plot(year, plot_285[3], marker='o')
ax4.plot(year, plot_190[3], marker='o')
ax4.plot(year, plot_123[3], marker='o')

ax5.plot(year, plot_6[4], marker='o')
ax5.plot(year, plot_258[4], marker='o')
ax5.plot(year, plot_285[4], marker='o')
ax5.plot(year, plot_190[4], marker='o')
ax5.plot(year, plot_123[4], marker='o')

ax6.plot(year, plot_6[5], marker='o')
ax6.plot(year, plot_258[5], marker='o')
ax6.plot(year, plot_285[5], marker='o')
ax6.plot(year, plot_190[5], marker='o')
ax6.plot(year, plot_123[5], marker='o')

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

labels = ['Assignee 6', 'Assignee 258', 'Assignee 285', 'Assignee 190', 'Assignee 123']

plt.figlegend(labels, ncol=len(labels),
              loc='lower center', fontsize='small', shadow=True)

plt.figure().tight_layout()

# plt.savefig('images/netbeans_metrics.png', bbox_inches='tight')

plt.show()
