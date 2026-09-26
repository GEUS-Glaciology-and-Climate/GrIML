import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Set the font family to sans-serif
mpl.rcParams['font.family'] = 'sans-serif'

# Specify "Arial" as the font to use for the sans-serif family
mpl.rcParams['font.sans-serif'] = ['Arial']

# Optional: You can also set a default font size
mpl.rcParams['font.size'] = 10

fsize1=12
fsize2=11

# Klimadatastyrelsen Open Country Greenland 1:50,000 vector dataset
klimadata = [156593,           # Number of all lakes
            14337.3,          # All lakes area
            np.nan,              # Total volume
            2918,              # Number of IMLs
            3744.5,           # IMLs area
            np.nan               # IMLs volume
            ]

# Global Glacial Lake dataset
zhang_data = [14845,           # Number of all lakes
              6683.1,         # All lakes area
              398.5,           # Total volume
              5926,            # Number of IMLs
              6535.3,         # IMLs areas
              397.8            # IMLs volume
              ]

# GIGLake (Global Inventory of Glacial Lakes) dataset
song_data = [48307,          # Number of all lakes
             10681.8,       # All lakes area
             np.nan,           # Total volume
             2826,           # Number of IMLs
             2957.0,        # IMLs areas
             np.nan            # IMLs volume
             ]

# ESA Glaciers_cci 2017 inventory
iiml_data = [np.nan,           # Number of all lakes
             np.nan,           # All lakes area
             np.nan,           # Total volume
             3347,           # Number of IMLs
             4018.9,        # IMLs areas
             np.nan            # IMLs volume
             ]

# IMLs 2016-2025
new_data = [np.nan,           # Number of all lakes
            np.nan,           # All lakes area
            np.nan,           # Total volume
            4038,           # Number of IMLs
            4734.9,        # IMLs areas
            462.5          # IMLs volume
            ]

labels = ['Klimadatasytrelsen',
          'Zhang et al.',
          'Song et al.',
          'ESA cci_glaciers',
          'This study']

colors = ['#a559aa',
          '#59a89c',
          '#f0c571',
          '#e02b35',
          '#082a54']
x = np.arange(len(labels))  # the label locations
width = 0.7  # the width of the bars

#fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(13,5))
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3,
    figsize=(12, 5),
    gridspec_kw={'width_ratios': [1.25, 1.25, 0.5]}  # ax3 is smaller
)

counts = [klimadata[-3],zhang_data[-3],song_data[-3],iiml_data[-3],new_data[-3]]
rects1 = ax1.bar(x, counts, width, color=colors)

areas = [klimadata[-2],zhang_data[-2],song_data[-2],iiml_data[-2],new_data[-2]]
rects2 = ax2.bar(x, areas, width, color=colors)

volumes = [zhang_data[-1], new_data[-1]]
rects3 = ax3.bar(x[:2], volumes, 0.6, color=[colors[1], colors[-1]])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Number of ice-marginal lakes', fontsize=fsize2)
ax2.set_ylabel('Total lake area (km$^2$)', fontsize=fsize2)
ax3.set_ylabel('Total lake volume (Gt)', fontsize=fsize2)

for ax in [ax1,ax2]:
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90, fontsize=fsize2)

ax3.set_xticks(x[:2])
ax3.set_xticklabels([labels[1], labels[-1]], rotation=90, fontsize=fsize2)

ax1.set_ylim([0,7000])
ax2.set_ylim([0,7000])
ax3.set_ylim([0,500])

for ax in [ax1,ax2,ax3]:
    ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5, alpha=0.5)
    ax.set_axisbelow(True)

ax1.text(-0.5, 6600, "a.", fontsize=fsize1, fontweight="bold")
ax2.text(-0.5, 6600, "b.", fontsize=fsize1, fontweight="bold")
ax3.text(-0.3, 470, "c.", fontsize=fsize1, fontweight="bold")

#ax1.text(-0.5, 7500, "Comparison of existing Greenland glacial lake datasets", fontsize=fsize1, fontweight="bold")

def autolabel(rects, ax, decimals=2):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        if decimals == 2:
            ax.annotate('{:.1f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        elif decimals == 1:
            ax.annotate('{:.1f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        else:
            ax.annotate('{:.0f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

autolabel(rects1, ax1, 0)
autolabel(rects2, ax2, 2)
autolabel(rects3, ax3, 2)

fig.tight_layout()
plt.savefig("lake_dataset_comparison.png", dpi=300, transparent=False)
#plt.show()