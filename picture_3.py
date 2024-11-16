import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
from scipy.stats import pearsonr
# 把数据的年份信息重新提取一下
def get_years():
    data = pd.read_csv(r"dataset/observation_based_approach_result.csv")
    FileName = data['FileName']
    Area = data['Area']
    Name = data['Name']
    year_data = pd.DataFrame([])
    for i in range(len(Area)):
        if Area[i]<=200000:
            d = pd.read_csv(r"dataset/small_basins_data_Yearly/"+FileName[i]+r".csv")
            year = np.ravel(d['Year'])
            q_day = np.ravel(d['n_flow'])
            # q = np.ravel(d['Flow_mm'])
            q_day1 = q_day[year>1980]
            # q1 = q[year>1980]
            y1 = year[year>1980]
            q_day2 = q_day1[y1<2021]
            # q2 = q1[y1<2021]
            k = np.ravel(np.zeros((40, 1)))
            k[q_day2>=365] = 1
            year_data[Name[i]] = k
    year_data.index = [1981+i for i in range(40)]
    # year_data.to_csv("dataset/year.csv")
    year_data.to_csv("dataset/year_1116.csv")
# get_years()

# 调出多年平均的降水和蒸散发
def get_p_et():
    data = pd.read_csv(r"dataset/observation_based_approach_result.csv")
    FileName = data['FileName']
    Area = data['Area']
    Name = data['Name']
    p_et_data = pd.DataFrame([])
    for i in range(len(Area)):
        if Area[i]<=200000:
            d = pd.read_csv(r"dataset/small_basins_data_Yearly/"+FileName[i]+r".csv")
            year = np.ravel(d['Year'])
            p = np.ravel(d['P_MSWEP'])
            et = np.ravel(d['PET_FAO_CO2'])
            p1 = p[year>1980]
            et1 = et[year>1980]
            y1 = year[year>1980]
            p2 = p1[y1<2021]
            et2 = et1[y1<2021]
            P = np.nanmean(p2)
            ET = np.nanmean(et2)
            p_et_data[Name[i]] = [P, ET]
    p_et_data.index = ['P', 'ET_yang']
    # p_et_data.to_csv("dataset/p_et.csv")
    p_et_data.to_csv("dataset/p_et_1116.csv")
# get_p_et()

# 调出多年气温相关
def get_temp():
    data = pd.read_csv(r"dataset/observation_based_approach_result.csv")
    FileName = data['FileName']
    Area = data['Area']
    Name = data['Name']
    t_data = pd.DataFrame([])
    for i in range(len(Area)):
        if Area[i]<=200000:
            d = pd.read_csv(r"dataset/small_basins_data_Yearly/"+FileName[i]+r".csv")
            year = np.ravel(d['Year'])
            t = np.ravel(d['Temp'])
            tmax = np.ravel(d['Tmax'])
            tmin = np.ravel(d['Tmin'])
            t1 = t[year>1980]
            tmax1 = tmax[year > 1980]
            tmin1 = tmin[year > 1980]
            y1 = year[year>1980]
            t2 = t1[y1<2021]
            tmax2 = tmax1[y1 < 2021]
            tmin2 = tmin1[y1 < 2021]
            T = np.nanmean(t2)
            Tmax = np.nanmean(tmax2)
            Tmin = np.nanmean(tmin2)
            Td = Tmax-Tmin
            t_data[Name[i]] = [T, Tmax, Tmin, Td]
    t_data.index = ['Temp', 'Tmax', 'Tmin', 'Tdet']
    # p_et_data.to_csv("dataset/p_et.csv")
    t_data.to_csv("dataset/temp_1116.csv")
# get_temp()

