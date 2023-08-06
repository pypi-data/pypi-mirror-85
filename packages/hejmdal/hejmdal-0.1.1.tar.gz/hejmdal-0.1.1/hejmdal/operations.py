from .base import *
from . import datacalls
from . import formatting

def generate_file(form, data_gen=None):
    if data_gen is None: data_gen = datacalls.MainData
    data = data_gen(form)
    result = form.return_format(data)
    return result


def build_site_list():
    base_sites = read_sites()
    sites = {'sitesother':[]}
    for key in base_sites.keys():
        items = [line.split() for line in base_sites[key]]
        if key == 'Greenland West:':
            sites['siteswest'] = items
        elif key == 'Greenland East:':
            sites['siteseast'] = items
        else:
            sites['sitesother'] += items
    return sites

def read_sites():
    sections = {}
    name = None
    with open('static/ListofStations.txt') as f:
        for line in f.read().split('\n'):
            if not line:
                if name is not None:
                    sections[name] = section
                name = None
            elif name is None:
                name = line
                section = []
            else:
                section.append(line)
    return sections
    