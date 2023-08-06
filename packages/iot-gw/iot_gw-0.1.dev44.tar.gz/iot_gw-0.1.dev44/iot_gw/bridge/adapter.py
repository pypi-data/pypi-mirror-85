class BridgeAdapter:
    """
        Bridge Adapter interface
    """

    def __init__(self,adapter,device_manager):
        self.__adapter=adapter
        self.__device_manager=device_manager

    def get_adapter(self):
        return self.__adapter

    def get_device_manager(self):
        return self.__device_manager

    def connect(self):
        """
        Establish connection to the bridge

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method connect for bridge adapter: %s" % self.get_adapter())

    def attach(self,device_id):
        """
        Attach a device to the gateway

        Parameters
        ----------
        device_id : str 
            device identifiant

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method attach for bridge adapter: %s" % self.get_adapter())

    def unattach(self,device_id):
        """
        Unattach a device from the gateway

        Parameters
        ----------
        device_id : str
            device identifiant

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method unattach for bridge adapter: %s" % self._adapter)

    def publish_event(self,payload,device_id,qos):
        """
        Publish an event message to bridge from a device

        Parameters
        ----------
        payload : str
            message payload
        device_id: str
            device identifiant
        qos: int, optional
            quality of service. 

        Returns
        -------
            True if message is published
            False if message is not published
        """
        raise NotImplementedError("Not implemented method publish_event for bridge adapter: %s" % self._adapter)

    def publish_state(self,payload,device_id,qos):
        """
        Publish a state message to bridge from a device

        Parameters
        ----------
        payload : str
            message payload
        device_id: str
            device identifiant
        qos: int, optional
            quality of service. 

        Returns
        -------
            True if message is published
            False if message is not published
        """
        raise NotImplementedError("Not implemented method publish_state for bridge adapter: %s" % self._adapter)

    def is_connected(self):
        """
        Get connection status

        Returns
        -------
            True if connection is established
            False if connection is not established
        """
        raise NotImplementedError("Not implemented method is_connected for bridge adapter: %s" % self._adapter)
