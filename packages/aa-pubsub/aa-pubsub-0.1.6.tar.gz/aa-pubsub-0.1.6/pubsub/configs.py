import logging
import os
import warnings
import yaml

INVALID_CONFIG = 'invalid config file: {}'
CANNOT_LOAD = 'can not load config fle: {}'
CUSTOM_CONFIG = 'use custom config file: {}'
SYSTEM_CONFIG = 'use system config file: {}'
INVALID_MODEL = 'invalid config model or model is not configured: {}'
INVALID_PARAM = 'invalid param in config model {} or param is not configured in config model {}: {}'

ROBOT_CONFIGS_PATH = 'ROBOT_CONFIGS'
CONFIG_FILES = 'pubsub.yaml'

DEPRECATED_WARNING = 'you are using a deprecated config file, please udpate your pubsub application and re-config it'

class Configs():
    def __init__(self, config_file=None):
        if config_file is None:
            logging.debug(SYSTEM_CONFIG.format(config_file))
            config_file = os.path.join(os.getenv(ROBOT_CONFIGS_PATH),
                                       CONFIG_FILES)
        else:
            logging.debug(CUSTOM_CONFIG.format(config_file))

        self.config_file = config_file
        valid, msg = self.check_config_file()
        if not valid:
            raise Exception(msg)
        configs = self.get_configs()
        if configs is None:
            msg = CANNOT_LOAD.format(self.config_file)
            logging.error(msg)
            raise Exception(msg)
        self.configs = configs

    def check_config_file(self):
        msg = ''
        if not os.path.isfile(self.config_file):
            msg = INVALID_CONFIG.format(self.config_file)
            logging.error(msg)
            return False, msg
        return True, msg
    
    def check_config(self):
        try:
            mono = self.configs['mono']
            return True
        except KeyError as e:
            logging.error(DEPRECATED_WARNING)
            return False        

    def get_configs(self):
        config = None
        if os.path.isfile(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f.read(), )
        return config

    def get_config(self, model, param=''):
        res = None
        if model is None or model.strip() == '':
            msg = INVALID_MODEL.format(model)
            logging.error(msg)
            raise Exception(msg)
        try:
            config = self.configs[model]
        except KeyError as e:
            msg = INVALID_MODEL.format(model)
            logging.error(msg)
            logging.error(e)
            raise Exception(INVALID_MODEL.format(model))
        if param is None or param.strip() == '':
            res = config
        else:
            try:
                res = config[param]
            except KeyError as e:
                msg = INVALID_PARAM.format(model, model, param)
                logging.error(msg)
                logging.error(e.message)
                raise Exception(INVALID_PARAM.format(model, model, param))

        return res



def get_default_robot_configs():
    warnings.warn("get_default_robot_configs is deprecated, it's for Pubsub lower than 1.4.0", DeprecationWarning)
    config = {}
    config['track_type']='sub'
    config['track_source']='0'
    config['track_host']='127.0.0.1'
    config['track_port']='6379'
    config['track_db']='3'
    config['track_name']='robot_track_pub'
    config['track_topic']='robot_track'

    config['type']='sub'
    config['source']='0'
    config['host']='127.0.0.1'
    config['port']='6379'
    config['db']='3'
    config['name']='robot_mono'
    config['topic']='robot_mono'
    return config


def get_robot_configs():
    warnings.warn("get_default_robot_configs is deprecated, it's for Pubsub lower than 1.4.0", DeprecationWarning)
    config = get_default_robot_configs()       
    robot_configs=os.getenv('ROBOT_CONFIGS')
    if robot_configs is not None:
        config_file = os.path.join(robot_configs, 'pubsub.yaml')
        if os.path.isfile(config_file):
            print('>> use user config file:{}'.format(config_file))
            with open(config_file, 'r') as f:
                config = yaml.load(f.read())
    return config 


# const value
def get_config():
    _configs = Configs()
    ck = _configs.check_config()
    if ck:
        return _configs.get_configs()
    else:
        return get_robot_configs()

ROBOT_CFGS = get_config()