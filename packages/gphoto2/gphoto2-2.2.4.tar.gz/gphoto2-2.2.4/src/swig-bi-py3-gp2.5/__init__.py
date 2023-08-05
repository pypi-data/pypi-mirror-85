__version__ = "2.2.4"


class GPhoto2Error(Exception):
    """Exception raised by gphoto2 library errors

    Attributes:
        code   (int): the gphoto2 error code
        string (str): corresponding error message
    """
    def __init__(self, code):
        string = gp_result_as_string(code)
        Exception.__init__(self, '[%d] %s' % (code, string))
        self.code = code
        self.string = string

from gphoto2.abilities_list import *
from gphoto2.camera import *
from gphoto2.context import *
from gphoto2.file import *
from gphoto2.filesys import *
from gphoto2.list import *
from gphoto2.port_info_list import *
from gphoto2.port_log import *
from gphoto2.result import *
from gphoto2.version import *
from gphoto2.widget import *

__all__ = dir()
