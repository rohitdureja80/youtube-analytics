import json

class ConfigParser:
    
    def __init__(self):
        with open("./config.json") as jsonConfig:
            self.config = json.load(jsonConfig)
    
    def DbConfigSettings(self):
        return self.config["postgres"]