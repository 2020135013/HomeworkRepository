"""
Yonsei University
2023-2 CCO1100.01
Computer Programming

Department: Astronomy
ID: 2020135013
Name: Seohyun Jang

Created  Date: 2023-11-20
Modified Date: 2023-11-20
"""
print('[CCO1100.01] 2023-2 Project : "Where Do The Olderly Go By Subway?"')

# import modules
import os
import datetime
import numpy as np
from numpy.lib import recfunctions as rfn
import matplotlib.pyplot as plt

################################ from ################################

import matplotlib
import matplotlib.font_manager as fm

fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/NanumMyeongjo.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)

# import congestion data, congestion 100% = 160, time for congestion21 data
name = np.genfromtxt("./서울교통공사_역별시간대별혼잡도_20221231.csv", dtype='U10', delimiter=",")[0]
dtype = []
for i in range(45):
    dtype.append((name[i], '<f8'))
dtype[1] = (name[1], '<U10')
dtype[4] = (name[4], '<U20')
dtype[5] = (name[5], '<U10')

congestion22 = np.genfromtxt("./서울교통공사_역별시간대별혼잡도_20221231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 43))
congestion21 = np.genfromtxt("./서울교통공사_역별시간대별혼잡도_20211231.csv", dtype=dtype[1:], skip_header=True, filling_values=0, delimiter=",", usecols=range(0, 42))
congestion19 = np.genfromtxt("./서울교통공사_혼잡도_20191231.csv", dtype=dtype[1:], skip_header=True, filling_values=0, delimiter=",", usecols=range(0, 42))

print(congestion22.shape)
print(congestion22.dtype)

################################# to #################################

# import elder data
name = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20221231.csv", dtype='U10', delimiter=",")[0]
dtype = []
for i in range(7):
    dtype.append((name[i], '<f8'))
dtype[3] = (name[3], '<U10')

elder22 = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20221231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 7))
elder21 = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20211231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 7))
elder20 = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20201231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 7))
elder19 = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20191231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 7))
elder18 = np.genfromtxt("./서울교통공사_역별 권종별 우대권 승차현황_20181231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 7))

print(elder22.dtype)

################################ from ################################

# import data by day
name = np.genfromtxt("./서울교통공사 2021년 일별 역별 시간대별 승하차인원(1_8호선).csv", dtype='U10', delimiter=",")[0]
dtype = []
for i in range(26):
    dtype.append((name[i], '<i8'))
dtype[1] = (name[1], '<U10')
dtype[2] = (name[2], '<U10')
dtype[4] = (name[4], '<U20')
dtype[5] = (name[5], '<U10')

byday23 = np.genfromtxt("./서울교통공사_역별 일별 시간대별 승하차인원_20230630.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 26))
byday22 = np.genfromtxt("./서울교통공사_역별 일별 시간대별 승하차인원 정보_20221231.csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 26))
byday21 = np.genfromtxt("./서울교통공사 2021년 일별 역별 시간대별 승하차인원(1_8호선).csv", dtype=dtype, skip_header=True, filling_values=0, delimiter=",", usecols=range(1, 26))
byday20 = np.genfromtxt("./서울교통공사 2020년 일별 역별 시간대별 승하차인원(1_8호선).csv", dtype=dtype[1:], skip_header=True, filling_values=0, delimiter=",", usecols=range(0, 25))

print(byday23.dtype)

byday = rfn.stack_arrays((byday20, byday21, byday22, byday23))
print(byday)

byday_ = np.genfromtxt("./서울시 지하철 호선별 역별 시간대별 승하차 인원 정보.csv", dtype='<U20', delimiter=",")[0:2]

# muim data
convert = lambda x: float(x.strip(b'""'))
converters={3: convert, 4: convert, 5: convert, 6: convert}
name = np.genfromtxt("./서울시 지하철 호선별 역별 유_무임 승하차 인원 정보.csv", dtype="<U20", delimiter=",")[0]
dtype = []
for i in range(7):
    if i < 3:
        dtype.append((name[i].strip('"'), '<U20'))
    else:
        dtype.append((name[i].strip('"'), '<i8'))
print(dtype)
muim = np.genfromtxt("./서울시 지하철 호선별 역별 유_무임 승하차 인원 정보.csv", skip_header=True, filling_values=0, converters=converters, dtype=dtype, delimiter=",")
for i in range(len(muim)):
    muim['사용월'][i] = muim['사용월'][i].strip('""')
    muim['호선명'][i] = muim['호선명'][i].strip('""')
    muim['지하철역'][i] = muim['지하철역'][i].strip('""')


# make npy files by station
for num in elder20['역번호']:
    station = byday[byday['역번호'] == num]
    station_name = station['역명'][0]
    
    station_muim = muim[(muim['지하철역'] == station['역명'][0]) & (muim['호선명'] == station['호선'][0])]
    station_line = station['호선'][0]
    
    station_cong22 = congestion22[congestion22['역번호'] == num]
    station_cong21 = congestion21[congestion21['역번호'] == num]
    station_cong19 = congestion19[congestion19['역번호'] == num]
    station_eld22 = elder22[elder22['역번호'] == num]
    station_eld21 = elder21[elder21['역번호'] == num]
    station_eld20 = elder20[elder20['역번호'] == num]
    station_eld19 = elder19[elder19['역번호'] == num]
    station_eld18 = elder18[elder18['역번호'] == num]

    station = rfn.rec_drop_fields(station, ['호선', '역번호', '역명'])
    station = rfn.rec_append_fields(station, ['유임', '무임', '경로', *[f'혼잡도{i}' for i in range(5, 24)]],
                                    [np.array([])] * 22, dtypes='<i8')
    
    try:
        for i in range(len(station)):
            # appending freeriding monthly data
            year = station['날짜'][i][0:4]
            month = station['날짜'][i][5:7]
            date = datetime.datetime.strptime(station['날짜'][i], "%Y-%m-%d").weekday()
            for j in range(len(station_muim)):
                if year+month == station_muim['사용월'][j]:
                    if i % 2 == 0:
                        station['유임'][i] = station_muim['유임승차인원'][j]
                        station['무임'][i] = station_muim['무임승차인원'][j]
                    else:
                        station['유임'][i] = station_muim['유임하차인원'][j]
                        station['무임'][i] = station_muim['무임하차인원'][j]
            
            # appending congestion data & elder data
            if year == '2022':
                for k in range(5, 24):
                    if date == 5:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '토요일'][f'{k}시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '토요일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong22[station_cong22['요일구분'] == '토요일'][f'{k}시30분'])*160)
                    elif date == 6:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '공휴일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '공휴일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong22[station_cong22['요일구분'] == '공휴일'][f'{k}시30분'])*160)
                    else:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '평일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong22[station_cong22['요일구분'] == '평일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong22[station_cong22['요일구분'] == '평일'][f'{k}시30분'])*160)
                station['경로'][i] = station_eld22['경로']
            elif year == '2021' or year == '2020':
                for k in range(5, 24):
                    if date == 5:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '토요일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '토요일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong21[station_cong21['요일구분'] == '토요일'][f'{k}시30분'])*160)
                    elif date == 6:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '공휴일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '공휴일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong21[station_cong21['요일구분'] == '공휴일'][f'{k}시30분'])*160)
                    else:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '평일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong21[station_cong21['요일구분'] == '평일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong21[station_cong21['요일구분'] == '평일'][f'{k}시30분'])*160)
                if year == '2021':
                    station['경로'][i] = station_eld21['경로']
                elif year == '2020':
                    station['경로'][i] = station_eld20['경로']
            elif year == '2019' or year == '2018':
                for k in range(5, 24):
                    if date == 5:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '토요일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '토요일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong19[station_cong19['요일구분'] == '토요일'][f'{k}시30분'])*160)
                    elif date == 6:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '공휴일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '공휴일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong19[station_cong19['요일구분'] == '공휴일'][f'{k}시30분'])*160)
                    else:
                        if k == 5:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '평일']['5시30분'])*160)
                        else:
                            station[f'혼잡도{k}'][i] = int(sum(station_cong19[station_cong19['요일구분'] == '평일'][f'{k}시00분'])*160 +\
                                                        sum(station_cong19[station_cong19['요일구분'] == '평일'][f'{k}시30분'])*160)
                if year == '2019':
                    station['경로'][i] = station_eld19['경로']
                elif year == '2018':
                    station['경로'][i] = station_eld18['경로']
            
            # byday data is not coincident by year
            if year == '2020' or year == '2022':
                station['23시_이후'][i] = station['23시_이후'][i] + station['합_계'][i]
                station['합_계'][i] = station['06시_이전'][i]
                for m in range(6,23):
                    if m < 9:
                        station['합_계'][i] += station[f'0{m}시0{m+1}시'][i]
                    elif m == 9:
                        station['합_계'][i] += station[f'0{m}시{m+1}시'][i]
                    else:
                        station['합_계'][i] += station[f'{m}시{m+1}시'][i]
                station['합_계'][i] += station['23시_이후'][i]
        
        # save array as station name
        np.save(f"./{int(num)}_{station_line}_{station_name}.npy", station)
    
    except:
        print(f"Error with appending with {num}_{station_line}_{station_name}")

