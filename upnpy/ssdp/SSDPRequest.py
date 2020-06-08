import socket
from upnpy.ssdp.SSDPHeader import SSDPHeader
from upnpy.ssdp.SSDPDevice import SSDPDevice


class SSDPRequest(SSDPHeader):

    """
        **Create and perform an SSDP request**

        :param method: SSDP request method [M-SEARCH or NOTIFY]
    """

    def __init__(self, ssdp_mcast_addr='239.255.255.250', ssdp_port=1900, **headers):
        super().__init__(**headers)

        self.SSDP_MCAST_ADDR = ssdp_mcast_addr
        self.SSDP_PORT = ssdp_port

        self.set_header('HOST', f'{self.SSDP_MCAST_ADDR}:{self.SSDP_PORT}')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def m_search(self, discover_delay=2, st='ssdp:all', **headers):

        """
            **Perform an M-SEARCH SSDP request**

            Send an SSDP M-SEARCH request for finding UPnP devices on the network.

            :param discover_delay: Device discovery delay in seconds
            :type discover_delay: int
            :param st: Specify device Search Target
            :type st: str
            :param headers: Specify M-SEARCH specific headers
            :type headers: str
            :return: List of device that replied
            :rtype: list
        """

        self.set_method('M-SEARCH')

        self.set_header('MAN', '"ssdp:discover"')
        self.set_header('MX', discover_delay)
        self.set_header('ST', st)
        self.set_headers(**headers)

        self.socket.settimeout(discover_delay)
        devices = self._send_request(self._get_raw_request())


        for device in devices:
            yield device

    def notify(self, **headers):

        """
        Perform a NOTIFY SSDP request

        :param headers: Specify NOTIFY specific headers
        :return:
        """
        self.set_method('NOTIFY')
        self.set_headers(**headers)

    def _get_raw_request(self):

        """
        Get raw request data to send to server
        """

        final_request_data = ''

        if self.method is not None:
            ssdp_start_line = f'{self.method} * HTTP/1.1'
        else:
            ssdp_start_line = 'HTTP/1.1 200 OK'

        final_request_data += f'{ssdp_start_line}\r\n'

        for header, value in self.headers.items():
            final_request_data += f'{header}: {value}\r\n'

        final_request_data += '\r\n'

        return final_request_data

    def _send_request(self, message):
        self.socket.sendto(message.encode(), (self.SSDP_MCAST_ADDR, self.SSDP_PORT))

        devices = []

        try:
            while True:

                # UDP packet data limit is 65507 imposed by IPv4
                # https://en.wikipedia.org/wiki/User_Datagram_Protocol#Packet_structure

                response, addr = self.socket.recvfrom(65507)
                device = SSDPDevice(addr, response.decode())
                devices.append(device)
        except socket.timeout:
            pass

        return devices
