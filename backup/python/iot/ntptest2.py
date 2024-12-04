import os
import ntplib
from time import ctime
print "================aaaa===================="
try:
    client = ntplib.NTPClient()
    response = client.request('europe.pool.ntp.org', version=3)
    print "===================================="
    print "Offset : "+str(response.offset)
    print "Version : "+str(response.version)
    print "Date Time : "+str(ctime(response.tx_time))
    print "Leap : "+str(ntplib.leap_to_text(response.leap))
    print "Root Delay : "+str(response.root_delay)
    print "Ref Id : "+str(ntplib.ref_id_to_text(response.ref_id))
    print  str(ctime(response.tx_time))
    os.system("sudo date -s '"+str(ctime(response.tx_time))+"'")
    print "===================================="
except:
    os.system("sudo date")
    print "NTP Server Down Date Time NOT Set At The Startup"
    pass