print(station.dtype)

################################# to #################################

# check 1 : sum of day = month
s150_raw = np.load("./150_1호선_서울역.npy")
print(s150_raw.dtype)
# criteria
cri_cong = s150_raw['혼잡도5'] != 999999
s150 = s150_raw[cri_cong]
print(s150)

moneyhist, freehist, sumhist, years = [], [], [], []
for i in range(len(s150)):
    if i % 2 == 0:
        time = datetime.datetime.strptime(s150['날짜'][i], "%Y-%m-%d").date()
        if time.day == 1:
            moneyride150 = s150['유임'][i]
            freeride150 = s150['무임'][i]
            sum_ride = 0
        else:
            sum_ride += s150['합_계'][i]
            
        # print last day of month
        if (time + datetime.timedelta(1)).day == 1:
            print(f"{time.year}-{time.month}-{time.day} : money {moneyride150} + free {freeride150} = total {moneyride150+freeride150} vs. sum {sum_ride}")
            moneyhist.append(moneyride150)
            freehist.append(freeride150)
            sumhist.append(sum_ride)
            years.append(f"{time.year - 2000}.{time.month}")

# plot as bar for comparing
plt.figure(figsize=(20, 8))
plt.ticklabel_format(style = 'plain')
x_values1 = [2 * element + 0.82 * 1 for element in range(36)]
x_values2 = [2 * element + 0.82 * 2 for element in range(36)]
x_values = [2 * element + 0.82 * 1.5 for element in range(36)]
plt.bar(x_values1, freehist, label="free riders")
plt.bar(x_values1, moneyhist, bottom=freehist, label="money riders")
plt.bar(x_values2, sumhist, label="sum riders of days")
plt.xticks(x_values, years)
plt.title("Check the datasets, (sum of daily data == monthly data)?")
plt.legend()
plt.show()


