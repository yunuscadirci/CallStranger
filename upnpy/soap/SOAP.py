import urllib.parse
import urllib.error
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

import upnpy.utils as utils
from upnpy import exceptions


def _parse_response(response):
    response = response.read().decode()
    return_arguments = {}

    xml_root = minidom.parseString(response)
    xml_response_arguments = xml_root.getElementsByTagName('s:Body')[0].childNodes[0]

    for return_argument in xml_response_arguments.childNodes:
        if return_argument.firstChild is None:
            return_arguments[return_argument.tagName] = ''
        else:
            return_arguments[return_argument.tagName] = return_argument.firstChild.nodeValue

    return return_arguments


def send(service, action, **action_arguments):

    """
        **Send a SOAP request**

        This function allows you to invoke an action for the target service.

        :param service: DeviceService object
        :param action: SOAPAction object
        :return: Request response data


        - Example of a RAW SOAP request::

            POST path control URL HTTP/1.0
            HOST: hostname:portNumber
            CONTENT-LENGTH: bytes in body
            CONTENT-TYPE: text/xml; charset="utf-8"
            USER-AGENT: OS/version UPnP/1.1 product/version
            SOAPACTION: "urn:schemas-upnp-org:service:serviceType:v#actionName"

            <?xml version="1.0"?>
            <s:Envelope
            xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
            s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                <s:Body>
                    <u:actionName xmlns:u="urn:schemas-upnp-org:service:serviceType:v">
                        <argumentName>in arg value</argumentName>
                        <!-- other in args and their values go here, if any -->
                    </u:actionName>
                </s:Body>
            </s:Envelope>

    """

    args_in = action.args_in

    if not all(arg.name in action_arguments.keys() for arg in args_in):

        missing_arguments = []

        for argument in action.args_in:
            if argument.name not in action_arguments.keys():
                missing_arguments.append(argument.name)

        raise exceptions.ArgumentError(
            f'Missing arguments for action "{action.name}".',
            missing_arguments
        )

    for argument in action_arguments.keys():
        in_argument_names = [arg.name for arg in args_in]
        if argument not in in_argument_names:
            raise exceptions.ArgumentError(f'This service does not accept the "in" argument "{argument}".', argument)

    xml_root = Element('s:Envelope')
    xml_root.set('xmlns:s', 'http://schemas.xmlsoap.org/soap/envelope/')
    xml_root.set('s:encodingStyle', 'http://schemas.xmlsoap.org/soap/encoding/')

    xml_body = SubElement(xml_root, 's:Body')

    xml_action_name = SubElement(xml_body, f'u:{action.name}')
    xml_action_name.set('xmlns:u', service.service)

    for argument in action.arguments:
        try:
            argument_value = action_arguments[argument.name]
        except KeyError:
            continue

        xml_action_name_argument = SubElement(xml_action_name, argument.name)
        xml_action_name_argument.text = str(argument_value)

    soap_body = tostring(xml_root, short_empty_elements=False)

    headers = {
        'Host': f'{urllib.parse.urlparse(service.base_url).netloc}',
        'Content-Length': len(soap_body),
        'Content-Type': 'text/xml; charset="utf-8"',
        'SOAPAction': f'"{service.service}#{action.name}"'
    }

    full_control_url = service.base_url + service.control_url

    try:
        return _parse_response(
            response=utils.make_http_request(full_control_url, data=soap_body, headers=headers)
        )
    except urllib.error.HTTPError as e:
        if e.code == 500:
            response = e.read().decode()
            xml_root = minidom.parseString(response)
            error_code = xml_root.getElementsByTagName('errorCode')[0].firstChild.nodeValue
            xml_error_description = xml_root.getElementsByTagName('errorDescription')[0].firstChild

            if xml_error_description is None:
                error_description = ''
            else:
                error_description = xml_error_description.nodeValue
            raise exceptions.SOAPError(error_description, int(error_code))
        else:
            raise exceptions.SOAPError('Unknown response code received.', e.code)
