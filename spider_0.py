import requests
import re
import pandas as pd
import sqlite3
import datetime
from time import sleep

url0_0 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=dy&routeName=51A&dir=0&lang=zh-tw'
url1_0 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=dy&routeName=51A&dir=1&lang=zh-tw'
url0_1 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=sd&routeName=51A&dir=0&lang=zh-tw'
url1_1 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=sd&routeName=51A&dir=1&lang=zh-tw'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"

}


def get_url(url):
    response = requests.get(url, headers=headers)
    r = response.text
    return r


def get_staName(r):
    staName_regex = r'"staName":"(.*?)"'
    staName = re.findall(staName_regex, r)
    return staName


def get_stacode(r):
    station_regex = r'"staCode":"(\w\d.*?)"'
    sta_code = re.findall(station_regex, r)
    return sta_code


def get_businfo(r):
    bus_regex = r'"staCode":"(.*?)"'
    bus_1 = r'"busInfo":\[(.*?)\]'
    bus_2 = r'"busPlate":"(.*?)"'
    bus_3 = r'"status":"(.*?)"'
    bus_info = re.findall(bus_regex, r)
    bus_info1 = re.findall(bus_1, r)
    kk = 0
    for k in bus_info1:
        if k:
            busPlate = re.findall(bus_2, k)
            status = re.findall(bus_3, k)
            for i in range(len(busPlate)):
                cc = [bus_info[kk], busPlate[i], status[i]]
                bb.append(cc)
        kk = kk + 1
    print(bb)
    return bb


def match_staCode(stacode, businfo, staName):
    t = datetime.datetime.now().replace(microsecond=0)
    df_columns = ['staCode', 'staName', 'busPlate', 'status', 'time']
    df = pd.DataFrame(columns=df_columns)
    df['staCode'] = stacode
    df['staName'] = staName

    for i in range(len(businfo)):
        scode = businfo[i][0]
        bplate = businfo[i][1]
        status = businfo[i][2]
        sindex = df[df['staCode'] == scode].index

        if businfo[i][0] == businfo[i - 1][0]:
            a = [[scode], ['staName'], [bplate], [status], ['time']]
            df1 = pd.DataFrame(columns=df_columns)
            df1['staCode'] = a[0]
            df1['busPlate'] = a[2]
            df1['status'] = a[3]
            df1['staName'] = df.iloc[sindex[0], 1]
            if df1 is not None:
                above = df.iloc[0:sindex[0]+1]
                below = df.iloc[sindex[0]+1:]
                df = pd.concat([above, df1, below], ignore_index=True)

        else:
            df.iloc[sindex, 2] = bplate
            df.iloc[sindex, 3] = status

    df.loc[:, 'time'] = t
    df.index = df.time
    df = df.drop(columns='time')
    df.mask(df.isna(), other=-1, inplace=True)
    return df


def insert_df(df, table):
    conn = sqlite3.connect('bustrack.db')
    df.to_sql(table, conn, if_exists='append')
    conn.commit()
    conn.close()


while True:

    r_0_0 = get_url(url0_0)
    r_1_0 = get_url(url1_0)
    r_0_1 = get_url(url0_1)
    r_1_1 = get_url(url1_1)
    sta_code_0 = get_stacode(r_0_0)
    sta_code_1 = get_stacode(r_1_0)
    bb = []
    bus_info_0 = get_businfo(r_0_0)
    bb = []
    bus_info_1 = get_businfo(r_1_0)
    sta_Name_0 = get_staName(r_0_1)
    sta_Name_1 = get_staName(r_1_1)

    df_0 = match_staCode(sta_code_0, bus_info_0, sta_Name_0)
    df_1 = match_staCode(sta_code_1, bus_info_1, sta_Name_1)

    print(df_0)
    print()
    print(df_1)

    insert_df(df_0, 'BUS_0')
    insert_df(df_1, 'BUS_1')

    t = datetime.datetime.now().time()
    t0 = datetime.time(17, 0)
    t1 = datetime.time(22, 30)
    t2 = datetime.time(6, 0)

    if t0 < t < t1:
        sleep(5)
    elif t < t2:
        print('out of service')
        break
    else:
        sleep(10)
