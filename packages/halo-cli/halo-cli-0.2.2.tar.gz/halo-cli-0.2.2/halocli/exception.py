
class CliException(Exception):
    pass

class ConfigException(CliException):
    pass

class HaloCommandException(CliException):
    pass

class HaloPluginMngrException(CliException):
    pass

class HaloPluginClassException(CliException):
    pass

class HaloPluginException(CliException):
    pass

class ValidException(CliException):
    pass