# 把TRENDY数据的趋势都算出来
def get_trendy_trend():
    data = pd.read_csv(r"dataset/observation_based_approach_result.csv")
    Name = data['Name']
    # Name = pd.read_excel(r"dataset/name_1034.xlsx")['Name']
    year = pd.read_csv(r"dataset/year_1116.csv")
    trendy_name_runoff = ['CABLE_POP', 'CLASSIC', 'CLM5', 'DLEM', 'IBIS', 'ISAM',
                          'ISBA_CTRIP', 'JSBACH', 'JULES', 'LPJ_GUESS', 'LPX_Bern', 'ORCHIDEE',
                          'SDGVM', 'VISIT_NIES']
    S = np.zeros((len(trendy_name_runoff), len(Name)))
    for i in range(len(trendy_name_runoff)):
        d = pd.read_excel(r"./dataset/streamflow driven by CO2 from TRENDYS/"+trendy_name_runoff[i]+"_CO2_1116.xlsx")
        for j in range(len(Name)):
            q = np.array(d[str(Name[j])])
            y = np.array(year[str(Name[j])])
            q = np.float64(q)
            q[y==0] = np.NaN
            s = mk.original_test(q).slope
            S[i, j] = s
    S = pd.DataFrame(S, index=trendy_name_runoff, columns=Name)
    # S.to_csv("dataset/TRENDY_CO2_trend.csv")
    S.to_csv("dataset/TRENDY_CO2_trend_1116.csv")
# get_trendy_trend()

def get_fullt_differential_trend():
    data = pd.read_csv(r"dataset/observation_based_approach_result.csv")
    FileName = data['FileName']
    Area = data['Area']
    Name = data['Name']
    k_co2 = data['PET_FAO_YANG_par_CO2']
    s_data = pd.DataFrame([])
    for i in range(len(Area)):
        if Area[i]<=100000:
            d = pd.read_csv(r"dataset/small_basins_data_Yearly/" + FileName[i] + r".csv")
            year = np.ravel(d['Year'])
            q_day = np.ravel(d['n_flow'])
            q = np.ravel(d['Flow_mm'])
            q_day1 = q_day[year>1980]
            q1 = q[year>1980]
            y1 = year[year>1980]
            q_day2 = q_day1[y1<2021]
            q2 = q1[y1<2021]
            q2[q_day2<365] = np.NaN
            s = mk.original_test(q2).slope
            s_co2 = s * k_co2[i]
            s_data[Name[i]] = [s_co2, s]
    s_data.index = ['Q_CO2_trend', 'Q_trend']
    # s_data.to_csv("dataset/fully_differential_trend.csv")
    s_data.to_csv("dataset/fully_differential_trend_1116.csv")
# get_fullt_differential_trend()

trendy_name_runoff = ['CABLE_POP', 'CLASSIC', 'CLM5', 'DLEM', 'IBIS', 'ISAM',
                          'ISBA_CTRIP', 'JSBACH', 'JULES', 'LPJ_GUESS', 'LPX_Bern', 'ORCHIDEE',
                          'SDGVM', 'VISIT_NIES']
trendy_name = ['CABLE-POP', 'CLASSIC', 'CLM5.0', 'DLEM', 'IBIS', 'ISAM', 'ISBA-CTRIP', 'JSBACH',
                'JULES', 'LPJ-GUESS', 'LPX-Bern', 'ORCHIDEE', 'SDGVM', 'VISIT-NIES']
