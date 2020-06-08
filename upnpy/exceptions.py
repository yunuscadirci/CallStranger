class SOAPError(Exception):

    """
        **Custom SOAP exception**

        Custom SOAP exception class.
        Raised whenever an error response has been received during action invocation.
    """

    def __init__(self, description, code):
        self.description = description
        self.error = code


class IGDError(Exception):

    """
        **Custom Internet Gateway Device exception**

        Custom IGD exception class.
        Raised whenever a problem with the IGD has been detected.
    """

    pass


class ArgumentError(Exception):

    """
        **Custom Argument exception**

        Custom Argument exception class.
        Raised whenever an error has been detected during action invocation.
    """

    def __init__(self, message, argument):
        self.message = message
        self.argument = argument


class ServiceNotFoundError(Exception):

    """
        **Custom Service exception**

        Custom Service exception class.
        Raised whenever a particular service was not found for a device.
    """

    def __init__(self, message, service_name):
        self.message = message
        self.service = service_name


class ActionNotFoundError(Exception):

    """
        **Custom Action exception**

        Custom Action exception class.
        Raised whenever a particular action is not available for a service.
    """

    def __init__(self, message, action_name):
        self.message = message
        self.action = action_name


class NotRetrievedError(Exception):

    """
        **Custom exception for objects that have not been retrieved**

        Custom object not retrieved exception class.
        Raised whenever a certain property for a device or service was not retrieved.
    """

    pass


class NotAvailableError(Exception):

    """
        **Custom exception for when a certain URL could not be retrieved**

        Custom element not retrieved exception class.
        Raised whenever a value needed to be accessed could not be retrieved from the URL.
    """

    pass
