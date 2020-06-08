from upnpy.ssdp.SSDPRequest import SSDPRequest
from upnpy import exceptions
import upnpy.utils as utils


class UPnP:

    """
        **UPnP object**

        A UPnP object used for device discovery
    """

    def __init__(self):
        self.ssdp = SSDPRequest()
        self.discovered_devices = []

    def discover(self, delay=2, **headers):

        """
            **Find UPnP devices on the network**

            Find available UPnP devices on the network by sending an M-SEARCH request.

            :param delay: Discovery delay, amount of time in seconds to wait for a reply from devices
            :type delay: int
            :param headers: Optional headers for the request
            :return: List of discovered devices
            :rtype: list
        """

        discovered_devices = []
        for device in self.ssdp.m_search(discover_delay=delay, st='upnp:rootdevice', **headers):
            discovered_devices.append(device)

        self.discovered_devices = discovered_devices
        return self.discovered_devices

    def get_igd(self):

        """
            **Get the Internet Gateway Device if available**

            Gets the Internet Gateway device if it's available after discovery.

            :return: The IGD if successful or raises a upnpy.exceptions.IGDError exception upon failure
            :rtype: SSDPDevice
        """

        ig_devices = []

        for device in self.discovered_devices:
            device_type = utils.parse_device_type(device.type_)
            if device_type == 'InternetGatewayDevice':
                ig_devices.append(device)

        if len(ig_devices) == 1:
            return ig_devices[0]
        elif len(ig_devices) > 1:
            raise exceptions.IGDError('Multiple IGDs found. Specify one manually.')
        else:
            raise exceptions.IGDError('No IGD found.')