# check 2 : sum of month = year
moneyrides_hist, freerides_hist, sumsumrides_hist, elders_hist = [], [], [], []
for i in range(len(s150)):
    if i % 2 == 0:
        time = datetime.datetime.strptime(s150['날짜'][i], "%Y-%m-%d")
        if time.month == 1 and time.day == 1:
            elders = s150['경로'][i]
            moneyrides = s150['유임'][i]
            freerides = s150['무임'][i]
            sum_sum_ride = 0
        else:
            if (time + datetime.timedelta(1)).day == 1:
                moneyrides += s150['유임'][i]
                freerides += s150['무임'][i]
            sum_sum_ride += s150['합_계'][i]
        if (time + datetime.timedelta(1)).month == 1 and (time + datetime.timedelta(1)).day == 1:
            print(f"{time.year}-{time.month}-{time.day} : elders {elders} vs. rides {moneyrides+freerides} vs. sum {sum_sum_ride}")
            print(f"diff = {moneyrides + freerides - sum_sum_ride} vs. elders {elders}")
            moneyrides_hist.append(moneyrides)
            freerides_hist.append(freerides)
            sumsumrides_hist.append(sum_sum_ride)
            elders_hist.append(elders)

# plot as bar for comparing
fig, ax = plt.subplots(1, 2, figsize=(20,8))
plt.ticklabel_format(style = 'plain')
xvalues1 = [2 * element + 0.82 * 1 for element in range(3)]
xvalues2 = [2 * element + 0.82 * 2 for element in range(3)]
xvalues = [2 * element + 0.82 * 1.5 for element in range(3)]
ax[0].bar(xvalues1, freerides_hist, label="free riders")
ax[0].bar(xvalues1, moneyrides_hist, bottom=freerides_hist, label="money riders")
ax[0].bar(xvalues2, sumsumrides_hist, label="sum riders of days")
ax[0].set_xticks(xvalues)
ax[0].set_xticklabels(['2020', '2021', '2022'])
ax[0].set_title("Check the datasets\n(sum of monthly data == annually data)?")
ax[0].legend(loc=2)

ax[1].bar(xvalues1, np.array(moneyrides_hist) + np.array(freerides_hist) - np.array(sumsumrides_hist),
          color='darkred', label="difference")
ax[1].bar(xvalues2, elders_hist, color='blue', label="elder riders")
ax[1].set_xticks(xvalues)
ax[1].set_xticklabels(['2020', '2021', '2022'])
ax[1].set_title("Maybe due to elder riders?")
ax[1].legend()
plt.show()

print("2020 경로", elder20[elder20['역번호']==150]['경로'])
print("2021 경로", elder21[elder21['역번호']==150]['경로'])            
print("2022 경로", elder22[elder22['역번호']==150]['경로'])

print("2020 장애", elder20[elder20['역번호']==150]['장애'])
print("2021 장애", elder21[elder21['역번호']==150]['장애'])            
print("2022 장애", elder22[elder22['역번호']==150]['장애'])

