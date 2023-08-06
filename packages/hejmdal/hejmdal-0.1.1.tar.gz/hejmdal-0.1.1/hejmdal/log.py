import sys
from logging.config import dictConfig

log_locaton = 'logs/'

def dict_gen(filt=None, format_mod=''):
    def handle_gen(subpath, file=None, level='INFO', **other):
        handle_dict = {
            'class':'logging.'+subpath,
            'level': level,
            'formatter':'default',
            **other
        }
        if file is not None:
            handle_dict['filename'] = f"{log_locaton}{file}.log"
        if filt is not None:
            handle_dict['filters'] = ['customFilt']
        return handle_dict
    handlers = {
        'wsgi':handle_gen('StreamHandler', stream='ext://flask.logging.wsgi_errors_stream'),
        'appLogger':handle_gen('FileHandler',file='main'),
        'session':handle_gen('FileHandler',file='session', level='DEBUG'),
        'rotating':handle_gen('handlers.RotatingFileHandler',file='rotation',level='DEBUG')
    }
    format = f'[%(asctime)s] %(levelname)s in %(module)s @ L%(lineno)d{format_mod}: %(message)s'
    # format = '[%(asctime)s] %(levelname)s in %(module)s @ L%(lineno)d: %(message)s'
    # if filt is not None:
        # format = '[%(asctime)s] %(levelname)s in %(module)s @ L%(lineno)d under %(url)s for %(access_route)s: %(message)s'
    config = {
            'version':1,
            'formatters':{'default': {
                'format': format
            }},
            'handlers':handlers,
            'root': {
                'level': 'DEBUG',
                'handlers': list(handlers.keys())
            }
        }
    if filt is not None:
        config['filters'] = {'customFilt':{'()': filt}}
    return config
    # return {
            # 'version':1,
            # 'formatters':{'default': {
                # 'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            # }},
            # 'handlers':{
                # 'wsgi': {
                    # 'class': 'logging.StreamHandler',
                    # 'stream': 'ext://flask.logging.wsgi_errors_stream',
                    # 'level': 'INFO',
                    # 'formatter': 'default'
                # },
                # 'appLogger':{
                    # 'class': 'logging.FileHandler',
                    # 'filename': 'logs/main.log',
                    # 'level': 'INFO',
                    # 'formatter': 'default'
                # },
                # 'session':{
                    # 'class': 'logging.FileHandler',
                    # 'filename': 'logs/session.log',
                    # 'mode': 'w',
                    # 'level': 'DEBUG',
                    # 'formatter': 'default'
                # },
                # 'rotating':{
                    # 'class': 'logging.handlers.RotatingFileHandler',
                    # 'filename': 'logs/rotation.log',
                    # 'level': 'DEBUG',
                    # 'maxBytes': 1048576,
                    # 'backupCount': 2,
                    # 'formatter': 'default'
                # },
            # },
            # 'root': {
                # 'level': 'DEBUG',
                # 'handlers': ['wsgi', 'appLogger', 'session','rotating']
            # }
        # }



logger = None
log_builder = None
pre_config = None

# def get_logger():
    # global logger
    # if logger is None:
        # if 'app' in sys.modules:
            # import app
            # from logging import Filter
            # class ContextFilter(Filter):
                # def filter(self, record):
                    # record.url = app.request.url
                    # record.access_route = ', '.join(app.request.access_route)
                    # return True
            # dictConfig(dict_gen(ContextFilter, ' under %(url)s for %(access_route)s'))
            # logger = app.app.logger
        # else:
            # import logging
            # dictConfig(dict_gen())
            # logger = logging.root
    # return logger
    
def get_logger():
    global logger
    if logger is None:
        if log_builder is not None:
            dictConfig(pre_config)
            logger = log_builder()
        else:
            import logging
            dictConfig(dict_gen())
            logger = logging.root
    return logger

def register_logger(logger_gen, context_filter=None, format_mod=''):
    global log_builder, pre_config
    if log_builder is None:
        # dictConfig(dict_gen(context_filter, format_mod))
        pre_config = dict_gen(context_filter, format_mod)
        log_builder = logger_gen
    else:
        get_logger().warning(f'trying to register an extra logger: {logger_gen}')

def log_gen(prefix="", msg="", level='info'):
    get_logger().__getattribute__(level)(f"{prefix}{msg}")
    # if 'app' in sys.modules:
        # from app import request
        # get_logger().__getattribute__(level)(f"{prefix}{request.url} for {', '.join(request.access_route)}: {msg}")
    # else:
        # import logging
        # get_logger().__getattribute__(level)(f"{prefix}: {msg}")
