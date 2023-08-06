class PluginException(Exception):
    status = 'Exception'
    exit_code = 3


class PluginWarning(PluginException):
    status = 'Warning'
    exit_code = 1


class PluginError(PluginException):
    status = 'Error'
    exit_code = 2


class PluginUnknown(PluginException):
    status = 'Unknown'
    exit_code = 3
