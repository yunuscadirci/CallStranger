class SSDPHeader:
    def __init__(self, **headers):

        """
        Example M-SEARCH header:

        ----------------------------------------------------------------------------------
        M-SEARCH * HTTP/1.1             SSDP method for search requests
        HOST: 239.255.255.250:1900      SSDP multicast address and port (REQUIRED)
        MAN: "ssdp:discover"            HTTP Extension Framework scope (REQUIRED)
        MX: 2                           Maximum wait time in seconds (REQUIRED)
        ST: upnp:rootdevice             Search target (REQUIRED)

        ----------------------------------------------------------------------------------
        """

        self.headers = {}
        self.set_headers(**headers)

        self._available_methods = ['M-SEARCH', 'NOTIFY']

        self.method = None
        self.host = self.headers.get('HOST')
        self.man = self.headers.get('MAN')
        self.mx = self.headers.get('MX')
        self.st = self.headers.get('ST')

    def _check_method_required_params(self):
        if self.method == 'M-SEARCH':
            # M-SEARCH required parameters: HOST, MAN, MX, ST
            if None in [self.host, self.man, self.mx, self.st]:
                raise ValueError('M-SEARCH method requires HOST, MAN, MX and ST headers to be set.')
        elif self.method == 'NOTIFY':
            pass

    def set_method(self, method):
        method = method.upper()
        if method in self._available_methods:
            self.method = method.upper()
        else:
            raise ValueError('Method must be either' + ' or '.join(self._available_methods))

    def set_header(self, name, value):
        self.headers[name.upper()] = value

    def set_headers(self, **headers):
        for key, value in headers.items():
            self.set_header(key.upper(), value)