print("2020 유공자", elder20[elder20['역번호']==150]['유공자'])
print("2021 유공자", elder21[elder21['역번호']==150]['유공자'])            
print("2022 유공자", elder22[elder22['역번호']==150]['유공자'])

# elder ratio by year
elder_ratio22 = elder22[elder22['역번호']==150]['경로'] / (elder22[elder22['역번호']==150]['경로'] + elder22[elder22['역번호']==150]['장애'] + elder22[elder22['역번호']==150]['유공자'])
elder_ratio21 = elder21[elder21['역번호']==150]['경로'] / (elder21[elder21['역번호']==150]['경로'] + elder21[elder21['역번호']==150]['장애'] + elder21[elder21['역번호']==150]['유공자'])
elder_ratio20 = elder20[elder20['역번호']==150]['경로'] / (elder20[elder20['역번호']==150]['경로'] + elder20[elder20['역번호']==150]['장애'] + elder20[elder20['역번호']==150]['유공자'])


# check 3 : cong = ride - getoff + move = (free+money)ride - (free+money)getoff + (free+money=all)move
days = [0]
move, allmove = [], []
ride, getoff, cong, allcong = 0, 0, 0, 0
for i in range(len(s150)):
    time = datetime.datetime.strptime(s150['날짜'][i], "%Y-%m-%d").date()
    
    # move by month
    if i % 2 == 0:
        ride += s150['합_계'][i]
        for j in range(5, 24):
            cong += s150[f'혼잡도{j}'][i]
            allcong += s150[f'혼잡도{j}'][i]
    else:
        getoff += s150['합_계'][i]
        if (time + datetime.timedelta(1)).day == 1:
            move.append(cong - (ride - getoff))
            ride, getoff, cong = 0, 0, 0
    
    # allmove by month
    if time.day == 1:
        if i % 2 == 0:
            moneyride150 = s150['유임'][i]
            freeride150 = s150['무임'][i]
        else:
            moneygetoff150 = s150['유임'][i]
            freegetoff150 = s150['무임'][i]
            
    if (time + datetime.timedelta(1)).day == 1 and i % 2 != 0:
        days.append(days[-1] + time.day)
        allmove.append(allcong - (moneyride150 + freeride150 - moneygetoff150 - freegetoff150))
        allcong = 0

freemove = np.array(allmove) - np.array(move)

# from freemove, derive eldermove using elder_ratio
eldermove20 = freemove[0:366] * elder_ratio20
eldermove21 = freemove[366:366+365] * elder_ratio21
eldermove22 = freemove[366+365:366+365+365] * elder_ratio22
eldermove = np.append(np.append(eldermove20, eldermove21), eldermove22)

# make x-axis data
timestep_y = [(datetime.datetime.strptime('2020-01-01', "%Y-%m-%d").date() + datetime.timedelta(i)) for i in (0, 366, 366+365)]
timestep_m = [(datetime.datetime.strptime('2020-01-01', "%Y-%m-%d").date() + datetime.timedelta(i)) for i in days[:-1]]
timestep_d = [(datetime.datetime.strptime('2020-01-01', "%Y-%m-%d").date() + datetime.timedelta(i)) for i in range(366+365+365)]

# plot moving people
plt.figure(figsize=(8,8))
plt.scatter(timestep_m, freemove, label='free riders')
plt.scatter(timestep_m, eldermove, label='elder riders')
plt.xlabel("date")
plt.ylabel("# of moving people against total riders")
plt.title("Moving people in station 'Seoul'")
plt.legend()
plt.show()


