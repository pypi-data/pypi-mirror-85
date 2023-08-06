import time
import ssl
import logging
from enum import Enum
import paho
from .adapter import ProxyAdapter

class MqttProxy(ProxyAdapter):
    def __init__(self,config,adapter):
        super().__init__('mqtt',adapter)
        self.__client_id='mqtt_proxy'
        self.__username=config['login']
        self.__password=config['password']
        self.__hostname=config['hostname']
        self.__port=config['port']
        self.__ca_certs_file = config['ca_certs_file'] if 'ca_certs_file' in config else None
        self.__client=paho.mqtt.client.Client(client_id=self.__client_id)
        self.__client.username_pw_set(username=self.__username,password=self.__password)
        if not self.__ca_certs_file is None:
            logging.debug("Enable TLS")
            self.__client.tls_set(self.__ca_certs_file,tls_version= ssl.PROTOCOL_TLSv1_2)
        self.__client.enable_logger(logging)
        self.__client.on_connect=self.__on_connect
        self.__client.on_disconnect=self.__on_disconnect
        self.__client.on_message=self.on_message
        self.__is_connected=False
        self.__topicHandlers={
            'attach' : self.__on_attach_message,
            'unattach' : self.__on_unattach_message,
            'state' : self.__on_state_message,
            'event' : self.__on_event_message
        }
        
    def start(self):
        return self.connect()

    def connect(self,timeout=5,async_connect=True):
        if async_connect:
            self.__client.connect_async(self.__hostname,int(self.__port))
            self.__client.loop_start()
            self.__wait_for_connection(timeout)
        else:
            self.__client.connect(self.__hostname,self.__port)
        return self.is_connected()

    def is_ready(self):
        return self.is_connected()

    def is_connected(self):
        return self.__is_connected

    def config(self,device_id,configuration):
        logging.debug("Config device {}: {}".format(device_id,configuration))
        self.__client.publish(
            topic="/config/{}".format(device_id),
            payload=configuration,
            qos=0)

    def commands(self,device_id,command):
        logging.debug("Commands device {}: {}".format(device_id,command))
        self.__client.publish(
            topic="/commands/{}".format(device_id),
            payload=command,
            qos=0)

    def on_message(self,client,userdata,message):
        payload = str(message.payload.decode('utf-8'))
        logging.debug(
            'Received message \'{}\' on topic \'{}\' with Qos {}'
            .format(payload, message.topic, str(message.qos))
        )
        topics= list(filter(lambda t : len(t) > 0,message.topic.split('/')))
        if topics[0] in self.__topicHandlers:
            self.__topicHandlers[topics[0]](message.payload,topics[1:])
        else:
            logging.warn("MQTT proxy have receiced message on an unknown topic: %s",topics[0])

    def __on_attach_message(self,payload,subtopics):
        device_id=payload.decode('utf-8')
        self.__client.subscribe('/event/{}'.format(device_id))
        self.__client.subscribe('/state/{}'.format(device_id))
        self.attach_handler(device_id)

    def __on_unattach_message(self,payload,subtopics):
        device_id=payload.decode('utf-8')
        self.__client.unsubscribe('/event/{}'.format(device_id))
        self.__client.unsubscribe('/state/{}'.format(device_id))
        self.unattach_handler(device_id)

    def __on_event_message(self,payload,subtopics):
        self.event_handler(subtopics[0],payload)

    def __on_state_message(self,payload,subtopics):
        self.state_handler(subtopics[0],payload)

    def __on_connect(self,client,userdata,flags,rc):
        logging.debug("MQTT client %s connection is up" % self.__client_id)
        self.__client.subscribe('/attach',qos=1)
        self.__client.subscribe('/unattach',qos=1)
        self.__is_connected=True

    def __on_disconnect(self,client,userdate,rc):
        logging.debug("MQTT client %s connection is down" % self.__client_id)
        self.__is_connected=False


    def __wait_for_connection(self, timeout=5):
        total_time = 0
        while not self.__is_connected and total_time < timeout:
            logging.debug("wait_for_connection %d" % timeout)
            if timeout > 0:
                total_time +=1
            time.sleep(1)
        if not self.__is_connected:
            raise RuntimeError('Could not connect to MQTT server.')
        logging.debug("wait_for_connection terminated %s" % self.is_connected)

