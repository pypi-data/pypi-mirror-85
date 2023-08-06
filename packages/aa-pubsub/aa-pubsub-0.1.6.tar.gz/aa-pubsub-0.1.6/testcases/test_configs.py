import unittest
import os
import sys
import logging


def reset_robot_config_path(env ,root, folder):
    try:
        os.environ[env] = os.path.join(root, folder)
    except Exception as e:
        logging.debug(e)
        os.environ.setdefault(env,os.path.join(root, folder))


class ADeprecatedConfigsTest(unittest.TestCase):
    def setUp(self):
        # use ROBOT_CONFIGS
        _root = sys.path[0]
        logging.debug('run in root: {}'.format(_root))
        self.root = _root        
    
    def testDeprecatedConfigFile(self):                
        reset_robot_config_path('ROBOT_CONFIGS', self.root, 'deprecated_config')
        from pubsub.configs import ROBOT_CFGS
        self.assertEqual(ROBOT_CFGS['host'], "127.0.0.1")


class ConfigsTest(unittest.TestCase):
    def setUp(self):
        from pubsub import configs
        # use ROBOT_CONFIGS
        _root = sys.path[0]
        logging.debug('run in root: {}'.format(_root))
        reset_robot_config_path(configs.ROBOT_CONFIGS_PATH, _root, 'config')
        _configs = configs.Configs()
        self.configs = _configs
        self.root = _root

    def testFileNotExist(self):
        _file = os.path.join(self.root, 'config', 'notexist.yaml')
        with self.assertRaises(Exception) as e:        
            _configs = configs.Configs(_file)
            self.assertEqual(
                configs.CANNOT_LOAD.format(_file),
                str(e.exception)
            )
    
    def testEmptyFile(self):
        _file = os.path.join(self.root, 'config', 'empty.yaml')
        with self.assertRaises(Exception) as e:
            _configs = configs.Configs(_file)
            self.assertEqual(
                configs.CANNOT_LOAD.format(_file),
                str(e.exception)
            )

    def testCustomFile(self):
        _file = os.path.join(self.root, 'config', 'custom.yaml')        
        with self.assertRaises(Exception) as e:
            _configs = configs.Configs(_file)            
            self.assertTrue(False)
    
    def testInvalidModel(self):
        _model = 'nomodel'
        with self.assertRaises(Exception) as e:
            val = self.configs.get_config(_model)
            self.assertEqual(
                configs.INVALID_MODEL.format(_model),
                str(e.exception)
            )

    def testModelisNone(self):
        _model = None
        with self.assertRaises(Exception) as e:
            val = self.configs.get_config(_model)
            self.assertEqual(
                configs.INVALID_MODEL.format(_model),
                str(e.exception)
            )

    def testParamisNone(self):
        _model = 'test'
        _param = None
        with self.assertRaises(Exception) as e:
            val = self.configs.get_config(_model, _param)
            self.assertEqual(
                configs.INVALID_MODEL.format(_model),
                str(e.exception)
            )

    def testInvalidParam(self):
        _model = 'test'
        _param = 'None'        
        with self.assertRaises(Exception) as e:
            val = self.configs.get_config(_model, _param)
            self.assertEqual(
                configs.INVALID_PARAM.format(_model, _model, _param),
                str(e.exception)   
            )
