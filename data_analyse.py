import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def rdb(tablename):

    conn = sqlite3.connect('bustrack.db')
    df = pd.read_sql_query("SELECT * FROM '{}'".format(tablename),conn,index_col='time',parse_dates=True)
    conn.close()
    df.index = pd.to_datetime(df.index)
    return df

def lfb(dataframe,a):
    stacode = dataframe['staCode'].drop_duplicates()
    busplate = dataframe['busPlate'].drop_duplicates().tolist()
    busplate.remove('-1')
    df_bus = dataframe[dataframe.busPlate==busplate[a]]
    bus_t = pd.DataFrame()
    for i in range(len(stacode)):
        df_bus1 = df_bus[df_bus['staCode']==stacode[i]]
        if i == 0:
            bus_arr = df_bus1.drop_duplicates(keep='last')
        else:
            bus_arr = df_bus1.drop_duplicates(keep='first')
        bus_t = bus_t.append(bus_arr)
    return bus_t

def timeint(dataframe):
    t=[]
    # leave = dataframe[dataframe.status == '0']
    # print(leave)
    # print(leave.index[0])

    stacode = dataframe['staCode'].drop_duplicates().tolist()

    arr = dataframe[dataframe.status == '1']
    arrtime = arr.index
    for i in range(1,len(arrtime)):
        t1 = int((arrtime[i] - arrtime[i-1]).seconds)
        t.append(t1)

    return stacode,t

def timeintpic(staname,t,a):

    staname1 = []
    for i in range(len(staname)-1):
        staname1.append(staname[i]+'-'+staname[i+1])

    data = pd.DataFrame({'staname':staname1,'timegap':t})
    fig,ax = plt.subplots()
    ax = sns.barplot(x='staname',y='timegap',data= data)
    ax.set_xlabel('station to station')
    ax.set_ylabel('timegap (s)')
    ax.set_xticklabels(labels=staname1,fontsize = 'small',rotation= 60)
    plt.title('route:51A-{} time interval at 3pm,2019/11/06'.format(a))
    plt.tight_layout()
    plt.savefig('time_interval_3pm_{}.png'.format(a),dpi = 600)
    plt.show()

def timeduration(dataframe):
    t=[]
    stacode = dataframe['staCode'].drop_duplicates().tolist()

    arr = dataframe[dataframe.status == '1']
    arrtime = arr.index
    for i in range(1,len(arrtime)):
        t1 = int((arrtime[i] - arrtime[0]).seconds)/60
        t1 = round(t1)
        t.append(t1)

    return stacode,t

def timedurplt(stacode,t,a):

    t.insert(0,0)
    data = pd.DataFrame({'stacode':stacode,'timedur':t})
    fig,ax = plt.subplots()
    ax.plot(stacode,t)
    ax.set_xlabel('station')
    ax.set_ylabel('time duration (min)')
    ax.set_xticklabels(labels=stacode,fontsize = 'small',rotation = 90)
    plt.title('route:51A-{} time duration at 3pm,2019/11/06'.format(a))
    plt.tight_layout()
    plt.savefig('time_duration_3pm_{}.png'.format(a),dpi = 600)
    plt.show()

df = rdb('00')
bus_time = lfb(df,0)
stacode, tg = timeint(bus_time)
timeintpic(stacode, tg,0)
stacodedur,td = timeduration(bus_time)
timedurplt(stacodedur,td,0)

df1 = rdb('11')
bus_time1 = lfb(df1,6)
stacode1, tg1 = timeint(bus_time1)
timeintpic(stacode1,tg1,1)
stacodedur1,td1 = timeduration(bus_time1)
timedurplt(stacodedur1,td1,1)







