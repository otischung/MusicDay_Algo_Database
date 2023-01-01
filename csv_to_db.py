import pandas as pd
import os
import sqlite3

csv_file = "./label - 手改.csv"
table = pd.read_csv(csv_file)
conn = sqlite3.connect('MusicDay.db')  #建立資料庫
cursor = conn.cursor()
cursor.execute('CREATE TABLE music(title, Artist, Album, File_Path, Cover_Path, First_Comment, Lowest_Pitch, First_Quartile_Pitch, Medium_Pitch, Third_Quartile_Pitch, Highest_Pitch)')  #建立資料表
conn.commit()
table.to_sql('music', conn, if_exists='append', index=False)  #將csv資料加入
