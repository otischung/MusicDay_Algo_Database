def Judge(Tester_Highest,Tester_Lowest,Song_Highest,Song_Lowest):
    if Song_Lowest < Tester_Lowest or Song_Highest > Tester_Highest:
        return 0  ##判斷歌曲最高/低音是否超過Tester的音域，是return 0,or return 1
    else:
        return 1
    
    
def Distance(Tester_Lowest,Tester_Avg_Low,Tester_Average,Tester_Avg_High,Tester_Highest,Song_Lowest,Song_Avg_Low,Song_Average,Song_Avg_High,Song_Highest):
    Diff_Highest = abs(Tester_Highest-Song_Highest)  ##計算各項距離
    Diff_Lowest = abs(Tester_Lowest-Song_Lowest)
    Diff_Avg_High = abs(Tester_Avg_High-Song_Avg_High)
    Diff_Avg_Low = abs(Tester_Avg_Low-Song_Avg_Low)
    Diff_Average = abs(Tester_Average-Song_Average)
    
    return Diff_Highest+Diff_Lowest+Diff_Avg_High+Diff_Avg_Low+Diff_Average
    ##看看要不要用別的方式比較，我只是先打個雛形