import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ax = plt.figure().gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

year = [2001, 2002, 2003, 2004, 2005]
plot_6 = [0.18541, 0.15509, 0.18997, 0.16839, 0.15791]
plot_258 = [0.07588, 0.05183, 0.10493, 0.10245, 0.10379]
plot_285 = [0.09598, 0.07167, 0.14125, 0.08826, 0.15155]
plot_190 = [0.02333, 0.04177, 0.02676, 0.07557, 0.12613]
plot_123 = [0.15025, 0.12428, 0.06762, 0.11688, 0.1339]

plt.plot(year, plot_6, marker='o')
plt.plot(year, plot_258, marker='o')
plt.plot(year, plot_285, marker='o')
plt.plot(year, plot_190, marker='o')
plt.plot(year, plot_123, marker='o')

labels = ['Assignee 6', 'Assignee 258', 'Assignee 285', 'Assignee 190', 'Assignee 123']
plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)

plt.show()
plt.savefig('images/eclipse_layer_1.png')
