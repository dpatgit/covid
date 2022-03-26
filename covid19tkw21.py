#! /usr/bin/env python3
# 05 Sep 2020 : Move to TKINTER from Console
# 05 Sep 2020 : Last good run
# 28 Sep 2020 : Adding plt.show()
# 18 Oct 2020 : GridSpec and Axes
# 21 Nov 2020 : Modify all_date / data_today
# 09 Dec 2020 : 그림 보기 버튼
# 19 Dec 2020 : ECEC changes to weekly annoucement
# 15 Jan 2021 : Week number of Y2021
# 20 Feb 2021 : Image showing with PIL & matplotlib
# 10 Apr 2021 : Platform 
# 13 Jun 2021 : math for nan
# 05 Aug 2021 : Y axis from file
# 07 AUg 2021 : Four(4) graphs
# 02 Sep 2121 : Detecting OS
# 24 Oct 2021 : Seperation of common and this parts
# 07 Jan 2022 : Week numbers +105 instead of +53
# 05 Feb 2022 : X ticks in Y2022 to be -105 (in Y2021 to be -53)

# nadocoding tkinter
from tkinter import *
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk

# ecdc
import pandas as pd
import subprocess
from requests import get
from filecmp import cmp

from covid19_common import *


root = Tk()
root.title("COVID-19 Status by EU CDC with TKINTER")


def con_print(sline):
    txt_con.insert(END, "\n{0:s} {1:s}".format(str(datetime.now())[11:19], sline))
    txt_con.see(END)
    txt_con.update()
    return


# Date
date_frame = LabelFrame(root, text="대상일")
date_frame.pack(fill="x", padx=5, pady=5, ipady=5)

def anotherdate(event):
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 대상일 "+txt_date.get()+"로 변경"+"\n")
    #txt_con.see(END)
    con_print("Target Date changed to {0:s}\n".format(txt_date.get()))
    return

def all_date():
    if txt_date.get().find("*") == 8:
        txt_date.delete(0, END)
        txt_date.insert(0, str(datetime.now())[0:10])
        btn_date.config(text="Folder 전체")
    else:
        txt_date.delete(0, END)
        txt_date.insert(0, str(datetime.now())[0:8]+"**")
        btn_date.config(text="오늘")
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 대상일이 "+txt_date.get()+"(으)로 변경"+"\n")
    #txt_con.see(END)
    con_print("Target Date changed to {0:s}\n".format(txt_date.get()))
    return

txt_date = Entry(date_frame)
txt_date.insert(0, str(datetime.now())[0:10])
txt_date.bind("<Return>", anotherdate)

# txt_date.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)
txt_date.pack(side="left", fill="x", padx=5, pady=5, ipady=4)

btn_date = Button(date_frame, text="Folder 전체", width=12, command=all_date)
btn_date.pack(side="left", padx=5, pady=5)

p_var = DoubleVar()
progress_b = ttk.Progressbar(date_frame, maximum=100, variable=p_var)
progress_b.pack(side="right", fill="x",  expand=True, padx=5, pady=5)

# option frame
option_frame = LabelFrame(root, text="선택사항")
option_frame.pack(fill="x", padx=5, pady=5, ipady=5)

def calc1(event):
    y[1] = int(txt_y1.get().replace(",", ""))
    txt_y1.delete("0", END)
    txt_y1.insert(END, "{0:,d}".format(y[1]))
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 그래프 Y1 최대값이 "+txt_y1.get()+"(으)로 변경"+"\n")
    #txt_con.see(END)
    con_print("Maximum Y_1 changed to " + txt_y1.get() + "\n")


lbl_y1 = Label(option_frame, text="Y1", width=5)
lbl_y1.pack(side="left", padx=5, pady=5)
txt_y1 = Entry(option_frame, width=9)
txt_y1.insert(0, "{0:,d}".format(y[1]))
txt_y1.bind("<Return>", calc1)
txt_y1.pack(side="left", padx=5, pady=5)

def calc2(event):
    y[2] = int(txt_y2.get().replace(",", ""))
    txt_y2.delete("0", END)
    txt_y2.insert(END, "{0:,d}".format(y[2]))
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 그래프 Y2 최대값이 "+txt_y2.get()+"(으)로 변경"+"\n")
    #txt_con.see(END)
    con_print("Maximum Y_2 changed to " + txt_y2.get() + "\n")

lbl_y2 = Label(option_frame, text="Y2", width=5)
lbl_y2.pack(side="left", padx=5, pady=5)
txt_y2 = Entry(option_frame, width=9)
txt_y2.insert(0, "{0:,d}".format(y[2]))
txt_y2.bind("<Return>", calc2)
txt_y2.pack(side="left", padx=5, pady=5)

