from halo_app.exceptions import HaloException

class IllegalProviderException(HaloException):
    pass

class IllegalRuntimeException(HaloException):
    pass

class IllegalServiceDomainException(HaloException):
    pass

class IllegalIdException(HaloException):
    pass
