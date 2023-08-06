import unittest
import jwt
import logging
from iot_gw.bridge.gcp import create_jwt_token, create_mqtt_client, MqttBridge
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
gw_private_key = os.path.join(dir_path,'data/gw_private.pem')
gw_public_key = os.path.join(dir_path,'data/gw_public.pem')
ca_certs = os.path.join(dir_path, 'data/mqtt.googleapis.com.pem')

mqtt_bridge_config={
    'project_id': 'iot-dev-260617',
    'region': 'europe-west1',
    'registry_id': 'mylab',
    'device_id': 'gw-dev',
    'private_key_file': gw_private_key,
    'ca_certs_file': ca_certs,
    'bridge_hostname': 'mqtt.googleapis.com',
    'bridge_port': 443
}

class TestGcpBridge(unittest.TestCase):
    
    # def setUp(self):
    #     logging.basicConfig(level=logging.DEBUG)
        
    def test_create_jwt_token(self):
        token=create_jwt_token('project_id',gw_private_key)
        self.assertIsNotNone(token)
        with open(gw_public_key, 'r') as f:
            public_key = f.read()  
        decodedToken=jwt.decode(token,public_key,algorithms='RS256',options={'verify_aud': False})
        self.assertEqual(decodedToken['aud'],'project_id')
        self.assertEqual(decodedToken['exp'] - decodedToken['iat'], 3600)

    def test_create_mqtt_client(self):
        client=create_mqtt_client(
            'project_id',
            'europe-west-1',
            'registry_id',
            'device_id',
            gw_private_key,
            ca_certs)
        self.assertIsNotNone(client)

    def test_connect_mqtt_bridge(self):
        bridge = MqttBridge(None,mqtt_bridge_config)
        try:
            bridge.connect()
        except RuntimeError:
            self.fail()
        self.assertTrue(bridge.is_connected())



if __name__ == '__main__':
    unittest.main()