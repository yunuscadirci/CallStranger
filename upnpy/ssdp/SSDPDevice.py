from urllib.parse import urlparse
from xml.dom import minidom
from functools import wraps
import urllib.error

import upnpy.utils as utils
from upnpy.soap import SOAP
from upnpy import exceptions


def _device_description_required(func):

    """
    Decorator for checking whether the device description is available on a device.
    """

    @wraps(func)
    def wrapper(device, *args, **kwargs):
        if device.description is None:
            raise exceptions.NotRetrievedError('No device description retrieved for this device.')
        return func(device, *args, **kwargs)
    return wrapper


def _service_description_required(func):

    """
    Decorator for checking whether the service description is available on a device's service.
    """

    @wraps(func)
    def wrapper(service, *args, **kwargs):
        if service.description is None:
            raise exceptions.NotRetrievedError('No service description retrieved for this service.')
        elif service.description == exceptions.NotAvailableError:
            return
        return func(service, *args, **kwargs)
    return wrapper


def _base_url_required(func):

    """
    Decorator for constructing the BaseURL (from device response LOCATION header
    or <URLBase> element in device description).
    """

    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        if instance.base_url is None:
            raise exceptions.NotRetrievedError('No base URL was retrieved for this device.')
        return func(instance, *args, **kwargs)
    return wrapper


