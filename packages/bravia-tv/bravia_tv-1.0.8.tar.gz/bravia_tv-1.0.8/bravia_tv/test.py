from braviarc import BraviaRC
import json
import time
tv_data = None
with open('/home/dave/.homeassistant/.storage/core.config_entries','r') as fh:
    data = json.loads(fh.read()).get('data',{})
    entries = data.get('entries',[])
    for entry in entries:
        if 'XBR-65X900B' == entry.get('title'):
            tv_data = entry.get('data')
    if tv_data:
        tv = tv_data['host'],tv_data['mac']
        # print(tv)


a = BraviaRC(tv_data['host'], tv_data['mac'],'255.255.255.0')

a.connect("6931","deleteMe","delete_me")
#a.turn_on()
print(a.get_playing_info())
a.get_webappstatus()
# tempcookies = a._cookies
# print(a.is_connected())
# a.media_play()
# print(a._cookies)
# a.connect("6931","deleteMe","delete_me")
# a._cookies = tempcookies
# print(a.is_connected())
# a.media_play()
# st=time.time()
# a.turn_on()
# # print("on to on", a.get_power_status(),time.time()-st)
# a.turn_off()
# # print("on -> standby", a.get_power_status())
# # st=time.time()
# # a.turn_on()
# # print("standby -> on", a.get_power_status(),time.time()-st)
# # a.turn_off()
# # print("on -> off", a.get_power_status())
# time.sleep(40)
# # st=time.time()
# # print("time to get off status",a.get_power_status(),time.time()-st)
# # st=time.time()
# a.turn_on()
# print("off -> on",a.get_power_status(),time.time()-st)

# print(a.is_connected())
# print(a._cookies)
# temp=a._cookies
#print("media_play", a.media_play())
# a.connect("6516","deleteMe","delete_me")
# print(a._cookies)
# a._cookies=temp
# print(a.is_connected())
# print("media_play", a.media_play())


# a.turn_on()

# #a.turn_off()
# print(a.get_power_status())
# a._cookies=None
# print(a.is_connected())