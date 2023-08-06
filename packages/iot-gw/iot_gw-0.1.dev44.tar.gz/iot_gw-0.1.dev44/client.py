import time
import logging
from iot_gw.proxy.mqtt import MqttProxy


logging.basicConfig(level=logging.DEBUG)
proxy=MqttProxy('test','gateway','P@ssw0rd','./tests/data/ca.crt',
    on_attach=lambda d:print("on_attach {}".format(d)),
    on_unattach=lambda d:print("on_unattach {}".format(d)),
    on_event=lambda d,p:print("on_event {} / {}".format(d,p)),
    on_state=lambda d,p:print("on_sate {} / {}".format(d,p))
)
is_connected=proxy.connect(hostname='192.168.99.11',port=8883,async_connect=True)
print(is_connected)

while proxy.is_connected():
    time.sleep(1)