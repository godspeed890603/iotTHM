import datetime
import time

currentDateTime = datetime.datetime.now()
print(datetime.datetime.now()+datetime.timedelta(minutes=15))

nextReportTime=datetime.datetime.now()+datetime.timedelta(seconds=5)
while(True):
    if(datetime.datetime.now()>nextReportTime):
        nextReportTime=datetime.datetime.now()+datetime.timedelta(seconds=5)
   #subDatetime=datetime.datetime.now()-currentDateTime
    #print(subDatetime)
        print("1")
    #print(datetime.datetime.min)
    #print(datetime.datetime.now()-currentDateTime)
    #print(datetime.datetime.now()-datetime.timedelta(minutes=15))
    
    time.sleep(1)
