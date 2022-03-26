# 24 Oct 2021 : Seperated for common use
# 07 Jan 2022 : Week numbers +105 instead of +53
# 05 Feb 2022 : X ticks in Y2022 to be -105 (in Y2021 to be -53)
# 10 Feb 2022 : Y ticks error in 1.5M


import os
import math
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import warnings
import sys

from datetime import datetime
from matplotlib import gridspec


def mypath():
    sfile = str(os.path.realpath(__file__))
    for i in range(len(sfile)-1,1,-1) :
        if sfile[i] == '\\'  or sfile[i] == '/':
            break
    i0 = i
    for i in range(i0-1,1,-1) :
        if sfile[i] == '\\' or sfile[i] == '/':
            break
    #print(sfile[:i0+1], sfile[:i+1])
    return sfile[:i0+1], sfile[:i+1]

myPath, myPath0 = mypath()

try:
    myfile = open(myPath+"yaxis.in", "r", encoding="utf8")
    lines = myfile.readlines() 
    myfile.close()
    if len(lines) == 5:
        y = [ int(lines[1])*10, int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]) ]
    elif len(lines) == 6:
        y = [ int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5]) ]
except:
    y = [ 100000000, 5000000, 2000000, 1000000, 500000 ]


def lines(scondition) :
    if scondition == "Europe" :
        lt = "-"
    elif scondition == "Asia" :
        lt = "--"
    elif scondition == "America":
        lt = "-."
    elif scondition == "Oceania":
        lt = "b:"
    else :
        lt = ":"
    return lt


def longnameeach(scountry, bflag) :
    if scountry[:13] == "United States" :
        sanswer = "USA"
    elif scountry == "United Kingdom" :
        sanswer = "UK "
    elif scountry == "United Arab Emirates" :
        sanswer = "UAE"
    elif scountry == "Dominican Republic" :
        sanswer = "Dominican R"
    elif scountry == "Bosnia and Herzegovina" or scountry == "Bosnia And Herzegovina" :
        sanswer = "Bos & Her"
    elif scountry == "North Macedonia" :
        sanswer = "N.Marcedonia"
    elif scountry == "Myanmar/Burma" :
        sanswer = "Myanmar"
    else :
        sanswer = scountry
    if bflag and sanswer[0:4] != "0.1x":
        sanswer = "0.1x" + sanswer
    return sanswer


def ytickrecomd(ymax) :
    det = math.log10(ymax)
    yd = int(ymax*pow(10, -int(det-1)))
#     if det == int(det) : yd *= 2
    if yd%7 == 0:
        ymajor = ymax//7
        yminor = ymajor//2
    elif yd%9 == 0:
        ymajor = ymax//3
        yminor = ymajor//3
    elif yd%6 == 0:
        ymajor = ymax//3
        yminor = ymajor//4
    elif yd%15 == 0:
        ymajor = ymax//3
        yminor = ymajor//5
    elif yd%25 == 0:
        ymajor = ymax//5
        yminor = ymajor//5
    elif yd%16 == 0:
        ymajor = ymax//4
        yminor = ymajor//4
    elif yd%20 == 0:
        ymajor = ymax//4
        yminor = ymajor//5
    else:
        ymajor = ymax//5
        yminor = ymajor//4
    return ymajor, yminor


def legdfontsize(id):
    if id > 39 :
        fontsize = 5.2
    elif id > 36 :
        fontsize = 5.4
    elif id > 33 :
        fontsize = 5.5
    elif id > 31 :
        fontsize = 6
    else :
        fontsize = 7
    return fontsize


