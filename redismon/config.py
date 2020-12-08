from configparser import ConfigParser, ExtendedInterpolation


class Config:
    def __init__(self, path):
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.parser.read(path)
        self.config = self.build_config(self.parser)
        

    def build_config(self, parser):
        config = {}
        for section in self.parser.sections():
            m = {}
            for key in self.parser[section]:
                m[key] = self.parser.get(section, key)
                
            config[section] = m

        return config

    def get(self, section):
        if section not in self.config:
            return None

        return self.config[section]
