import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def picture2():
    data = pd.read_csv(r"dataset/streamflow_driven_by_CO2_TRENDYS.csv")

    trendy_name = ['CABLE-POP', 'CLASSIC', 'CLM5.0', 'DLEM', 'IBIS', 'ISAM', 'ISBA-CTRIP', 'JSBACH',
                       'JULES', 'LPJ-GUESS', 'LPX-Bern', 'ORCHIDEE', 'SDGVM', 'VISIT-NIES']
    trendy_name2 = ['CABLE-POP', 'CLASSIC', 'CLM5.0', 'DLEM', 'IBIS', 'ISAM', 'ISBA-CTRIP', 'JSBACH',
                       'JULES', 'LPJ-GUESS', 'LPX-BERN', 'ORCHIDEE', 'SDGVM', 'VISIT-NIES']

    fig = plt.figure(figsize=(12, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    marker = ['^', 'o', '*']
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax = fig.add_subplot(111)
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax.spines[['right', 'top']].set_visible(False)
    colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
    ax.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)

    lx = [-0.25, 0.45]
    for i in range(8):
        plt.bar(x=30+40*(i+0), height=20, bottom=-10, width=20, color='gray', alpha=0.10)
    QQ = np.zeros((12, 14))
    for i in range(len(trendy_name)):
        q = np.ravel(data[trendy_name[i]])
        qq = np.ravel([0.0]*12)
        for j in range(12):
            qq[j] = np.mean(q[j*10:(j+1)*10])
        QQ[:, i] = qq

    DS = np.mean(QQ, axis=0)
    K = np.argsort(DS)
    print(K)
    for i in range(len(trendy_name)):
        s = [-4, -2, 0, 2, 4]
        plt.plot([k*20+10+s[int(i%len(s))] for k in range(12)], QQ[:, K[13-i]], c=colors[int(i % 5)], ls='--',
                 lw=0.5, markersize=10, marker=marker[int(i%3)], markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[int(i%5)], label=trendy_name2[K[13-i]])

    plt.xticks([20*i+10 for i in range(12)], [str(1901+i*10)+"$-$\n$-$"+str(1910+i*10) for i in range(12)],
               fontfamily='serif', fontsize=13)
    plt.yticks(fontfamily='serif', fontsize=13)
    plt.xlim([0, 240])
    plt.ylim([-9, 9])
    plt.ylabel("Q driven by CO$_2$ (mm yr$^{-1}$)", fontfamily='serif', fontsize=14)
    plt.xlabel("Years (yr)", fontfamily='serif', labelpad=8, fontsize=14)

    ax.patch.set_alpha(0.3)
    handles, labels = ax.get_legend_handles_labels()
    legend_font = {
        'family': 'serif',  # 字体
        'style': 'normal',
        'size': 12,  # 字号
        'weight': "normal",  # 是否加粗，不加粗
    }
    fig.legend(handles[:], labels[:], loc='lower center', prop=legend_font, ncol=7)

    fig.patch.set_alpha(1.0)
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.98,
        bottom=0.18,
        left=0.075,
        right=0.975,
        hspace=0.55,
        wspace=1.0
    )
    plt.rcParams['savefig.dpi'] = 2000
    plt.show()

picture2()
