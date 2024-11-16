import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
from scipy.stats import pearsonr

def get_sort(P, FDM, num):
    index = np.argsort(P)
    P_NEW = P[index]
    FDM_NEW = FDM[index]
    pm, fdmm, std = [], [], []
    k, p = 0, 0
    s = int(len(P)/num)+1
    l = int(len(P)%num)
    # print(len(P), s)
    for i in range(num):
        if k<=l:
            pm.append(np.median(P_NEW[i * s:(i + 1) * s]))
            fdmm.append(np.median(FDM_NEW[i * s:(i + 1) * s]))
            std.append(np.std(FDM_NEW[i * s:(i + 1) * s]))
        else:
            pm.append(np.median(P_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            fdmm.append(np.median(FDM_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            std.append(np.std(FDM_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            p = p+1
        k = k + 1
    return pm, fdmm, std

def Data_et(name):
    data_E = pd.read_csv(name)
    data_E = np.array(data_E)[:, 1:]
    data_E = data_E.astype(float)
    data_E[np.isnan(data_E) == True] = 0
    return data_E
  
data_Q = pd.read_csv(r".streamflow_CO2_trend.csv")
data_Q = np.array(data_Q)[:, 1:]
pd.read_csv(r"evspsblveg_CO2_trend.csv")
data_E = Data_et(r"evapotrans_CO2_trend.csv")
data_Et = Data_et(r"tran_CO2_trend.csv")
data_Es = Data_et(r"evspsblsoi_CO2_trend.csv")
data_Ei = Data_et(r"evspsblveg_CO2_trend.csv")
trendy_name = ['CABLE-POP', 'CLASSIC', 'CLM5.0', 'DLEM', 'IBIS', 'ISAM', 'ISBA-CTRIP', 'JSBACH',
                'JULES', 'LPJ-GUESS', 'LPX-Bern', 'ORCHIDEE', 'SDGVM', 'VISIT-NIES']
def p1(fig, data_Q, data_E, num):
    RHO, P = [], []
    # Y = np.zeros((len(trendy_name), len(data_Q)))
    k = 1
    for i in range(len(trendy_name)):
        q = np.ravel(data_Q[i, :])
        e = np.ravel(data_E[i, :])
        q = q.astype(float)
        q[np.isnan(q)] = 0
        if sum(e) == 0 or sum(q) == 0:
            RHO.append(np.NaN)
            P.append(np.NaN)
        else:
            plt.rcParams['xtick.direction'] = 'inout'
            plt.rcParams['ytick.direction'] = 'inout'
            ax = fig.add_subplot(3,7,k)
            # ax.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)
            ax.plot([0, 0], [-1.7, 1.7], c='k', ls=':', lw=1, alpha=0.75)
            ax.plot([-1.7, 1.7], [0, 0], c='k', ls=':', lw=1, alpha=0.75)

            x, y, z = get_sort(e, q, num)
            ax.plot(x, y, c='k', ls='-', lw=1,
                    markersize=2, marker='o', markeredgewidth=0.75,
                    markerfacecolor='None', markeredgecolor=colors[0])

            plt.xlim([-1.7, 1.7])
            plt.ylim([-1.7, 1.7])
            if k == 1 or k == 8:
                plt.xticks([-1.5, 0, 1.5], fontfamily='serif', fontsize=10)
                plt.yticks([-1.5 + 0.5 * i for i in range(7)], fontfamily='serif', fontsize=10)
                plt.ylabel("Q change driven\nby CO$_2$ (mm yr$^{-2}$)", fontfamily='serif', fontsize=12)
            else:
                plt.xticks([-1.5, 0, 1.5], fontfamily='serif', fontsize=10)
                plt.yticks([-1.5 + 0.5 * i for i in range(7)], [" "]*7, fontfamily='serif', fontsize=10)
            if k == 11 or k == 4:
                plt.xlabel("E change driven by CO$_2$ (mm yr$^{-2}$)", fontfamily='serif', labelpad=5, fontsize=12)
            plt.text(-1.3, -1.5, chr(96+k), ha='left', va='bottom', fontfamily='serif', fontsize=16, weight='bold')
            plt.title(trendy_name[i], loc='center', fontfamily='serif', fontsize=12, weight='normal')
            k = k + 1

            pc = pearsonr(x, y)
            print(trendy_name[i], pc[0], pc[1])
            RHO.append(pc[0])
            P.append(pc[1])
    return RHO, P
def prho(ax, x, y, p, markersize=10, marker='v', markeredgewidth=1.5, markerfacecolor='None', markeredgecolor='#1f77b4', label='p$<0.05$'):
    if p < 0.05:
        ax.plot(x, y, ls='None',
                markersize=markersize, marker=marker, markeredgewidth=markeredgewidth,
                markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor, label=label)
        ax.plot([-1.2, x], [y, y], ls='--', lw=0.5, c=markeredgecolor)
    else:
        ax.plot(x, y, ls='None',
                markersize=markersize, marker='x', markeredgewidth=markeredgewidth,
                markerfacecolor=markerfacecolor, markeredgecolor='r', label=label)
        ax.plot([-1.2, x], [y, y], ls='--', lw=0.5, c=markeredgecolor)
def p2(ax, data_E, data_Q):
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    Q = np.median(data_Q, axis=1)
    ks = np.argsort(Q)
    linewidth = 1.5
    color = ['gray', 'white']
    for k in range(15):
        plt.bar(x=k + 0.2, height=3, bottom=-1.5, width=1, color=color[k % 2], alpha=0.1)
    for k in range(14):
        q = np.ravel(data_Q[ks[k], :])
        e = np.ravel(data_E[ks[k], :])
        # et = np.ravel(data_Et[ks[k], :])
        x1 = np.median(e)
        s1 = np.std(e)
        x2 = np.median(q)
        s2 = np.std(q)
        # x3 = np.median(et)
        # s3 = np.std(et)
        if x2 < 0:
            ax.bar([k + 0.4], x2, width=0.3, edgecolor=colors[1], facecolor='None', label='Q',
                   yerr=[[s2], [0]], ecolor=colors[1], error_kw={'linewidth': linewidth}, linewidth=linewidth)
        else:
            ax.bar([k + 0.4], x2, width=0.3, edgecolor=colors[1], facecolor='None',
                   yerr=[[0], [s2]], ecolor=colors[1], error_kw={'linewidth': linewidth}, linewidth=linewidth)
        if sum(e) == 0:
            pass
        else:
            x, y, z = get_sort(e, q, 20)
            pc = pearsonr(x, y)
            if x1<0:
                ax.bar([k], x1, width=0.3, edgecolor=colors[0], facecolor='None', label='E',
                       yerr=[[s1], [0]], ecolor=colors[0], error_kw={'linewidth': linewidth}, linewidth=linewidth)
            else:
                ax.bar([k], x1, width=0.3, edgecolor=colors[0], facecolor='None',
                       yerr=[[0], [s1]], ecolor=colors[0], error_kw={'linewidth': linewidth}, linewidth=linewidth)
            ax.scatter(k+0.2, pc[0], edgecolor='r', facecolor='None', marker=(5, 1), label='$\\rho_s$')
    plt.xticks([k + 0.2 for k in range(14)], [trendy_name[k] for k in ks], fontfamily='serif', fontsize=12, rotation=90)

def p3(ax, RHO1, P1):
    color = ['red', 'orange', 'yellow', 'white']
    for i in range(4):
        plt.bar(x=0.125+i*0.25, height=21, bottom=-1, width=0.25, color=color[3-i], alpha=0.1)
    for i in range(4):
        plt.bar(x=-0.125-i*0.25, height=21, bottom=-1, width=0.25, color=color[3-i], alpha=0.1)
    t1, t2 = 0, 0
    for i in range(14):
        if t1 == 0 and P1[i]<0.05:
            prho(ax, RHO1[i], 14-i, P1[i],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label='p$<0.05$')
            t1 = 1
        elif t2 == 0 and P1[i]>=0.05:
            prho(ax, RHO1[i + 1], 14 - i, P1[i + 1],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label='p$\geq0.05$')
            t2 = 1
        else:
            prho(ax, RHO1[i], 14 - i, P1[i],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label=None)
    # ax.plot(RHO1[1:], [14-i for i in range(14)], ls='--', lw=0.5, c=colors[1])


fig = plt.figure(figsize=(10, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
marker = ['^', '*', 'o']
ls = [':', '--', '-.']

plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
RHO1, P1 = p1(fig, data_Q, data_E, 20)


ax = fig.add_subplot(3,7,(15,21))
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
p2(ax, data_E, data_Q)
handles2, labels2 = ax.get_legend_handles_labels()
plt.yticks([-1+0.2*i for i in range(11)], fontfamily='serif', fontsize=10)
plt.ylabel("Q or E change driven\nby CO$_2$ (mm yr$^{-2}$)\n or Rank correlation $\\rho_s$ ($-$)", fontfamily='serif', fontsize=12)
plt.xlim([-0.4, 13.8])
plt.ylim([-1.1, 0.9])
plt.title("n", loc='left', fontfamily='serif', fontsize=16, weight='bold')

legend_font = {
        'family': 'serif',
        'style': 'normal',
        'size': 11,
        'weight': "normal",
    }

fig.legend([handles2[5]]+[handles2[15]]+[handles2[-1]], [labels2[5]]+[labels2[15]]+[labels2[-1]],
           loc='center',
           bbox_to_anchor=[0.86, 0.365],
           prop=legend_font, ncol=3)

fig.patch.set_alpha(1.0)
plt.tight_layout()
plt.subplots_adjust()
plt.rcParams['savefig.dpi'] = 1000
plt.show()
