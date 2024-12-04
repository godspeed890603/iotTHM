# Return CPU temperature as a character string
import os
def getCPUtemperature():
    #res = os.popen('vcgencmd measure_temp').readline()
    res = os.popen('vcgencmd get_mem arm').readline()
    return(res.replace("temp=","").replace("C\n",""))

temp1=getCPUtemperature()
#temp2= 9.0/5.0*temp1+32
print (temp1,"C")#, "\n",  temp2,"F")
