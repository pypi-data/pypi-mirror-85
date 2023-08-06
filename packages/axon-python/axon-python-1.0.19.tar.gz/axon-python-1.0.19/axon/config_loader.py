from configparser import ConfigParser


class Config:
    def __init__(self, config_file_path):
        self.cf = ConfigParser(allow_no_value=True)
        self.cf.optionxform = str
        self.config_file_path = config_file_path
        self.cf.read(self.config_file_path)

    def get_section(self, section):
        return dict(self.cf.items(section))

    def set_section(self, items):
        # Re-save file
        for item in items:
            if 'key' in item and 'value' in item:
                self.cf.set('SETTINGS', item['key'], item['value'])

        with open(self.config_file_path, 'w') as config_file:
            self.cf.write(config_file)
