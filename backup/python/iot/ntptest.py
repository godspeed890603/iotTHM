import ntplib
from time import ctime
c = ntplib.NTPClient()
response = c.request('europe.pool.ntp.org', version=3)
print(response.offset)
response.version
print(ctime(response.tx_time))
ntplib.leap_to_text(response.leap)
response.root_delay
ntplib.ref_id_to_text(response.ref_id)
