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
plot_6 = [[230.867412712037, 46.01251761, 10912.596402166, 642.409747351607, 4201.829862575],
          [15040.16046309133, 7224.592500474, 17870.240011392, 12029.88142881943, 6374.616946538],
          [3.92156862745098, 0.0, 0.0, 5.203619909502263, 0.0], [9.0, 1.0, 1.0, 17.0, 2.0]]
plot_258 = [[517.5911543806153, 9215.559185514, 8.880007104, 825.8221542355, 841.791112544],
            [11751.776025708, 9261.385017108, 1057.769168082, 12891.17699168233, 841.971112688],
            [5.921052631578947, 0.0, 0.0, 1.183431952662722, 0.0], [4.0, 1.0, 1.0, 5.0, 1.0]]
plot_285 = [[1165.619862407, 1212.3813197495, 0.023888908, 1065.609583706714, 223.605700529],
            [15686.356112996, 8356.6852120815, 2710.252240024, 12430.43486784419, 6239.207370077],
            [0.0, 0.0, 0.0, 1.550387596899225, 0.0], [2.0, 2.0, 1.0, 7.0, 2.0]]
plot_190 = [[460.9502487404444, 10428.401528099, 571.5277934, 590.404065324878, 851.638481533],
            [15665.438056706, 27597.711674436, 577.597779056, 12661.13866552015, 4729.256667672],
            [2.564102564102564, 0.0, 0.0, 1.5625, 0.0], [1.0, 2.0, 1.0, 6.0, 1.0]]
plot_123 = [[2867.768771138, 1303.610278061349, 18108.33195431, 1850.337873578235, 4517.653872529731],
            [17577.74654887608, 9148.188837434791, 43486.657518126, 16088.3158987304, 39060.97716424442],
            [4.086845466155811, 2.893890675241158, 9.090909090909092, 4.715127701375246, 2.194787379972565],
            [3.0, 6.0, 1.0, 7.0, 3.0]]

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

labels = ['Assignee 6', 'Assignee 258', 'Assignee 285', 'Assignee 190', 'Assignee 123']

plt.figlegend(labels, fontsize='large', ncol=1, handleheight=2.4, labelspacing=0.05, shadow=True,
              bbox_to_anchor=(0.98, 0.48))

plt.figure().tight_layout()

# plt.savefig('images/netbeans_centrality.png', bbox_inches='tight')

plt.show()
