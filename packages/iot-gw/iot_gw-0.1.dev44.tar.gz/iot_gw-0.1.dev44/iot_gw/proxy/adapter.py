class ProxyAdapter:

    """
    Proxy Adapter interface
    """

    def __init__(self,id,adapter):
        self.__adapter_id=id
        self.__adapter=adapter

    def start(self):
        """
        Start proxy

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method connect for proxy adapter: %s" % self.__adapter_id)

    def is_ready(self):
        """
        Get proxy status

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method is_ready for proxy adapter: %s" % self.__adapter_id)

    def commands(self,device_id,commands):
        """
        Send commands message to a device

        Parameters
        ----------
        device_id: str
            Device identifiant

        commands: str
            commands message

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method commands for proxy adapter: %s" % self.__adapter_id)

    def config(self,device_id,configuration):
        """
        Send configuration message

        Parameters
        ----------
        device_id: str
            Device identifiant

        configuration: str
            configuration message

        Returns
        -------
            True or False
        """
        raise NotImplementedError("Not implemented method config for proxy adapter: %s" % self.__adapter_id)


    def attach_handler(self,device_id):
        self.__adapter.attach(device_id)

    def unattach_handler(self,device_id):
        self.__adapter.unattach(device_id)
        
    def event_handler(self,device_id,event):
        self.__adapter.publish_event(event,device_id)
        
    def state_handler(self,device_id,event):
        self.__adapter.publish_state(event,device_id)

