import unittest
import os
import iot_gw.gateway as gw

dir_path = os.path.dirname(os.path.realpath(__file__))

class GatewayTest(unittest.TestCase):

    def test_load_default_config(self):
        default_config = {
            'storage':{
                'key_pair_path' : './tests/data'
            },
            'bridge':{
                'adapter': 'gcp',
                'project_id': 'iot-dev-260617',
                'region': 'europe-west1',
                'registry_id': 'mylab',
                'device_id': 'gw-dev',
                'private_key_file': './tests/data/gw_private.pem',
                'ca_certs_file': './tests/data/mqtt.googleapis.com.pem',
                'bridge_hostname': 'mqtt.googleapis.com',
                'bridge_port': 443
            },
            'server':{
                'http':{
                    'host':'0.0.0.0',
                    'port':'8080'
                }
            }
        }
        # when config_path is undefined, use default config
        config = gw._load_config(config_path = None, default_config=default_config)
        self.assertEquals(default_config,config)
        # when file is not found, use default config
        config = gw._load_config(config_path="/wrong/path.yml",default_config=default_config)
        self.assertEquals(default_config,config)

    def test_load_config(self):
        config = gw._load_config(config_path=os.path.join(dir_path,"data/configuration.yml"),default_config=None)
        self.assertIsNotNone(config)
        self.assertTrue('storage' in config)

        

