import sqlite3
import Calculate



def Comparison(Test_Lowest,Test_Avg_Low,Test_Average,Test_Avg_High,Test_Highest):
    conn = sqlite3.connect('MusicDay.db')  #建立資料庫
    c = conn.cursor()
    
    Multilist = [[0]*2]
    a = Test_Lowest
    b = Test_Avg_Low
    c = Test_Average
    d = Test_Avg_High
    e = Test_Highest
     
    for i in range(0,1000,1): ##for testing 後面改成(0,1000,1)
        sql_fetch = f"select * from music where ID={i}"
        c.execute(sql_fetch)
        Data_from_music = c.fetchone()
        
        Song_Lowest = Data_from_music[7]
        Song_Avg_Low = Data_from_music[8]
        Song_Average = Data_from_music[9]
        Song_Avg_High = Data_from_music[10]
        Song_Highest = Data_from_music[11]
        
        
        if Calculate.Judge(e,a,Song_Highest,Song_Lowest) == 0:
            continue
        if i == 1000:
            Multilist[i][0] = Data_from_music[0]
            Multilist[i][1] = Calculate.Distance(a,b,c,d,e,Song_Lowest,Song_Avg_Low,Song_Average,Song_Avg_High,Song_Highest)
        else:
            Multilist.append([Data_from_music[0],Calculate.Distance(a,b,c,d,e,Song_Lowest,Song_Avg_Low,Song_Average,Song_Avg_High,Song_Highest)])
            
    Multilist.sort(key = lambda s:s[1])

    Return_Val = [[0]*5]
    for i in range(0,5,1):  ##測試，到時改成0,5,1就是最小的五筆資料
        sql_fetch = f"select * from music where ID={Multilist[i][0]}"
        c.execute(sql_fetch)
        Data = c.fetchone()
        Return_Val[i] = dict([('Name', f'{Data[1]}'), ('Artist', f'{Data[2]}'), ('Album', f'{Data[3]}'), ('URL', f'{Data[6]}')])

    conn.close ##close the file
    return Return_Val