# functionalization Check 3
def moving_elders(filename):
    num = int(filename.split("_")[0])
    station_name = filename.split("_")[2][:-4]
    data_raw = np.load(filename)
    
    cri_cong = data_raw['혼잡도5'] != 999999
    cri_money = data_raw['유임'] != 999999
    data = data_raw[cri_cong & cri_money]
    
    # elder ratio by year
    elder_ratio22 = elder22[elder22['역번호']==num]['경로'] / (elder22[elder22['역번호']==num]['경로'] + elder22[elder22['역번호']==num]['장애'] + elder22[elder22['역번호']==num]['유공자'])
    elder_ratio21 = elder21[elder21['역번호']==num]['경로'] / (elder21[elder21['역번호']==num]['경로'] + elder21[elder21['역번호']==num]['장애'] + elder21[elder21['역번호']==num]['유공자'])
    elder_ratio20 = elder20[elder20['역번호']==num]['경로'] / (elder20[elder20['역번호']==num]['경로'] + elder20[elder20['역번호']==num]['장애'] + elder20[elder20['역번호']==num]['유공자'])
    
    days = [0]
    move, allmove = [], []
    ride, getoff, cong, allcong = 0, 0, 0, 0
    for i in range(len(data)):
        time = datetime.datetime.strptime(data['날짜'][i], "%Y-%m-%d").date()

        # move by month
        if i % 2 == 0:
            ride += data['합_계'][i]
            for j in range(5, 24):
                cong += data[f'혼잡도{j}'][i]
                allcong += data[f'혼잡도{j}'][i]
        else:
            getoff += data['합_계'][i]
            if (time + datetime.timedelta(1)).day == 1:
                move.append(cong - (ride - getoff))
                ride, getoff, cong = 0, 0, 0

        # allmove by month
        if time.day == 1:
            if i % 2 == 0:
                global moneyride, freeride
                moneyride = data['유임'][i]
                freeride = data['무임'][i]
            else:
                global moneygetoff, freegetoff
                moneygetoff = data['유임'][i]
                freegetoff = data['무임'][i]

        if (time + datetime.timedelta(1)).day == 1 and i % 2 != 0:
            days.append(days[-1] + time.day)
            allmove.append(allcong - (moneyride + freeride - moneygetoff - freegetoff))
            allcong = 0

    freemove = np.array(allmove) - np.array(move)

    # from freemove, derive eldermove using elder_ratio
    eldermove20 = freemove[0:366] * elder_ratio20
    eldermove21 = freemove[366:366+365] * elder_ratio21
    eldermove22 = freemove[366+365:366+365+365] * elder_ratio22
    eldermove = np.append(np.append(eldermove20, eldermove21), eldermove22)
    
    return [freemove, eldermove]


# test file 2529_5호선_마포.npy
me2529 = moving_elders("2529_5호선_마포.npy")

# plot moving people 마포
plt.figure(figsize=(8,8))
plt.scatter(timestep_m, me2529[0], label='free riders')
plt.scatter(timestep_m, me2529[1], label='elder riders')
plt.xlabel("date")
plt.ylabel("# of moving people against total riders")
plt.title(f"Moving people in station 'Mapo'")
plt.legend()
plt.show()


# extract filename.npy
filelist = os.listdir()
filename = []
for file in filelist:
    if os.path.splitext(file)[1] == '.npy':
        filename.append(file)

# apply moving_elders function to all files
result_me = []
for file in filename:
    mes = moving_elders(file)[1]
    result_me.append([sum(mes), file])

# sorting result_me
result_me.sort()
print(result_me)


# for comparison, lowest 3 & highest 3
result_me_compare = result_me[0:3] + result_me[-3:]
for i in range(len(result_me_compare)):
    file = result_me_compare[i][1]
    globals()['compare{}'.format(i)] = moving_elders(file)

# plot 6 graphs
plt.figure(figsize=(20, 14))
for i in range(6):
    name = result_me_compare[i][1].split("_")[2][:-4]
    plt.subplot(2, 3, i+1)
    plt.plot(timestep_m, globals()['compare{}'.format(i)][0], label='free riders')
    plt.plot(timestep_m, globals()['compare{}'.format(i)][1], label='elder riders')
    plt.ylim(-13000, 2000)
    plt.xlabel("date")
    plt.ylabel("# of moving people against total riders")
    plt.title(f"Moving people in station '{name}'")
    plt.legend()
plt.show()


# freeride & freegetoff function
def free(filename):
    # same data import with moving_elders()
    num = int(filename.split("_")[0])
    station_name = filename.split("_")[2][:-4]
    data_raw = np.load(filename)
    
    cri_cong = data_raw['혼잡도5'] != 999999
    cri_money = data_raw['유임'] != 999999
    data = data_raw[cri_cong & cri_money]
    
    # ride & drop nums
    moneyride, freeride, moneygetoff, freegetoff = [], [], [], []
    for i in range(len(data)):
        time = datetime.datetime.strptime(data['날짜'][i], "%Y-%m-%d").date()
        if time.day == 1:
            if i % 2 == 0:
                moneyride.append(data['유임'][i])
                freeride.append(data['무임'][i])
            else:
                moneygetoff.append(data['유임'][i])
                freegetoff.append(data['무임'][i])
    
    return [freeride, freegetoff, moneyride, moneygetoff]


# free Seoul station
free150 = free("150_1호선_서울역.npy")

