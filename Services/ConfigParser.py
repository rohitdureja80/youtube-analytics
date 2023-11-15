import json

class ConfigParser:
    
    def __init__(self):
        environment = "LOCAL"
        configFile = "./" + environment + "_config.json"
        with open(configFile) as jsonConfig:
            self.config = json.load(jsonConfig)
    
    def DbConfigSettings(self):
        return self.config["postgres"]