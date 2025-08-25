#v00: 27/11/24 (from databoard00), 19/08/25 modified
#v01: 21/08/25 (sta), simplified for github; modified
#v02: 21/08/25 (sta), very modified options
import sys
import pandas as pd
import fondoA, fondoB, fondoC, fondoD, fondoE
import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
global Afps
Afps = {'A': fondoA.lis_fondoA, 'B': fondoB.lis_fondoB, 'C': fondoC.lis_fondoC,
        'D': fondoD.lis_fondoD, 'E': fondoE.lis_fondoE}

global lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE
lis_valsA = [x[1] for x in Afps['A']]
lis_valsB = [x[1] for x in Afps['B']]
lis_valsC = [x[1] for x in Afps['C']]
lis_valsD = [x[1] for x in Afps['D']]
lis_valsE = [x[1] for x in Afps['E']]

global lis_day, lis_all, lis_dates 
#afp.afp_fdoA = [('01-04-2002', 10000),...]
lis_day = [x[1] for x in Afps['A']]
lis_all = Afps['A']
lis_dates = [x for x in range(len(fondoA.lis_fondoA))]
       
def submit_data():
    global fechas_user, Dates00
    Dates00 = []
    Res, Res2 = [],[]
    fechas_user = [entry0.get()]  # Get the text entered
    for i, st in enumerate(fechas_user):
        aa = st.split()
        bb = st.split(',')
        if len(aa)==2:
            Res.append(aa)
        if len(bb)==2:
            Res.append(bb)
    for x in Res:
        temp =[]
        for y in x:
            z = (y.replace(' ','')).replace(',','')
            temp.append(z)
        Res2.append(tuple(temp))
    Res2 = list(set(Res2))
    #case text entered: indices (ej: 1000 1500)
    if len(Res2[0][0])<= 4 and len(Res2[0][1])<= 4:
        print('datos ok (indices)')
        Dates00 = sorted([int(Res2[0][0]),int(Res2[0][1])])
        return Dates00
    #case text entered: fechas (ej: 01-03-2010, 31-12-2010)
    else:
        for x in Res2[0]:
            FFs = []
            fech = x.split('-')
            day, mon, yea = int(fech[0]), int(fech[1]), int(fech[2])
            if (day >=1 and day <=31) and (mon >=1 and mon <=12) and (yea >=2002 and yea <=2025):
                if len(str(day))== 1:
                    day0 = '0'+str(day)
                else:
                    day0 = str(day)
                if len(str(mon))== 1:
                    mon0 = '0'+str(mon)
                else:
                    mon0 = str(mon)        
                FFs.append('-'.join([day0,mon0,str(yea)])) #original
                
                for fecha in FFs:
                    #1st search (exact):
                    print(f"fecha: {fecha}")
                    ready = False
                    for j, y in enumerate(Afps['A']):
                        if fecha == y[0]:
                            Dates00.append(j)
                            ready = True
                            break
                    if ready:
                        break
                    #2nd search (aprox):   
                    dt_user = datetime.strptime(fecha, '%d-%m-%Y')
                    num_user = int(dt_user.strftime("%Y%m%d"))
                    for j, y in enumerate(Afps['A']):
                        dt = datetime.strptime(y[0], '%d-%m-%Y')
                        num = int(dt.strftime("%Y%m%d"))
                        if num >= num_user:
                            Dates00.append(j-1)
                            break
        print('datos ok (fechas)')
        return sorted(Dates00)


def getdat(event):
    print(f"Ultimos datos ({Afps['A'][-1][0]}):")
    print(f"fondo A: {Afps['A'][-1][1]}")
    print(f"fondo B: {Afps['B'][-1][1]}")
    print(f"fondo C: {Afps['C'][-1][1]}")
    print(f"fondo D: {Afps['D'][-1][1]}")
    print(f"fondo E: {Afps['E'][-1][1]}")

def gr_(event):
    def graph_mlines(lis_x, Mlis_y):
        xvals = [x for x in range(len(lis_x))]
        plt.figure(figsize=(12,6))
        plt.grid(color='0.95')
        dic_fondos = {0:'A',1:'B',2:'C',3:'D',4:'E'}
        for i, yvals in enumerate(Mlis_y):
            plt.plot(xvals, yvals, label = f'fondo {dic_fondos[i]}', linewidth=0.5)
        plt.xlabel("dias")
        plt.ylabel("valor cuota")
        plt.title("AFP fondos")
        plt.legend()
        plt.show()

    graph_mlines(lis_dates, [lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE])

def gr_slog(event):
    def graph_mlines_slog(lis_x, Mlis_y):
        xvals = [x for x in range(len(lis_x))]
        plt.figure(figsize=(12,6))
        plt.grid(color='0.95')
        dic_fondos = {0:'A',1:'B',2:'C',3:'D',4:'E'}
        for i, yvals in enumerate(Mlis_y):
            plt.semilogy(xvals, yvals, label = f'fondo {dic_fondos[i]}', linewidth=0.5)
        plt.xlabel("dias")
        plt.ylabel("valor cuota")
        plt.title("AFP fondos (gráfico semilog)")
        plt.legend()
        plt.show()

    graph_mlines_slog(lis_dates, [lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE])