plt.figure(figsize=(15,7))
plt.subplot(1, 2, 1)
plt.ticklabel_format(style = 'plain')
plt.plot(timestep_m, free150[0], 'r', label="free ride")
plt.plot(timestep_m, free150[1], 'b', label="free get off")
plt.axvspan(datetime.datetime.strptime("2020.1.20.", "%Y.%m.%d."), datetime.datetime.strptime("2020.2.20.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.8.12.", "%Y.%m.%d."), datetime.datetime.strptime("2020.9.12.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.11.13.", "%Y.%m.%d."), datetime.datetime.strptime("2020.12.13.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2021.7.7.", "%Y.%m.%d."), datetime.datetime.strptime("2021.8.7.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.1.30.", "%Y.%m.%d."), datetime.datetime.strptime("2022.3.2.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.6.26.", "%Y.%m.%d."), datetime.datetime.strptime("2022.7.26.", "%Y.%m.%d."), alpha=0.25, color='gray')
plt.axvline(datetime.datetime.strptime("2022.4.25.", "%Y.%m.%d."), color='black', label="거리두기 해제")
plt.ylim(100000,1400000)
plt.xlabel("date")
plt.ylabel("population")
plt.title("코로나 대유행을 표시한 서울역 경로 우대권 승하차 인원")
plt.legend()

plt.subplot(1, 2, 2)
plt.ticklabel_format(style = 'plain')
plt.plot(timestep_m, free150[2], 'r', label="money ride")
plt.plot(timestep_m, free150[3], 'b', label="money get off")
plt.axvspan(datetime.datetime.strptime("2020.1.20.", "%Y.%m.%d."), datetime.datetime.strptime("2020.2.20.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.8.12.", "%Y.%m.%d."), datetime.datetime.strptime("2020.9.12.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.11.13.", "%Y.%m.%d."), datetime.datetime.strptime("2020.12.13.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2021.7.7.", "%Y.%m.%d."), datetime.datetime.strptime("2021.8.7.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.1.30.", "%Y.%m.%d."), datetime.datetime.strptime("2022.3.2.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.6.26.", "%Y.%m.%d."), datetime.datetime.strptime("2022.7.26.", "%Y.%m.%d."), alpha=0.25, color='gray')
plt.axvline(datetime.datetime.strptime("2022.4.25.", "%Y.%m.%d."), color='black', label="거리두기 해제")
plt.ylim(0,1500000)
plt.xlabel("date")
plt.ylabel("population")
plt.title("코로나 대유행을 표시한 서울역 일반 승하차 인원")
plt.legend()
plt.show()

# without ylim
plt.figure(figsize=(15,7))
plt.subplot(1, 2, 1)
plt.ticklabel_format(style = 'plain')
plt.plot(timestep_m, free150[0], 'r', label="free ride")
plt.plot(timestep_m, free150[1], 'b', label="free get off")
plt.axvspan(datetime.datetime.strptime("2020.1.20.", "%Y.%m.%d."), datetime.datetime.strptime("2020.2.20.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.8.12.", "%Y.%m.%d."), datetime.datetime.strptime("2020.9.12.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.11.13.", "%Y.%m.%d."), datetime.datetime.strptime("2020.12.13.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2021.7.7.", "%Y.%m.%d."), datetime.datetime.strptime("2021.8.7.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.1.30.", "%Y.%m.%d."), datetime.datetime.strptime("2022.3.2.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.6.26.", "%Y.%m.%d."), datetime.datetime.strptime("2022.7.26.", "%Y.%m.%d."), alpha=0.25, color='gray')
plt.axvline(datetime.datetime.strptime("2022.4.25.", "%Y.%m.%d."), color='black', label="거리두기 해제")
plt.xlabel("date")
plt.ylabel("population")
plt.title("코로나 대유행을 표시한 서울역 경로 우대권 승하차 인원")
plt.legend()

plt.subplot(1, 2, 2)
plt.ticklabel_format(style = 'plain')
plt.plot(timestep_m, free150[2], 'r', label="money ride")
plt.plot(timestep_m, free150[3], 'b', label="money get off")
plt.axvspan(datetime.datetime.strptime("2020.1.20.", "%Y.%m.%d."), datetime.datetime.strptime("2020.2.20.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.8.12.", "%Y.%m.%d."), datetime.datetime.strptime("2020.9.12.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2020.11.13.", "%Y.%m.%d."), datetime.datetime.strptime("2020.12.13.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2021.7.7.", "%Y.%m.%d."), datetime.datetime.strptime("2021.8.7.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.1.30.", "%Y.%m.%d."), datetime.datetime.strptime("2022.3.2.", "%Y.%m.%d."), alpha=0.5, color='gray')
plt.axvspan(datetime.datetime.strptime("2022.6.26.", "%Y.%m.%d."), datetime.datetime.strptime("2022.7.26.", "%Y.%m.%d."), alpha=0.25, color='gray')
plt.axvline(datetime.datetime.strptime("2022.4.25.", "%Y.%m.%d."), color='black', label="거리두기 해제")
plt.xlabel("date")
plt.ylabel("population")
plt.title("코로나 대유행을 표시한 서울역 일반 승하차 인원")
plt.legend()
plt.show()


