from .base import *
from . import operations
from . import formatting
from . import forms
from . import datacalls

def get_data(data_gen=None, form=None, **options):
    if form is None:
        form = forms.TrustedForm(**options)
    if data_gen is None:
        if isinstance(data_gen, str):
            data_gen = {
                'default':datacalls.SmartSourceData,
                'general':datacalls.SmartSourceData,
                'local':datacalls.FileData,
                'download':datacalls.DownloadData,
                'server':datacalls.JsonData,
                'json':datacalls.JsonData,
            }.get(data_gen,datacalls.JsonData)
        else:
            data_gen = datacalls.JsonData
    return data_gen(form)


def get_file(data_gen=None, form=None, **options):
    if form is None:
        form = forms.TrustedForm(**options)
    data = get_data(data_gen, form, **options)
    return form.return_format(data)

def main():
    #should hold code to handle when called from command line
    pass
    
if __name__ == '__main__':
    main()