def graphs(sfilename, x_data, y_data, c_data, icountry) :
    global y
    #print(x_data)
    plt.figure(figsize=(19, 10))
    n_fig = 8
    ax = [i for i in range(n_fig)]
    gs = gridspec.GridSpec(nrows=2, ncols=n_fig//2, height_ratios=[9, 5], width_ratios=[1, 1, 1, 1])
    for i in range(n_fig): ax[i] = plt.subplot(gs[i])
    idgrc = [0, 0, 0, 0]
    for i in range(0, len(icountry)-1) :
        if icountry[i][1].find("total") > 0:
            continue
        bflag = False
        istart = icountry[i][0]
        istop  = (icountry[i][0]+icountry[i+1][0])//2
        xs = x_data[istart:istop]
        ys = y_data[istart:istop, :]
        for k in range(len(ys)) :
            if math.isnan(ys[k][0]):
               ys[k][0] = ys[k-1][0]
        iend = len(ys)-1
        if (y[1] < ys[iend,0]) or (y[1]//50 < ys[iend,1]) :
            idgr = 0
            idgrc[0] += 1
        elif (y[2] < ys[iend,0]) or (y[2]//50 < ys[iend,1]) :
            idgr = 1
            idgrc[1] += 1
        elif (y[3] < ys[iend,0] < y[2]) or (y[3]//50 < ys[iend,1] < 0.05*y[2]):
            idgr = 2
            idgrc[2] += 1
        elif icountry[i][1] == "South Korea":
            idgr = 3
            idgrc[3] += 1
        elif (y[4] < ys[iend,0] < y[3]) or (y[4]//50 < ys[iend,1] < 0.05*y[3]):
            idgr = 3
            idgrc[3] += 1
        else :
            idgr = 4
        if idgr < 4 :
            icountry[i][1] = longnameeach(icountry[i][1], bflag)
            if icountry[i][1] == "South Korea" :
                linets = 'b--'
            else :
                linets = lines(icountry[i][2])
            ax[idgr].plot(xs, ys[:,0], linets, label=icountry[i][1])
            ax[idgr+4].plot(xs, ys[:,1], linets, label=icountry[i][1])
            if idgr < 2  :
                ax[idgr].text(xs[iend], ys[iend,0], " "+icountry[i][1][0:3]+"_"+str(ys[iend,0]//1000)+"K", fontsize=5)
                ax[idgr+4].text(xs[iend], ys[iend,1], " "+icountry[i][1][0:3]+"_"+str(ys[iend,1]), fontsize=5)
            elif idgr == 2 :#and ( 0.4 < ys[iend,0] / y[idgr] < 0.99 ):
                ax[2].text(xs[iend], ys[iend,0], " "+icountry[i][1][0:3]+"_"+str(ys[iend,0]//1000)+"K", fontsize=5)
                ax[6].text(xs[iend], ys[iend,1], " "+icountry[i][1][0:3]+"_"+str(ys[iend,1]), fontsize=5)
            elif idgr == 3 and icountry[i][1] == "South Korea" :
                ax[3].text(xs[iend], ys[iend,0], " Kor"+"_"+str(int(ys[iend,0])), fontsize=5)
                ax[7].text(xs[iend], ys[iend,1], " Kor"+"_"+str(int(ys[iend,1])), fontsize=5)
            elif idgr == 3 : #and (0.6 < ys[iend,0] / y[idgr] < 0.99) :
                ax[3].text(xs[iend], ys[iend,0], " "+icountry[i][1][0:3]+"_"+str(ys[iend,0]//1000)+"K", fontsize=5)
                ax[7].text(xs[iend], ys[iend,1], " "+icountry[i][1][0:3]+"_"+str(ys[iend,1]), fontsize=5)
            else:
                pass
    week_start = 0
    thisweek = datetime.now().isocalendar()[1] + 105 # +53
    week_close = (int(thisweek)//13+2)*13
    warnings.simplefilter("ignore")
    for idgr in range(n_fig//2) :
        ax[idgr].axes.grid(True)
        ax[idgr].axes.legend(loc=2, fontsize=legdfontsize(idgrc[idgr]))
        ax[idgr].set_xlim(week_start, week_close)
        ax[idgr].xaxis.set_major_locator(ticker.MultipleLocator(13))
        xlbl = []
        for xi in ax[idgr].get_xticks().tolist():
            if xi < 1:
                xlbl.append("Wk")
            elif xi < 45 :
                xlbl.append(str(int(xi)))
            elif 44 < xi < 54 :
                xlbl.append("20."+str(int(xi)))
            elif 53 < xi < 67 :
                xlbl.append("21."+str(int(xi-53)))
            elif 105 < xi < 118 :
                xlbl.append("22."+str(int(xi-105)))
            elif 66 < xi < 105:
                xlbl.append(str(int(xi-53)))
            else :
                xlbl.append(str(int(xi-105)))
        ax[idgr].set_xticklabels(xlbl, fontsize=8)
        ax[idgr].set_ylim(0, y[idgr])
        ymajor, yminor = ytickrecomd(y[idgr])
        ax[idgr].yaxis.set_major_locator(ticker.MultipleLocator(ymajor))
        temp_tick = []
        for yi in ax[idgr].get_yticks().tolist():
            if yi >= 1.0E7 :
                temp_tick.append('{:2.0f}M'.format(yi//1E6))
            elif yi >= 1.0E6 :
                temp_tick.append('{:3.1f}M'.format((yi//1E5)*0.1))
            else:
                temp_tick.append('{:,g}K'.format(yi//1000))
        ax[idgr].set_yticklabels(temp_tick, fontsize=8)
        ax[idgr].yaxis.set_minor_locator(ticker.MultipleLocator(yminor))
        ax[idgr].yaxis.grid(True, which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.5)
        ax[idgr+4].axes.grid(True)
        ax[idgr+4].set_xlim(week_start, week_close)
        ax[idgr+4].xaxis.set_major_locator(ticker.MultipleLocator(13))
        #xlbl = []
        #for xi in ax[idgr+4].get_xticks().tolist():
        #    if xi < 1:
        #        xlbl.append("Wk")
        #    elif xi < 45 :
        #        xlbl.append(str(int(xi)))
        #    elif 44 < xi < 54 :
        #        xlbl.append("20."+str(int(xi)))
        #    elif 53 < xi < 67 :
        #        xlbl.append("21."+str(int(xi-53)))
        #    else :
        #        xlbl.append(str(int(xi-53)))
        ax[idgr+4].set_xticklabels(xlbl, fontsize=8)
        ax[idgr+4].set_ylim(0, y[idgr]//50) #10)
        ymajor, yminor = ytickrecomd(y[idgr]//50)
        ax[idgr+4].yaxis.set_major_locator(ticker.MultipleLocator(ymajor))
        ax[idgr+4].yaxis.set_minor_locator(ticker.MultipleLocator(yminor))
        temp_tick = []
        for yi in ax[idgr+4].get_yticks().tolist():
            if yi >= 1.0E7 :
                temp_tick.append('{:2.0f}M'.format(yi//1E6))
            elif yi >= 1.0E6 :
                temp_tick.append('{:3.1f}M'.format((yi//1E5)*0.1))
            else:
                temp_tick.append('{:,g}K'.format(yi//1000))
        ax[idgr+4].set_yticklabels(temp_tick, fontsize=8)
        ax[idgr+4].yaxis.grid(True, which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.5)
    warnings.simplefilter("default")
    ax[0].set_ylabel("Cumulative cases")
    ax[n_fig//2].set_ylabel("Cumulative death")
    plt.tight_layout()
    return ax