from .base import *

from . import formatting
import re
import datetime
from pathlib import Path

def to_datetime(string):
    numbers = list(map(int,re.split('-| |:|/', string)))
    return datetime.datetime(*numbers) if len(numbers)>3 else datetime.date(*numbers)
    
    
def string_options(*options):
    if len(options) == 1 and not isinstance(options[0], str):
        options = options[0]
    def type_gen(string):
        if string in options:   
            return string
        else:
            raise TypeError()
    return type_gen
    
def enum_options(*options, offset=0):
    if len(options) == 1 and not isinstance(options[0], str):
        options = options[0]
    def type_gen(string):
        for i, option in enumerate(options):
            if string == option:
                return i+offset
        else:
            return int(string)
    return type_gen

def dict_options(base=None, **options):
    if base is None:
        base = {}
    options = {**base, **options}
    def type_gen(string):
        if string in options:
            return options[string]
        else:
            raise TypeError()

class BaseForm:
    def __init__(self,**kwargs):
        self._args = kwargs

    @property
    def args(self):
        return self._args

    def load_data(self, name, default=None, type_gen=int):
        result = self.args.get(name, default)
        try:
            result = type_gen(result)
        except Exception as e:
            result = default
        return result

    def locations(self):
        return [name.upper() for name in self.core.args if len(name)==3 and name.isalpha()]

    def start_date(self):
        return self.load_data('startdate', datetime.datetime(1,1,1), to_datetime)

    def end_date(self):
        return self.load_data('enddate', datetime.datetime.now(), to_datetime)

    def quality(self):
        return self.load_data('quality', 'adjusted', type_gen=string_options('adjusted', 'reported'))

    def baselines(self):
        return self.load_data('baselines', 'yes', type_gen=string_options('yes', 'no'))

    def orientation(self):
        return self.load_data('orientation', 'XYZ', type_gen=string_options('XYZ','HDZ'))

    def resolution(self):
        return self.load_data('resolution', 'any', type_gen=string_options('any'))

    def requested_data_format(self):
        #remove references to this and then delete it...
        return self.load_data('format', default='default', type_gen=string_options(FORMAT_LIBRARY))

    # def __getattr__(self, key):
        # self.core.__getattribute__(key)

    @property
    def return_format(self):
        # return formatting.ReturnFormat
        format = self.load_data('format', default='default', type_gen=string_options(FORMAT_LIBRARY)) #TODO: get the actual format
        return FORMAT_LIBRARY.get(format, formatting.ReturnFormat)        


class RequestForm(BaseForm):
    def __init__(self, request):
        super().__init__()
        self.core = request

    @property
    def args(self):
        return self.core.args
        
class TrustedForm(BaseForm):
    #WARNING: this class assumes that the giver of the request is trusted, and as such slacks on the safety checking on some of its functions.
    
    def filepath(self):
        return self.load_data('filepath', type_gen=Path)
        
    def url(self):
        return self.load_data('filepath', 'geomag.space.dtu.dk/magdata/download', type_gen=str)

        
    def protocol(self):
        result = self.load_data('protocol', type_gen=str)#string_options('http', 'https'))
        return result if result != 'None' else None
