import sqlite3
import Calculate

Multilist = [[0] * 2]
conn = sqlite3.connect('MusicDay.db')  # 建立資料庫
c = conn.cursor()

for i in range(1000, 1003, 1):  # for testing 後面改成(0,1000,1)
    sql_fetch = f"select * from music where ID={i}"
    c.execute(sql_fetch)
    Data_from_music = c.fetchone()

    Song_Lowest = Data_from_music[7]
    Song_Avg_Low = Data_from_music[8]
    Song_Average = Data_from_music[9]
    Song_Avg_High = Data_from_music[10]
    Song_Highest = Data_from_music[11]

    if Calculate.Judge(170, 5, Song_Highest, Song_Lowest) == 0:
        continue
    if i == 1000:
        Multilist[i - 1000][0] = Data_from_music[0]
        Multilist[i - 1000][1] = Calculate.Distance(9, 17, 26, 73, 101, Song_Lowest, Song_Avg_Low, Song_Average, Song_Avg_High, Song_Highest)
    else:
        Multilist.append([Data_from_music[0], Calculate.Distance(9, 17, 26, 73, 101, Song_Lowest, Song_Avg_Low, Song_Average, Song_Avg_High, Song_Highest)])

Multilist.sort(key=lambda s: s[1])
for i in range(0, 3, 1):  # 測試，到時改成0,5,1就是最小的五筆資料
    print(Multilist[i])

conn.close  # close the file