def rent_histo(event):
    Ren_his, Ren_his_anu = [], []
    date_start = datetime.strptime(Afps['A'][0][0], "%d-%m-%Y")
    date_end = datetime.strptime(Afps['A'][-1][0], "%d-%m-%Y")
    delta_max = (date_end - date_start).days
    for lis in [lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE]:
        rent_hist = round((lis[-1] - lis[0])/lis[0], 3)
        rent_hist_anual = round(rent_hist / (delta_max/365), 3)
        Ren_his.append(f"{round(rent_hist*100, 1)}%")
        Ren_his_anu.append(f"{round(rent_hist_anual*100, 1)}%")
    Ren_his.insert(0, 'Renta histórica    :')
    Ren_his_anu.insert(0, 'Renta histórica/año:')
    Disp = [Ren_his, Ren_his_anu]
    Disp2 = pd.DataFrame(Disp, columns = ('Fondo'+14*' '+':','A','B','C','D','E'))
    print('-'*55)
    print(Disp2.to_string(justify='left',index=False))
    
def tramo_graf_rent(event):    
    def gr_mlines_tramo_rent(lis_x, Mlis_y, sta_end):
        sta, end = sta_end[0], sta_end[1]
        sta_date = Afps['A'][sta][0]
        end_date = Afps['A'][end][0]
        
        #rent calc:
        Ren_tram = []
        date_start = datetime.strptime(Afps['A'][sta][0], "%d-%m-%Y")
        date_end = datetime.strptime(Afps['A'][end][0], "%d-%m-%Y")
        delta_max = (date_end - date_start).days
        for lis in [lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE]:
            rent_tram = round((lis[end] - lis[sta])/lis[sta], 3)
            Ren_tram.append(f"({round(rent_tram*100, 1)}%)")

        #chart:
        xvals = [x for x in range(len(lis_x))]
        plt.figure(figsize=(12,6))
        plt.grid(color='0.95')
        dic_fondos = {0:'A',1:'B',2:'C',3:'D',4:'E'}
        for i, yvals in enumerate(Mlis_y):
            plt.plot(xvals[sta:end], yvals[sta:end], label = f'fondo {dic_fondos[i]} {Ren_tram[i]}', linewidth=0.5)                
        plt.title(f"Renta: {sta_date} a {end_date}")
        plt.legend()
        plt.show()   

    if len(Dates00)==2:
        gr_mlines_tramo_rent(lis_day, [lis_valsA, lis_valsB, lis_valsC, lis_valsD, lis_valsE], Dates00)
    else:
        print('Ingresar datos')


#start--------------------------------------------------------

vent = tk.Tk()
vent.geometry("180x350")
vent.configure(bg='khaki')
vent.title("AFP")

# Add a label for title:
lab00 = tk.Label(vent, text="AFP datos", font=("Arial",12,"bold"), bg='khaki', anchor="w")

com_wid = 21
butt1 = tk.Button(vent, text=f'Ultimos datos', anchor="w", width=com_wid)
butt2 = tk.Button(vent, text=f'Gráfico histórico', anchor="w", width=com_wid)
butt3 = tk.Button(vent, text=f'Gráfico histórico - semilog', anchor="w", width=com_wid)
butt4 = tk.Button(vent, text=f'Rentabilidad histórica', anchor="w", width=com_wid)

lab01 = tk.Label(vent, text="Ingresar tramo:", bg='khaki', anchor="w")
lab02 = tk.Label(vent, text="Ej.: 01-03-2010, 31-12-2010", bg='khaki', anchor="w")
lab03 = tk.Label(vent, text="Ej.: 1000,1500 (ver gráfico)", bg='khaki', anchor="w")

# Add an Entry widget for data entry
entry0 = tk.Entry(vent, width=25)
# Add a button to handle the input
butt5 = tk.Button(vent, text="Aceptar", command=submit_data)

butt6 = tk.Button(vent, text=f'Gráfico/Renta por tramo', anchor="w", width=com_wid)

# Arrange buttons in a grid
aa = 0
lab00.grid(row=1, column=0, padx=5, pady=1)
butt1.grid(row=aa+3, column=0, padx=5, pady=5)
butt2.grid(row=aa+4, column=0, padx=5, pady=5)
butt3.grid(row=aa+9, column=0, padx=5, pady=5)
butt4.grid(row=aa+10, column=0, padx=5, pady=5)
lab01.grid(row=aa+15, column=0, padx=5, pady=0)
lab02.grid(row=aa+16, column=0, padx=5, pady=0)
lab03.grid(row=aa+17, column=0, padx=5, pady=0)
entry0.grid(row=aa+18, column=0, padx=5, pady=5)
butt5.grid(row=aa+19, column=0, padx=5, pady=5)
butt6.grid(row=aa+20, column=0, padx=5, pady=5)

butt1.bind('<Button-1>', getdat)
butt2.bind('<Button-1>', gr_)
butt3.bind('<Button-1>', gr_slog)
butt4.bind('<Button-1>', rent_histo)
butt6.bind('<Button-1>', tramo_graf_rent)
vent.mainloop()
