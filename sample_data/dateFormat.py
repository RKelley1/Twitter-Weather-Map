import datetime


now = datetime.datetime.now()
currentDate = now.strftime("%Y-%m-%d %H:%M")
print(now.strftime("%Y-%m-%d %H:%M"))



print('http://localhost:8000/get-tweet?fromDate='+ currentDate + ':00')
