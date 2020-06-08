import urllib.request


def parse_device_type(device_type):

    """
        **Parse the the deviceType string**

        Parses only the deviceType portion of the device type string

        :param device_type: Full device type string
        :return: Parsed device type
        :rtype: str
    """

    return device_type.split(':')[3:][0]


def parse_service_id(service_id):

    """
        **Parse the the serviceID string**

        Parses only the serviceID portion of the service ID string

        :param service_id: Full device type string
        :return: Parsed service ID
        :rtype: str
    """

    return service_id.split(':')[3:][0]


def parse_http_header(header, header_key):

    """
        **Parse HTTP header value**

        Parse the value of a specific header from a RAW HTTP response.

        :param header: String containing the RAW HTTP response and headers
        :type header: str
        :param header_key: The header name of which to extract a value from
        :type header_key: str
        :return: The value of the header
        :rtype: str
    """

    split_headers = header.split('\r\n')

    for entry in split_headers:
        header = entry.strip().split(':', 1)

        if header[0].strip().lower() == header_key.strip().lower():
            return ''.join(header[1::]).split()[0]


def make_http_request(url, data=None, headers=None):

    """
        **Helper function for making HTTP requests**

        Helper function for making HTTP requests using urllib.

        :param url: The URL to which a request should be made
        :type url: str
        :param data: Provide data for the request. Request method will be set to POST if data is provided
        :type data: str
        :param headers: Provide headers to send with the request
        :type headers: dict
        :return: A urllib.Request.urlopen object
        :rtype: urllib.Request.urlopen
    """

    if not headers:
        headers = {}

    # If data is provided the request method will automatically be set to POST by urllib
    request = urllib.request.Request(url, data=data, headers=headers)
    return urllib.request.urlopen(request)
