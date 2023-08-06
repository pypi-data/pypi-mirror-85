import unittest
from iot_gw.bridge import bridge_adapter_factory;


class BridgeFactoryTest(unittest.TestCase):

    def test_gcp_mqtt_bridge(self):
        config = {
                'adapter': 'gcp',
                'project_id': 'iot-dev-260617',
                'region': 'europe-west1',
                'registry_id': 'mylab',
                'device_id': 'gw-dev',
                'private_key_file': './tests/data/gw_private.pem',
                'ca_certs_file': './tests/data/mqtt.googleapis.com.pem',
                'bridge_hostname': 'mqtt.googleapis.com',
                'bridge_port': 443
        }
        adapter = bridge_adapter_factory.create(None,config)
        self.assertIsNotNone(adapter)

    def test_missing_adapter_property(self):
        self.assertRaises(RuntimeError,bridge_adapter_factory.create,None,{})

    def test_unknown_adapter(self):
        self.assertRaises(RuntimeError,bridge_adapter_factory.create,None,{'adapter':'unknown'})    
