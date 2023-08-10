import configparser

class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.read_config()
    
    def read_config(self):
        self.config.read(self.config_file, encoding='utf-8')

        self.token = self.config['settings']['bot_token']
        self.owner_id = self.config['settings']['owner_id']
        self.manager = self.config['settings']['manager']

    def set_manager(self, manager):
        self.manager = manager
        self.config.set('settings', 'manager', manager)
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

config = Config('config.ini')