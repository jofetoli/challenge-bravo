import unittest
from yaml.scanner import ScannerError

from infrastructure.settings import get_config, config


class SettingsTests(unittest.TestCase):

    def test_incorret_path(self):
        with self.assertRaises(FileNotFoundError) as context:
            _config = get_config('10.56')

    def test_incorret_settings_file(self):
        with self.assertRaises(ScannerError) as context:
            _config = get_config('infrastructure/test/test_nok.yaml')

    def test_corret_settings_file(self):
        self.assertTrue('postgres' in config)
        self.assertTrue('cron' in config)

    def test_no_path(self):
        with self.assertRaises(TypeError) as context:
            config = get_config(None)
                   
if __name__ == '__main__':
    unittest.main()
