"""
Global fedimg exception and warning classes
"""


class SourceNotFound(Exception):
    """ The requested source was not found"""
    pass


class CommandRunFailed(Exception):
    """ The request command failed while running"""
    pass


class UnCompressFailed(Exception):
    """ The uncompress operation of the raw image failed"""
    pass
