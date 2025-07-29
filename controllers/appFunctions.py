import math

def SetPrice(PredefinedPrice,ParkedTimeStamp,LeavingTimeStamp):
    duration=LeavingTimeStamp-ParkedTimeStamp
    total_hrs=math.ceil(duration.total_seconds()/3600)
    return 50+(PredefinedPrice*total_hrs)