class SSDPDevice:

    """
        **Represents an SSDP device**

        Object for representing an SSDP device.

        :param address: SSDP device address
        :type address: tuple
        :param response: Device discovery response data
        :type response: str
    """

    def __init__(self, address, response):
        try:
           self.address = address
           self.host = address[0]
           self.port = address[1]
           self.response = response
           self.description = None
           self.friendly_name = None
           self.type_ = None
           self.base_url = None
           self.services = {}
           self.selected_service = None
           self.document_location=utils.parse_http_header(response, 'Location')
           self._get_description_request(utils.parse_http_header(response, 'Location'))
           self._get_friendly_name_request()
           self._get_type_request()
           self._get_base_url_request()
           self._get_services_request()
        except:
           print('!Error in ',address)			

    def get_services(self):

        """
            **Return a list of services available for the device**

            Returns a list of available services for the device.

            :return: List of services available for this device
            :rtype: list
        """

        return list(self.services.values())

    def get_friendly_name(self):

        """
            **Get the friendly name for the device**

            Gets the device's friendly name

            :return: Friendly name of the device
            :rtype: str
        """

        return self.friendly_name

    def _get_description_request(self, url):
        device_description=None
        try:		
            device_description = utils.make_http_request(url).read()
            self.description = device_description
        except:
            print('!Error in device description request',url)
        return device_description.decode()

    @_device_description_required
    def _get_friendly_name_request(self):
        root = minidom.parseString(self.description)
        device_friendly_name = root.getElementsByTagName('friendlyName')[0].firstChild.nodeValue
        self.friendly_name = device_friendly_name
        return self.friendly_name

    @_device_description_required
    def _get_type_request(self):
        root = minidom.parseString(self.description)
        device_type = root.getElementsByTagName('deviceType')[0].firstChild.nodeValue
        self.type_ = device_type
        return self.type_

    @_device_description_required
    def _get_base_url_request(self):
        location_header_value = utils.parse_http_header(self.response, 'Location')
        root = minidom.parseString(self.description)

        try:
            parsed_url = urlparse(root.getElementsByTagName('URLBase')[0].firstChild.nodeValue)
            base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        except IndexError:
            parsed_url = urlparse(location_header_value)
            base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

        self.base_url = base_url
        return base_url

    @_device_description_required
    @_base_url_required
    def _get_services_request(self):
        if not self.services:
            device_services = {}
            root = minidom.parseString(self.description)

            base_url = self.base_url
            try:
                for service in root.getElementsByTagName('service'):
                    service_string = service.getElementsByTagName('serviceType')[0].firstChild.nodeValue
                    service_id = service.getElementsByTagName('serviceId')[0].firstChild.nodeValue
                    scpd_url = service.getElementsByTagName('SCPDURL')[0].firstChild.nodeValue
                    control_url = service.getElementsByTagName('controlURL')[0].firstChild.nodeValue
                    event_sub_url = ('/'+service.getElementsByTagName('eventSubURL')[0].firstChild.nodeValue).replace('//','/') # dirty hack for eventSubURL startr with / or not 
                    
                    parsed_service_id = utils.parse_service_id(service_id)
                    
                    if parsed_service_id not in device_services.keys():
                        device_services[parsed_service_id] = self.Service(
                            service=service_string,
                            service_id=service_id,
                            scpd_url=scpd_url,
                            control_url=control_url,
                            event_sub_url=event_sub_url,
                            base_url=base_url
                        )
            except Exception as e:
                print('!Error in service definition',self.base_url,service_string)
                
            self.services = device_services

        return self.services

    def __getitem__(self, service_id):

        """
            **Allow access to a specific service on the device through a dictionary**

            Allows the user to access a specific service by its ID for the selected device through a dictionary key.

            :param service_id: ID for the service to select
            :return: Instance of SSDPDevice.Service for the service with the specified service ID
            :rtype: SSDPDevice.Service
        """

        try:
            return self.services[service_id]
        except KeyError:
            raise exceptions.ServiceNotFoundError(f'No service found with ID "{service_id}".', service_id)

    def __getattr__(self, service_id):

        """
            **Allow access to a specific service on the device through an attribute**

            Allows the user to access a specific service by its ID for the device through an attribute.

            :param service_id: ID for the service to use
            :return: Instance of SSDPDevice.Service for the service with the specified service ID
            :rtype: SSDPDevice.Service
        """

        try:
            return self.services[service_id]
        except KeyError:
            raise exceptions.ServiceNotFoundError(f'No service found with ID "{service_id}".', service_id)

    def __repr__(self):
        return f'Device <{self.friendly_name}>'

    class Service:

        """
            **Device service**

            Represents a service available on the device.

            :param service: Full service string (e.g.: ``urn:schemas-upnp-org:service:WANIPConnection:1``)
            :type service: str
            :param service_id: ID of the service
            :type service_id: str
            :param scpd_url: SCPD URL of the service
            :type scpd_url: str
            :param control_url: Control URL of the service
            :type control_url: str
            :param event_sub_url: Event Sub URL of the service
            :type event_sub_url: str
            :param base_url: Base URL of the service
            :type base_url: str
        """

        def __init__(self, service, service_id, scpd_url, control_url, event_sub_url, base_url):
            self.service = service
            self.type_ = self._get_service_type(service)
            self.version = self._get_service_version(service)
            self.id = service_id
            self.scpd_url = scpd_url
            self.control_url = control_url
            self.event_sub_url = event_sub_url
            self.base_url = base_url
            self.actions = {}
            self.description = None
            self.state_variables = {}

            #self._get_description_request()
            #self._get_state_variables_request()
            #self._get_actions_request()

        def get_actions(self):

            """
                **Return a list of actions available for the service**

                Returns a list of available actions for the service.

                :return: List of actions available for this service
                :rtype: list
            """

            if self.description == exceptions.NotAvailableError:
                raise exceptions.NotAvailableError('Can\'t get actions because a description for this service is'
                                                   ' not available.')
            return list(self.actions.values())

        def _get_description_request(self):

            """
                **Get the description of the service**

                Gets the service description by sending a request to the SCPD URL of the service.

                :return: Service description
                :rtype: str
            """

            try:
                service_description = utils.make_http_request(self.base_url +'/'+	self.scpd_url).read()
                self.description = service_description.decode()
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self.description = exceptions.NotAvailableError
                else:
                    raise

            return self.description

        @_service_description_required
        def _get_actions_request(self):

            """
                **Get the service actions**

                Gets the actions available for the service.

                :return: List of actions available for the service
                :rtype: list
            """

            all_actions = {}
            service_description = self.description

            root = minidom.parseString(service_description)
            actions = root.getElementsByTagName('action')

            for action in actions:
                action_name = action.getElementsByTagName('name')[0].firstChild.nodeValue
                action_arguments = []

                # An action's argument list is only required if the action has parameters according to UPnP spec
                try:
                    action_argument_list = action.getElementsByTagName('argumentList')[0]
                except IndexError:
                    action_argument_list = None

                if action_argument_list:
                    action_arguments_elements = action_argument_list.getElementsByTagName('argument')

                    for argument in action_arguments_elements:
                        argument_name = argument.getElementsByTagName('name')[0].firstChild.nodeValue
                        argument_direction = argument.getElementsByTagName('direction')[0].firstChild.nodeValue

                        # Argument return value is optional according to UPnP spec
                        try:
                            argument_return_value = argument.getElementsByTagName('retval')[0].firstChild.nodeValue
                        except IndexError:
                            argument_return_value = None

                        argument_related_state_variable = argument.getElementsByTagName(
                            'relatedStateVariable'
                        )[0].firstChild.nodeValue

                        action_arguments.append(
                            self.Action.Argument(
                                argument_name,
                                argument_direction,
                                argument_return_value,
                                argument_related_state_variable
                            )
                        )

                all_actions[action_name] = self.Action(action_name, action_arguments, self)

            self.actions = all_actions
            return all_actions

        @_service_description_required
        def _get_state_variables_request(self):

            service_description = self.description

            root = minidom.parseString(service_description)
            state_variables = {}

            xml_state_variables = root.getElementsByTagName('stateVariable')

            for state_variable in xml_state_variables:
                state_variable_name = state_variable.getElementsByTagName('name')[0].firstChild.nodeValue
                state_variable_data_type = state_variable.getElementsByTagName('dataType')[0].firstChild.nodeValue
                state_variable_allowed_value_list = []

                xml_allowed_values = state_variable.getElementsByTagName('allowedValue')

                if xml_allowed_values:
                    for allowed_value in xml_allowed_values:
                        state_variable_allowed_value_list.append(allowed_value.firstChild.nodeValue)

                state_variables[state_variable_name] = self.StateVariable(
                    state_variable_name,
                    state_variable_data_type,
                    state_variable_allowed_value_list
                )

            self.state_variables = state_variables
            return self.state_variables

        @staticmethod
        def _get_service_type(service):

            """
            Parse the service type <serviceType> portion of the service.
            """

            return service.split(':')[3]

        @staticmethod
        def _get_service_version(service):

            """
            Parse the service version <v> portion of the service.
            """

            return int(service.split(':')[4])

        def __getattr__(self, action_name):

            """
                **Allow executing an action through an attribute**

                Allows executing the specified action on the service through an attribute.

                :param action_name: Name of the action to execute on the service
                :return: Response from the device's service after executing the specified action
                :rtype: dict
            """

            if self.description == exceptions.NotAvailableError:
                raise exceptions.NotAvailableError('Can\'t execute actions because a description for this service is'
                                                   ' not available.')

            try:
                return self.actions[action_name]
            except KeyError:
                raise exceptions.ActionNotFoundError(
                    f'The "{action_name}" action is not available for this service.',
                    action_name
                )

        def __repr__(self):
            return f'<Service ({self.type_}) id="{utils.parse_service_id(self.id)}">'

        class Action:

            """
                **Represents an action on a service**

                This class holds the details of a specific action available on a service.

                :param name: Name of the action
                :type name: str
                :param argument_list: List of in / out arguments the action has
                :type argument_list: list
                :param service: The service to which this action belongs
                :type service: SSDPDevice.Service
            """

            def __init__(self, name, argument_list, service):
                self.name = name
                self.arguments = argument_list
                self.args_in = []
                self.args_out = []
                self.service = service

                for argument in self.arguments:
                    direction = argument.direction
                    if direction == 'in':
                        self.args_in.append(argument)
                    elif direction == 'out':
                        self.args_out.append(argument)
                    else:
                        raise exceptions.ArgumentError(
                            f'No valid argument direction specified by service for argument "{argument.name}".',
                            argument.name
                        )

            def get_input_arguments(self):

                """
                    **Get the input arguments for the action**

                    Gets the input arguments for the action.

                    :return: List of input arguments for the action
                    :rtype: list
                """

                input_arguments = []

                for argument in self.args_in:
                    related_state_variable = self.service.state_variables[argument.related_state_variable]
                    input_arguments.append(
                        {
                            'name': argument.name,
                            'data_type': related_state_variable.data_type,
                            'allowed_value_list': related_state_variable.allowed_value_list
                        }
                    )

                return input_arguments

            def get_output_arguments(self):

                """
                    **Get the output arguments for the action**

                    Gets the output arguments for the action.

                    :return: List of output arguments for the action
                    :rtype: list
                """

                output_arguments = []

                for argument in self.args_out:
                    related_state_variable = self.service.state_variables[argument.related_state_variable]
                    output_arguments.append(
                        {
                            'name': argument.name,
                            'data_type': related_state_variable.data_type,
                            'allowed_value_list': related_state_variable.allowed_value_list
                        }
                    )

                return output_arguments

            def __call__(self, **action_kwargs):

                """
                    **Execute the action**

                    Executes the action on the service by calling the class.

                    :param action_kwargs: Arguments for this action if any
                    :type action_kwargs: str, int
                    :return: Response from the device's service after executing the action
                    :rtype: dict
                """

                return SOAP.send(self.service, self, **action_kwargs)

            def __repr__(self):
                return f'<Action name="{self.name}">'

            class Argument:

                """
                    **Represents an argument for an action**

                    This class holds the details of an argument for an action.

                    :param name: Name of the argument
                    :type name: str
                    :param direction: Direction of the argument (in/out)
                    :type direction: str
                    :param return_value: Identifies at most one output argument as the return value
                    :type return_value: str
                    :param related_state_variable: Defines the type of the argument
                """

                def __init__(self, name, direction, return_value, related_state_variable):
                    self.name = name
                    self.direction = direction
                    self.return_value = return_value
                    self.related_state_variable = related_state_variable

        class StateVariable:
            def __init__(self, name, data_type, allowed_value_list=None):
                self.name = name
                self.data_type = data_type
                self.allowed_value_list = allowed_value_list

            def __repr__(self):
                return f'StateVariable <name="{self.name}">'