data = pd.read_excel(r"dataset\手动整合的图2数据_1116.xlsx")
P = np.ravel(data['P'])
ET = np.ravel(data['ET_yang'])
TEMP = np.ravel(data['Temp'])
FDM = np.ravel(data['FDM'])
LAI = np.ravel(data['LAI_annual_mean'])
data2 = pd.read_excel(r"dataset\info_1116.xlsx")
Main_climate = np.ravel(data2['Main_climate'])
forest = np.ravel(data2['forest'])
pasture = np.ravel(data2['pasture'])
lat = data2['Lat']

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
            # print(i * s, (i + 1) * s)
        else:
            pm.append(np.median(P_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            fdmm.append(np.median(FDM_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            std.append(np.std(FDM_NEW[i * s - p*1:(i + 1) * s - (p+1)]))
            p = p+1
            # print(i * s - p*1, (i + 1) * s - (p+1))
        k = k + 1
    # pm.append(np.median(P_NEW[k * num:]))
    # fdmm.append(np.median(FDM_NEW[k * num:]))
    # std.append(np.std(FDM_NEW[k * num:]))
    # # print(len(P_NEW[k * num:]))
    return pm, fdmm, std

def p1(ax, d, num):
    RHO, P = [], []
    x, y, z = get_sort(d, FDM, num)
    pc = pearsonr(x, y)
    print("FDM", pc[0], pc[1])
    ax.plot(x, y, c='k', ls='-', lw=2,
             # markersize=2, marker='o', markeredgewidth=0.5,
             # markerfacecolor='None', markeredgecolor=colors[int(0%5)],
             label='Observation-based\ndataset')
    RHO.append(pc[0])
    P.append(pc[1])
    Y = np.zeros((len(trendy_name_runoff), len(x)))
    for i in range(len(trendy_name_runoff)):
        t = np.ravel(data[trendy_name_runoff[i]])
        x, y, z = get_sort(d, t, num)
        ax.plot(x, y, c=colors[int(i % 5)], ls=ls[int(i % 3)], lw=1,
                 # markersize=2, marker='o', markeredgewidth=0.5,
                 # markerfacecolor='None', markeredgecolor=colors[int(0 % 5)],
                 label=trendy_name[i])
        Y[i, :] = y
        pc = pearsonr(x, y)
        print(trendy_name_runoff[i], pc[0], pc[1])
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

def p2(ax, RHO1, P1):
    color = ['red', 'orange', 'yellow', 'white']
    # for i in range(4):
    #     plt.bar(x=0.125+i*0.25, height=21, bottom=-1, width=0.25, color=color[3-i], alpha=0.1)
    # for i in range(4):
    #     plt.bar(x=-0.125-i*0.25, height=21, bottom=-1, width=0.25, color=color[3-i], alpha=0.1)
    plt.bar(x=-0.85, height=21, bottom=-1, width=0.3, color=color[1], alpha=0.2)
    plt.bar(x=0.85, height=21, bottom=-1, width=0.3, color=color[1], alpha=0.2)
    prho(ax, RHO1[0], 16, P1[0], markersize=10, marker='v', markeredgewidth=1.5,
         markerfacecolor='None', markeredgecolor=colors[0], label='p$<0.05$')
    t1, t2 = 0, 0
    for i in range(14):
        if t1 == 0 and P1[i+1]<0.05:
            prho(ax, RHO1[i+1], 14-i, P1[i+1],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label='p$<0.05$')
            t1 = 1
        elif t2 == 0 and P1[i+1]>=0.05:
            prho(ax, RHO1[i + 1], 14 - i, P1[i + 1],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label='p$\geq0.05$')
            t2 = 1
        else:
            prho(ax, RHO1[i + 1], 14 - i, P1[i + 1],
                 markersize=8, marker='o', markeredgewidth=1.5,
                 markerfacecolor='None', markeredgecolor=colors[1], label=None)
    # ax.plot(RHO1[1:], [14-i for i in range(14)], ls='--', lw=0.5, c=colors[1])

fig = plt.figure(figsize=(13, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
marker = ['^', '*', 'o']
ls = [':', '--', '-.']
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
ax = fig.add_subplot(241)
# plt.title("a", loc="left", pad=10, fontfamily='serif', weight="bold", fontsize=20)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
# ax.spines[['right', 'top']].set_visible(False)
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
ax.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)
RHO1, P1 = p1(ax, P, 22)

plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([-0.4+0.1*i for i in range(13)], fontfamily='serif', fontsize=10)
# plt.xlim([0, 240])
plt.ylim([-0.4, 0.8])
plt.ylabel("Q change driven by CO$_2$ (mm yr$^{-2}$)", fontfamily='serif', fontsize=12)
plt.xlabel("P (mm yr$^{-1}$)", fontfamily='serif', labelpad=5, fontsize=12)
plt.title("Precipitation", fontfamily='serif', fontsize=15)
plt.title("a", loc='left', fontfamily='serif', fontsize=18, weight='bold')

ax = fig.add_subplot(242)
# plt.title("a", loc="left", pad=10, fontfamily='serif', weight="bold", fontsize=20)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
# ax.spines[['right', 'top']].set_visible(False)
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
ax.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)
plt.plot([1, 1], [-1, 1], ls="-", lw=1, c='r', alpha=0.2)

RHO2, P2 = p1(ax, ET/P, 22)
handles1, labels1 = ax.get_legend_handles_labels()

plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([-0.4+0.1*i for i in range(13)],['']*13,fontfamily='serif', fontsize=10)
# plt.xlim([0, 240])
plt.ylim([-0.4, 0.8])
# plt.ylabel("Q driven by CO$_2$ (mm yr$^{-1}$)", fontfamily='serif', fontsize=12)
plt.xlabel("Aridity [PET/P] ($-$)", fontfamily='serif', labelpad=5, fontsize=12)
plt.title("Aridity", fontfamily='serif', fontsize=15)
plt.title("b", loc='left', fontfamily='serif', fontsize=18, weight='bold')

ax = fig.add_subplot(243)
# plt.title("a", loc="left", pad=10, fontfamily='serif', weight="bold", fontsize=20)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
# ax.spines[['right', 'top']].set_visible(False)
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
ax.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)

RHO3, P3 = p1(ax, TEMP, 22)
# handles1, labels1 = ax.get_legend_handles_labels()

plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([-0.4+0.1*i for i in range(13)],['']*13,fontfamily='serif', fontsize=10)
# # plt.xlim([0, 240])
plt.ylim([-0.4, 0.8])
# plt.ylabel("Q driven by CO$_2$ (mm yr$^{-1}$)", fontfamily='serif', fontsize=12)
plt.xlabel("T ($℃$)", fontfamily='serif', labelpad=5, fontsize=12)
plt.title("Temperature", fontfamily='serif', fontsize=15)
plt.title("c", loc='left', fontfamily='serif', fontsize=18, weight='bold')

ax = fig.add_subplot(245)
# plt.title("a", loc="left", pad=10, fontfamily='serif', weight="bold", fontsize=20)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
# ax.spines[['right', 'top']].set_visible(False)
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
# ax.grid(axis='x', ls="--", lw=1, c='k', alpha=0.25)
p2(ax, RHO1, P1)
plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([16]+[14-i for i in range(14)], ['Observation-\n-based dataset']+trendy_name, fontfamily='serif', fontsize=10)
plt.xlim([-1.1, 1.1])
plt.ylim([0, 17])
# plt.ylabel("Q driven by CO$_2$ (mm yr$^{-1}$)", fontfamily='serif', fontsize=12)
# plt.xlabel("Aridity [PET/P] ($-$)", fontfamily='serif', labelpad=5, fontsize=12)
plt.xlabel("Rank correlation $\\rho_s$ ($-$)", fontfamily='serif', labelpad=3, fontsize=11)
plt.title("Precipitation", fontfamily='serif', fontsize=15)
plt.title("e", loc='left', fontfamily='serif', fontsize=18, weight='bold')

ax = fig.add_subplot(246)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
p2(ax, RHO2, P2)
plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([16]+[14-i for i in range(14)], ['']*15, fontfamily='serif', fontsize=10.5)
plt.xlim([-1.1, 1.1])
plt.ylim([0, 17])
handles2, labels2 = ax.get_legend_handles_labels()
plt.xlabel("Rank correlation $\\rho_s$ ($-$)", fontfamily='serif', labelpad=3, fontsize=11)
plt.title("Aridity", fontfamily='serif', fontsize=15)
plt.title("f", loc='left', fontfamily='serif', fontsize=18, weight='bold')

ax = fig.add_subplot(247)
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
p2(ax, RHO3, P3)
plt.xticks(fontfamily='serif', fontsize=10)
plt.yticks([16]+[14-i for i in range(14)], ['']*15, fontfamily='serif', fontsize=10.5)
plt.xlim([-1.1, 1.1])
plt.ylim([0, 17])
plt.xlabel("Rank correlation $\\rho_s$ ($-$)", fontfamily='serif', labelpad=3, fontsize=11)
plt.title("Temperature", fontfamily='serif', fontsize=15)
plt.title("g", loc='left', fontfamily='serif', fontsize=18, weight='bold')

def pp(ax1, k=2, title1="a", title2="Total"):
    # plt.title("a", loc="left", pad=10, fontfamily='serif', weight="bold", fontsize=20)
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
    ax1.grid(axis='y', ls="--", lw=1, c='k', alpha=0.25)
    plt.xticks(fontfamily='serif', fontsize=10)
    if k==-1:
        RHO1, P1 = p1(ax1, LAI, 22)
        # plt.ylabel("Q change driven by CO$_2$ (mm yr$^{-2}$)", fontfamily='serif', fontsize=11)
        # plt.xlabel("mean annual LAI (-)", fontfamily='serif', labelpad=3, fontsize=11)
        # plt.yticks([-0.4 + 0.1 * i for i in range(13)], fontfamily='serif', fontsize=10)
        plt.xlabel("LAI (-)", fontfamily='serif', labelpad=3, fontsize=12)
        plt.yticks([-0.4 + 0.1 * i for i in range(13)], [""]*13, fontfamily='serif', fontsize=10)
    else:
        LAI_need = LAI[Main_climate == k]
        forest_need = forest[Main_climate == k]
        RHO1, P1 = p1(ax1, LAI_need[forest_need >= 50], 6)
        print(len(LAI_need[forest_need >= 50]))
        plt.ylabel("", fontfamily='serif', fontsize=10)
        plt.xlabel("mean annual LAI (-)", fontfamily='serif', labelpad=3, fontsize=11)
        plt.yticks([-0.4 + 0.1 * i for i in range(13)], ['']*13, fontfamily='serif', fontsize=10)
    ax1.set_ylim([-0.4, 0.8])

    plt.title(title2, fontfamily='serif', fontsize=15)
    plt.title(title1, loc='left', fontfamily='serif', fontsize=18, weight='bold')
    ax1.patch.set_alpha(0)
    return RHO1, P1

def pp2(ax2, RHO1, P1, k=-1, title1="b", title2="Total"):
    p2(ax2, RHO1, P1)
    plt.xticks(fontfamily='serif', fontsize=10)
    if k==-1:
        plt.yticks([16]+[14-i for i in range(14)], ['Benchmark\ndatasets and\ntheory']+trendy_name, fontfamily='serif', fontsize=10)
    else:
        plt.yticks([16] + [14 - i for i in range(14)], ['']*15, fontfamily='serif', fontsize=10)
    plt.xlim([-1.1, 1.1])
    plt.ylim([0, 17])
    plt.xlabel("Rank correlation $\\rho_s$ ($-$)", fontfamily='serif', labelpad=3, fontsize=11)
    plt.title(title2, fontfamily='serif', fontsize=15)
    plt.title(title1, loc='left', fontfamily='serif', fontsize=18, weight='bold')
    ax2.patch.set_alpha(0)

ax1 = fig.add_subplot(244)
RHO1, P1 = pp(ax1, k=-1, title1="d", title2="LAI")
ax2 = fig.add_subplot(248)
pp2(ax2, RHO1, P1, k=0, title1="h", title2="LAI")

legend_font = {
        'family': 'serif',
        'style': 'normal',
        'size': 11,
        'weight': "normal", 
    }
fig.legend(handles1+handles2, labels1+labels2, loc='lower center',
           # bbox_to_anchor=[0.56, 0.99],
           prop=legend_font, ncol=6)

fig.patch.set_alpha(1.0)
plt.tight_layout()
plt.subplots_adjust(
    top=0.951,
    bottom=0.19,
    left=0.09,
    right=0.986,
    hspace=0.376,
    wspace=0.093
)
plt.rcParams['savefig.dpi'] = 2000
plt.show()