def calc3(event):
    y[3] = int(txt_y3.get().replace(",", ""))
    txt_y3.delete("0", END)
    txt_y3.insert(END, "{0:,d}".format(y[3]))
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 그래프 Y3 최대값이 "+txt_y3.get()+"(으)로 변경"+"\n")
    #txt_con.see(END)
    con_print("Maximum Y_3 changed to " + txt_y3.get() + "\n")


lbl_y3 = Label(option_frame, text="Y3", width=5)
lbl_y3.pack(side="left", padx=5, pady=5)
txt_y3 = Entry(option_frame, width=9)
txt_y3.insert(0, "{0:,d}".format(y[3]))
txt_y3.bind("<Return>", calc3)
txt_y3.pack(side="left", padx=5, pady=5)

def calc4(event):
    y[4] = int(txt_y4.get().replace(",", ""))
    txt_y4.delete("0", END)
    txt_y4.insert(END, "{0:,d}".format(y[4]))
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 그래프 표시 최소값이 "+txt_y4.get()+"(으)로 변경"+"\n")
    #txt_con.see(END)
    con_print("Minimum Y changed to " + txt_y4.get() + "\n")


lbl_y4 = Label(option_frame, text=" 최소환자수", width=10)
lbl_y4.pack(side="left", padx=5, pady=5)
txt_y4 = Entry(option_frame, width=9)
txt_y4.insert(0, "{0:,d}".format(y[4]))
txt_y4.bind("<Return>", calc4)
txt_y4.pack(side="left", padx=5, pady=5)

# run frame
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

# 210903 RPi or Windows
if sys.platform.startswith("win"):
    btn_close = Button(frame_run, fg="red", padx=5, pady=5, text="닫기", width=12, command=root.quit)
elif sys.platform.startswith("linux"):
    btn_close = Button(frame_run, fg="red", padx=5, pady=5, text="닫기", width=12, command=root.destroy)

btn_close.pack(side="right", padx=5, pady=5)


def figview():
    if str(txt_date.get())[-2:]=="**" :
        file_list = os.listdir(myPath)
        files_png = [file for file in file_list if file.endswith(".png")]
        files_png.sort(reverse=True)
        sfilename = files_png[0]
    else:
        sfilename = "ECDC_COVID19_" + str(txt_date.get()) + "_wA4.png"
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+" 그림 - "+sfilename+"\n")
    #txt_con.see(END)
    #txt_con.update()
    con_print("Showing Figure " + sfilename + "\n")

    
#   210903 RPi or Windows
    if sys.platform.startswith("win"):
        cmd = "start " + myPath + sfilename
    elif sys.platform.startswith("linux"):
        cmd= "gpicview "+ myPath + sfilename

    subprocess.call(cmd, shell=True)

btn_figview = Button(frame_run, padx=5, pady=5, text="그림 보기", width=12, command=figview)
btn_figview.pack(side="right", padx=5, pady=5)



def data_in(sfilename):
    #txt_con.insert(END, "\n"+str(datetime.now())[11:19]+)
    #txt_con.see(END)
    #txt_con.update()
    con_print("Input from file "+sfilename)
    raw_data = pd.read_csv(myPath + sfilename)
    #txt_con.insert(END, "완료\n")
    #txt_con.see(END)
    #txt_con.update()
    raw_data = raw_data.sort_values(["continent", "country"], ascending=[True, True])
    x_data = raw_data.values[:, [6]]
    y_data = raw_data.values[:, [8, 8]]
    c_data = raw_data.values[:, [0, 2]]
    icntr = -1
    cntr_old = ""
    icountry = []
    for i in range(len(x_data)) :
#         print(i, x_data[i,0], "===>", x_data[i,0][:4], x_data[i,0][-2:], float(x_data[i,0][:4]) + float(x_data[i,0][-2:])*0.01)
        if (x_data[i,0]) [:4] == "2020" :
            x_data[i,0] = float(x_data[i,0][-2:])
        elif (x_data[i,0]) [:4] == "2021" :
            x_data[i,0] = float(x_data[i,0][-2:]) + 53
        elif (x_data[i,0]) [:4] == "2022" :
            x_data[i,0] = float(x_data[i,0][-2:]) + 105
            #print(x_data[i,0])
        else:
            pass
        if c_data[i, 0] != cntr_old :
            cntr_old = c_data[i, 0]
            icountry.append([ i, str(cntr_old), str(c_data[i][1]) ])
            icntr += 1
            if icntr > 0:
                ista = icountry[icntr-1][0]
                imid = (ista + i)//2
                y_data[ista:imid,1] = y_data[imid:i,0]
    icountry.append([len(x_data), "end", "end"])
    for i in range(len(icountry)-1):
        istart = icountry[i][0]
        istop  = (icountry[i][0]+icountry[i+1][0])//2
        istop2 = icountry[i+1][0]
        # print(i, icountry[i][1], istart, istop, istop2)
        for k in range(istop, istop2) :
            x_data[k] = "N"
            y_data[k,0] = y_data[k,1] = "N"
            c_data[k,0] = c_data[k,1] = "N"
        #print("삭제 후\n", y_data[istart:istop2, :])
    #txt_con.insert(END, str(datetime.now())[11:19]+" 구분 - {0:d}개 국가 및 {1:d}개 대륙".format(len(icountry)-1-5, 5)+"\n")
    #txt_con.see(END)
    #txt_con.update()
    con_print("Total {0:d} countries and {1:d} continents recognized\n".format(len(icountry)-1-5, 5))
    return x_data, y_data, c_data, icountry


