from redismon.config import Config

import unittest


class TestStringMethods(unittest.TestCase):
    def test_config_with_none_section(self):
        config = Config("./tests/test.ini")
        self.assertEquals(None, config.get("none_section"))

    def test_config_with_existed_section_with_existed_key(self):
        config = Config("./tests/test.ini")
        app = config.get("app")
        self.assertEquals("8080", app.get("port"))

    def test_config_with_existed_section_with_not_existed_key(self):
        config = Config("./tests/test.ini")
        app = config.get("app")
        self.assertEquals(None, app.get("value"))
