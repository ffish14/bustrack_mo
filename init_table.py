import sqlite3
import requests
import re



con = sqlite3.connect('bustrack.db')
c = con.cursor()
c.execute('CREATE TABLE BUS_0 (time,staCode,staName,busPlate,status)')
c.execute('CREATE TABLE BUS_1 (time,staCode,staName,busPlate,status)')

# url0 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=sd&routeName=51A&dir=0&lang=zh-tw'
# url1 = 'https://bis.dsat.gov.mo:37812/macauweb/getRouteData.html?action=sd&routeName=51A&dir=1&lang=zh-tw'
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
#     'cookie':'macauweb_huid:37812=a85e72b0-b92d-43d2-8d4f-d4f044eeb3d3'
# }

# def get_staName(url):
#     response = requests.get(url, headers=headers)
#     r = response.text
#     staName_regex = r'staCode":"(.*?)","staName":"(.*?)"'
#     staName = re.findall(staName_regex, r)
#     staName = list(map(lambda i: i[0] + '-' + i[1], staName))
#     response.close()
#     return staName
#
# def ins_staName(c,tableName,staName):
#     for i in range(len(staName)-1):
#         c.execute('INSERT INTO "%s" (station_name) VALUES ("%s")' % (tableName,staName[i]))
#
#
# staName0 = get_staName(url0)
# staName1 = get_staName(url1)
# ins_staName(c,'BUS_0',staName0)
# ins_staName(c,'BUS_1',staName1)

con.commit()
con.close()