def maingr(sfilename, x_data, y_data, c_data, icountry) :
    #txt_con.insert(END, str(datetime.now())[11:19]+" 처리중\n")
    #txt_con.see(END)
    #txt_con.update()
    con_print("Processing")
    ax = graphs(sfilename, x_data, y_data, c_data, icountry)

#   210903 RPi or Windows
    if sys.platform.startswith("win"):
        plt.get_current_fig_manager().window.state('zoomed')
#   elif sys.platform.startswith("linux"):
#       plt.show()
        
    sfilename = sfilename.replace(".csv", "_wA4.png")
    #txt_con.insert(END, str(datetime.now())[11:19]+" 저장 - {0:s}\n".format(sfilename))
    #txt_con.see(END)
    #txt_con.update()
    con_print("Saving {0:s}\n".format(sfilename))
    plt.savefig(sfilename)

    if (txt_date.get().find("**") > 0):
        plt.close()
    return True


def start():
    filename = "ECDC_COVID19_"
    p_var.set(0)
    progress_b.update()
    if txt_date.get().find("**") > 0 :
        file_list = os.listdir(myPath)
        files_csv = [file for file in file_list if file.endswith(".csv")]
        files_csv.sort()
        for idx, filename in enumerate(files_csv):
            x_data, y_data, c_data, icountry = data_in(filename)
            p_var.set(float(idx-0.5)/float(len(files_csv)-1)*100)
            progress_b.update()
            maingr(filename, x_data, y_data, c_data, icountry)
            p_var.set(float(idx)/float(len(files_csv)-1)*100)
            progress_b.update()
    else:
        file_name = filename + str(txt_date.get()) + ".csv"
        x_data, y_data, c_data, icountry = data_in(file_name)
        maingr(file_name, x_data, y_data, c_data, icountry)
    return
#

btn_start = Button(frame_run, padx=5, pady=5, text="처리 시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)


def data_today():
    sfilename = myPath + "Download"
    url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv"
    if txt_con.get("end-5c", "end-2c").find("음") == -1:
        txt_con.insert(END, "\n")
    #txt_con.insert(END, str(datetime.now())[11:19]+" ECDC 접속 중 " + "\n")
    #txt_con.update()
    con_print("Connecting ECDC ...")
    with open(sfilename, "wb") as file :
        try:
            response = get(url)
            file.write(response.content)
        except:
            #txt_con.insert(END, str(datetime.now())[11:19]+" CSV 파일 다운로드 실패" + "\n")
            #txt_con.update()
            con_print("CSV file download failed\n")
            
    file.close()
    #txt_con.insert(END, str(datetime.now())[11:19]+" CSV 파일 다운로드 완료 " + "\n")
    #txt_con.update()
    con_print("CSV file download completed\n")

    file_list = os.listdir(myPath)
    files_csv = [file for file in file_list if file.endswith(".csv")]
    files_csv.sort(reverse=True)
    for eachfile in files_csv:
        if cmp(myPath+eachfile, sfilename) == True :
            os.remove(sfilename)
            #txt_con.insert(END, str(datetime.now())[11:19]+" 최신파일 보유 " + eachfile + "\n")
            con_print("You have the latest file {0:s}".format(eachfile))
            txt_date.delete(0, END)
            txt_date.insert(0, eachfile[-14:-4])
            #txt_con.insert(END, str(datetime.now())[11:19]+" 대상일이 "+txt_date.get()+"(으)로 변경"+"\n")
            #txt_con.see(END)
            con_print("Target Date changed to {0:s}\n".format(txt_date.get()))
            return
    sfilename = "ECDC_COVID19_" + str(datetime.now())[0:10] + ".csv"
    os.replace(myPath+"Download", sfilename)
    #txt_con.insert(END, str(datetime.now())[11:19]+" 최신파일 다운 " + sfilename + "\n")
    #txt_con.see(END)
    con_print("The latest file downloded as {0:s}\n".format(sfilename))

    return

btn_start = Button(frame_run, padx=5, pady=5, text="업데이트 점검", width=12, command=data_today)
btn_start.pack(side="right", padx=5, pady=5)

# console frame
cout_frame = LabelFrame(root, text="현재상태")
cout_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_con = tkst.ScrolledText(cout_frame, height=12)
txt_con.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)
txt_con.insert(END, "Ready to serve\n")

root.resizable(False, False)
root.mainloop()
