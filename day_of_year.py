from datetime import datetime
def dayOfYear( ):
    date=str(datetime.date(datetime.now()))
    days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    d = list(map(int,date.split("-")))
    if d[0] % 400 == 0:
        days[2]+=1
    elif d[0]%4 == 0 and d[0]%100!=0:
        days[2]+=1
    for i in range(1,len(days)):
        days[i]+=days[i-1]
    return days[d[1]-1]+d[2]