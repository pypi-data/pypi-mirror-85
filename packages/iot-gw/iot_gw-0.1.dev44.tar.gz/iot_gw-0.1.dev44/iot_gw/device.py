import datetime
import os
import enum
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import jwt

class DeviceStatus(enum.Enum):
    UNKNOWN = 0
    REGISTERED = 1
    ATTACHED = 2


class Device:
    def __init__(self,device_id,key_folder=None):
        self.device_id = device_id
        self.status = DeviceStatus.UNKNOWN
        if not self.__key_pair_is_available(key_folder):
            self.__generate_key_pair()
        else:
            self.fetch(key_folder)

    def toJson(self):
        return {
            "device_id" : self.device_id,
            "public_key" : self.__public_key.decode('utf-8')
        }

    def get_public_key(self):
        return self.__public_key

    def get_private_key(self):
        return self.__private_key

    def dump(self, path):
        self.__dump(
            self.get_private_key(),
            self.__build_private_key_path(path)
        )
        self.__dump(
            self.get_public_key(),
            self.__build_public_key_path(path)
        )

    def fetch(self, path):
        with open(self.__build_private_key_path(path),'rb') as private_key_file:
            self.__private_key = crypto_serialization.load_pem_private_key(
                private_key_file.read(),
                password=None,
                backend=crypto_default_backend()
            ).private_bytes(
                crypto_serialization.Encoding.PEM,
                crypto_serialization.PrivateFormat.PKCS8,
                crypto_serialization.NoEncryption()
            )
        with open(self.__build_public_key_path(path),'rb') as public_key_file:
            self.__public_key = crypto_serialization.load_pem_public_key(
                public_key_file.read(),
                backend=crypto_default_backend()
            ).public_bytes(
                crypto_serialization.Encoding.PEM,
                crypto_serialization.PublicFormat.PKCS1
            ) 
        
    def __generate_key_pair(self):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        self.__public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.PKCS1
        )
        self.__private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

    def __build_private_key_path(self,path):
        return os.path.join(path,'{}_private.pem'.format(self.device_id))

    def __build_public_key_path(self,path):
        return os.path.join(path,'{}_public.pem'.format(self.device_id))
        
    def __dump(self,data,file):
        with open(file,'wb') as output:
            output.write(data)
    
    def __key_pair_is_available(self,path):
        if path is None:
            return False
        else:
            public_key_path = self.__build_public_key_path(path)
            private_key_path = self.__build_private_key_path(path)
            return os.path.isfile(self.__build_public_key_path(path)) and os.path.isfile(private_key_path)


class DeviceManager:

    def __init__(self,config):
        self.__key_pair_path = config['key_pair_path']

    def get_device(self,device_id):
        return Device(device_id,self.__key_pair_path)


    