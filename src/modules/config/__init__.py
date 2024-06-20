
from json import load
from os.path import abspath, dirname

class Config:

    def __init__(self) -> None:
        config = self.read_config()
        for key, value in config.items():
            self.__setattr__(key,value)

    def read_config(self) -> dict:
        config : dict = {}
        config_path = f'{dirname(abspath(__file__))}/config.json'
        with open(config_path,'r') as file:
            config = load(file)
            file.close()
        return config
    
CONFIG = Config()