import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ax1 = plt.subplot(231)
ax2 = plt.subplot(232)
ax3 = plt.subplot(233)
ax4 = plt.subplot(234)
ax5 = plt.subplot(235)

ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
ax5.xaxis.set_major_locator(MaxNLocator(integer=True))

year = [2001, 2002, 2003, 2004, 2005]
plot_37 = [[0.10461, 0.13587, 0.03713, 0.28105, 0.03111], [0.12922, 0.12326, 0.10974, 0.09624, 0.09784],
           [0.14282, 0.13921, 0.12189, 0.12853, 0.10043], [0.12796, 0.07453, 0.04099, 0.16948, 0.08798],
           [0.14063, 0.13095, 0.08338, 0.06617, 0.04842]]

for i in plot_37:
    i.reverse()

plot_34 = [[0.3906, 0.41644, 0.1555, 0.00136, 0.03479], [0.12922, 0.12543, 0.12712, 0.06206, 0.08559],
           [0.14559, 0.14753, 0.13898, 0.03261, 0.08581], [0.24176, 0.26555, 0.10654, 0.00217, 0.09597],
           [0.14506, 0.1435, 0.08404, 0.06243, 0.0512]]

for i in plot_34:
    i.reverse()

plot_39 = [[0.15231, 0.17916, 0.09363, 0.01589, 0.02652], [0.1358, 0.12782, 0.10918, 0.08501, 0.08246],
           [0.14563, 0.1454, 0.12218, 0.06336, 0.07019], [0.13144, 0.14354, 0.1207, 0.0737, 0.05108],
           [0.141, 0.1367, 0.08348, 0.06582, 0.05075]]

for i in plot_39:
    i.reverse()

plot_18 = [[0.12729, 0.06798, 0.15568, 0.0501, 0.01091], [0.12922, 0.12326, 0.10886, 0.11788, 0.04372],
           [0.14527, 0.13921, 0.11926, 0.09721, 0.03622], [0.08116, 0.10526, 0.14112, 0.11473, 0.07359],
           [0.08987, 0.13781, 0.08404, 0.06617, 0.04779]]

for i in plot_18:
    i.reverse()

plot_481 = [[0.03058, 0.15141, 0.02427, 0.01184, 0.02283], [0.12922, 0.12326, 0.10886, 0.06206, 0.06385],
            [0.14177, 0.14437, 0.0255, 0.04083, 0.03177], [0.00932, 0.21267, 0.09326, 0.07532, 0.04787],
            [0.08952, 0.09521, 0.07246, 0.06248, 0.01917]]

for i in plot_481:
    i.reverse()

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

ax1.set_xticks(year)
ax1.set_title('Layer 1')
ax1.set_xticklabels(year, rotation=45)

ax2.set_xticks(year)
ax2.set_title('Layer 2 - D1')
ax2.set_xticklabels(year, rotation=45)

ax3.set_xticks(year)
ax3.set_title('Layer 2 - D2')
ax3.set_xticklabels(year, rotation=45)

ax4.set_xticks(year)
ax4.set_title('Layer 3')
ax4.set_xticklabels(year, rotation=45)

ax5.set_xticks(year)
ax5.set_title('Layer 4')
ax5.set_xticklabels(year, rotation=45)

labels = ['Assignee 37', 'Assignee 34', 'Assignee 39', 'Assignee 18', 'Assignee 481']

plt.figlegend(labels, fontsize='large', ncol=1, handleheight=2.4, labelspacing=0.05, shadow=True,
              bbox_to_anchor=(0.98, 0.48))

plt.figure().tight_layout()

# plt.savefig('images/netbeans_metrics.png', bbox_inches='tight')

plt.show()