# extract filename.npy
filelist = os.listdir()
filename = []
for file in filelist:
    if os.path.splitext(file)[1] == '.npy':
        filename.append(file)

# apply free function to all files for ratio_ride & ratio_getoff
result_free = []
for file in filename:
    freefile = np.array(free(file))
    ratio_ride = freefile[0] / freefile[2] * 100
    ratio_getoff = freefile[1] / freefile[3] * 100
    result_free.append([sum(ratio_ride)/len(ratio_ride), sum(ratio_getoff)/len(ratio_getoff), file])
    
# sorting result_free
result_free.sort()
print(result_free)


# percentage of elders by station line
plt.figure(figsize=(10,6))
plt.ticklabel_format(style = 'plain')
lines1 = [2 * element + 0.84 * 1 for element in range(8)]
lines2 = [2 * element + 0.84 * 2 for element in range(8)]
line1, line2, line3, line4, line5, line6, line7, line8 = [], [], [], [], [], [], [], []
for i in range(len(result_free)):
    m = len(result_free) - 1 - i
    num = int(result_free[m][2].split("_")[0])
    if num < 200:
        if line1 == []:
            plt.bar(lines1[0], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[0], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line1.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[0], result_free[m][0], bottom=sum(np.array(line1).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[0], result_free[m][1], bottom=sum(np.array(line1).T[1]), color=plt.get_cmap("plasma")(m))
            line1.append([result_free[m][0], result_free[m][1]])
    elif num < 300:
        if line2 == []:
            plt.bar(lines1[1], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[1], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line2.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[1], result_free[m][0], bottom=sum(np.array(line2).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[1], result_free[m][1], bottom=sum(np.array(line2).T[1]), color=plt.get_cmap("plasma")(m))
            line2.append([result_free[m][0], result_free[m][1]])
    elif num < 400:
        if line3 == []:
            plt.bar(lines1[2], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[2], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line3.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[2], result_free[m][0], bottom=sum(np.array(line3).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[2], result_free[m][1], bottom=sum(np.array(line3).T[1]), color=plt.get_cmap("plasma")(m))
            line3.append([result_free[m][0], result_free[m][1]])
    elif num < 500:
        if line4 == []:
            plt.bar(lines1[3], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[3], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line4.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[3], result_free[m][0], bottom=sum(np.array(line4).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[3], result_free[m][1], bottom=sum(np.array(line4).T[1]), color=plt.get_cmap("plasma")(m))
            line4.append([result_free[m][0], result_free[m][1]])
    elif num < 2600:
        if line5 == []:
            plt.bar(lines1[4], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[4], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line5.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[4], result_free[m][0], bottom=sum(np.array(line5).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[4], result_free[m][1], bottom=sum(np.array(line5).T[1]), color=plt.get_cmap("plasma")(m))
            line5.append([result_free[m][0], result_free[m][1]])
    elif num < 2700:
        if line6 == []:
            plt.bar(lines1[5], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[5], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line6.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[5], result_free[m][0], bottom=sum(np.array(line6).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[5], result_free[m][1], bottom=sum(np.array(line6).T[1]), color=plt.get_cmap("plasma")(m))
            line6.append([result_free[m][0], result_free[m][1]])
    elif num < 2800:
        if line7 == []:
            plt.bar(lines1[6], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[6], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line7.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[6], result_free[m][0], bottom=sum(np.array(line7).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[6], result_free[m][1], bottom=sum(np.array(line7).T[1]), color=plt.get_cmap("plasma")(m))
            line7.append([result_free[m][0], result_free[m][1]])
    else:
        if line8 == []:
            plt.bar(lines1[7], result_free[m][0], color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[7], result_free[m][1], color=plt.get_cmap("plasma")(m))
            line8.append([result_free[m][0], result_free[m][1]])
        else:
            plt.bar(lines1[7], result_free[m][0], bottom=sum(np.array(line8).T[0]), color=plt.get_cmap("plasma")(m))
            plt.bar(lines2[7], result_free[m][1], bottom=sum(np.array(line8).T[1]), color=plt.get_cmap("plasma")(m))
            line8.append([result_free[m][0], result_free[m][1]])
plt.xticks([2 * element + 0.84 * 1.5 for element in range(8)], ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선'])
plt.title("elders ratio by station line")
plt.show()


# best 10 elders stations
print(result_free[-11:])

# around the station & inside th station
try:
    outside = np.genfromtxt("./서울교통공사 지하철 주변 주요시설 정보.csv", dtype="<U10", delimiter=",")[0]
    print(outside)
except:
    print("Error: ',' in csv data")

convert = lambda x: float(x.strip(b'""'))
converters={2: convert, 3: convert, 4: convert}
name = np.genfromtxt("./서울시 지하철 역사 노약자 장애인 편의시설 현황.csv", dtype="<U30", delimiter=",")[0]
dtype = []
for i in range(5):
    if i < 2:
        dtype.append((name[i].strip('"'), '<U30'))
    else:
        dtype.append((name[i].strip('"'), '<i8'))
inside1 = np.genfromtxt("./서울시 지하철 역사 노약자 장애인 편의시설 현황.csv", skip_header=True, converters=converters, dtype=dtype, delimiter=",")
for i in range(len(inside1)):
    inside1['호선'][i] = inside1['호선'][i].strip('""')
    inside1['역명'][i] = inside1['역명'][i].strip('""')
print(inside1.dtype)
    
name = np.genfromtxt("./서울시 지하철 역사 편의시설 현황.csv", dtype="<U30", delimiter=",")[0]
dtype = []
for i in range(13):
    dtype.append((name[i].strip('"'), '<U10'))
print(dtype)
inside2 = np.genfromtxt("./서울시 지하철 역사 편의시설 현황.csv", skip_header=True, filling_values=0, dtype=dtype, delimiter=",")
for i in range(len(inside2)):
    for j in range(len(inside2[0])):
        inside2[i][j] = inside2[i][j].strip('""')
        

# avg number
ev = sum(inside1['엘리베이터EV']) / len(inside1)
es = sum(inside1['에스컬레이터ES']) / len(inside1)
wl = sum(inside1['휠체어리프트WL']) / len(inside1)

# 10 stations
ten1 = []
for i in range(len(result_free[-11:])):
    station_name = result_free[-11:][i][2].split("_")[2][:-4]
    station_line = result_free[-11:][i][2].split("_")[1][0]
    if "(" in station_name:
        station_name = station_name[:station_name.index("(")]
    station_name2 = station_name + "(" + station_line + ")"
    in1_1 = inside1[inside1['역명'] == station_name]
    in1_2 = inside1[inside1['역명'] == station_name2]
    in1 = np.append(in1_1, in1_2)
    print(in1)
    ten1.append(list(in1[0]))
print([ev, es, wl])

# plot
plt.figure(figsize=(5,5))
for i in range(len(ten1)):
    plt.plot([0,1,2], ten1[i][2:], label=f"{ten1[i][1]}")
plt.plot([0,1,2], [ev, es, wl], 'k-', label="averge number")
plt.xticks([0,1,2], ['E/V', 'E/S', 'W/L'])
plt.title("facility for best 10 elders stations")
plt.legend()
plt.show()


# percent of yes
p0 = len(inside2[inside2['엘리베이터유무'] == "Y"]) / len(inside2)
p1 = len(inside2[inside2['휘체어리프트유무'] == "Y"]) / len(inside2)
p2 = len(inside2[inside2['환승주차자유무'] == "Y"]) / len(inside2)
p3 = len(inside2[inside2['자전거보관소유무'] == "Y"]) / len(inside2)
p4 = len(inside2[inside2['무인민원발급기유무'] == "Y"]) / len(inside2)
p5 = len(inside2[inside2['환전키오스크유무'] == "Y"]) / len(inside2)
p6 = len(inside2[inside2['기차예매역유무'] == "Y"]) / len(inside2)
p7 = len(inside2[inside2['문화공간유무'] == "Y"]) / len(inside2)
p8 = len(inside2[inside2['만남의장소유무'] == "Y"]) / len(inside2)
p9 = len(inside2[inside2['유아수유방유무'] == "Y"]) / len(inside2)

# 10 stations
ten2 = []
for i in range(len(result_free[-11:])):
    station_id = result_free[-11:][i][2].split("_")[0]
    if len(station_id) == 3:
        station_id = '0' + station_id
    in2 = inside2[inside2['지하철역ID'] == station_id]
    ten2.append(list(in2[0])[3:])
    print(list(in2[0])[3:])

for i in range(len(ten2[0])):
    globals()['p2{}'.format(i)] = ten2[:][i].count("Y")
print([p20, p21, p22, p23, p24, p25, p26, p27, p28, p29])
print([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9])

# plot
plt.figure(figsize=(8,8))
plt.plot(range(10), [p20, p21, p22, p23, p24, p25, p26, p27, p28, p29])
plt.plot(range(10), [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9], 'k-', label="averge percent")
xnames = []
for i in range(3,13):
    xnames.append(name[i].strip('"')[:-2])
plt.xticks(range(10), xnames, size=7)
plt.title("facility % for best 10 elders stations")
plt.legend()
plt.show()

# end program
print("End Program...")
