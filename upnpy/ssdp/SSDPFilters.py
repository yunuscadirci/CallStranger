import upnpy.utils as utils


def host_filter(device, host):
    return device.host == host


def port_filter(device, port):
    return device.port == port


def header_filter(device, headers):
    device_contains_header = False

    for header, value in headers.items():
        if utils.parse_http_header(device.response, header) == value:
            device_contains_header = True
        else:
            device_contains_header = False
            break

    return device_contains_header
