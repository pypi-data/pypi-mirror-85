import unittest
import paho.mqtt.client
from iot_gw.proxy.mqtt import MqttProxy
from mockito import mock, verify, when


mqtt_config={
    'login':'username',
    'password':'password',
    'hostname':'localhost',
    'port': 1886
}

class Message:
    def __init__(self,topic,payload,qos=0):
        self.topic=topic
        self.payload=payload.encode('utf-8')
        self.qos=qos

class MqttProxyTest(unittest.TestCase):

    def test_attach_topic(self):
        mqttMock = mock()
        adapterMock = mock()
        when(paho.mqtt.client).Client(client_id='mqtt_proxy').thenReturn(mqttMock)
        proxy = MqttProxy(mqtt_config,adapterMock)
        message = Message('/attach','device_id')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(adapterMock,times=1).attach('device_id')
        verify(mqttMock,times=1).subscribe('/event/device_id')
        verify(mqttMock,times=1).subscribe('/state/device_id')

    def test_unattach_topic(self):
        adapterMock = mock()
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='mqtt_proxy').thenReturn(mqttMock)
        proxy = MqttProxy(mqtt_config,adapterMock)
        message = Message('/unattach','device_id')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(adapterMock,times=1).unattach('device_id')
        verify(mqttMock,times=1).unsubscribe('/event/device_id')
        verify(mqttMock,times=1).unsubscribe('/state/device_id')

    def test_config(self):
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='mqtt_proxy').thenReturn(mqttMock)
        proxy = MqttProxy(mqtt_config,mock())
        proxy.config('device_id','configuration')
        verify(mqttMock,times=1).publish(
            topic='/config/device_id',
            payload='configuration',
            qos=0
        )
    
    def test_commands(self):
        mqttMock = mock()
        when(paho.mqtt.client).Client(client_id='mqtt_proxy').thenReturn(mqttMock)
        proxy = MqttProxy(mqtt_config,mock())
        proxy.commands('device_id','command')
        verify(mqttMock,times=1).publish(
            topic='/commands/device_id',
            payload='command',
            qos=0
        )

    def test_state_topic(self):
        listenerMock = mock()
        proxy = MqttProxy(mqtt_config,listenerMock)
        message = Message('/state/device_id','state')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).publish_state(b'state','device_id')

    def test_event_topic(self):
        listenerMock = mock()
        proxy = MqttProxy(mqtt_config,listenerMock)
        message = Message('/event/device_id','event')
        proxy.on_message(client='client_id',userdata=None,message=message)
        verify(listenerMock,times=1).publish_event(b'event','device_id')



    
