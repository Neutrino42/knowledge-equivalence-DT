import yaml
import re
from datetime import datetime


class Config(object):
    def __init__(self, path):
        self.data = {}
        with open(path, 'r') as f:
            self.data = yaml.safe_load(f)
            if self.data["version"] != "1.0":
                self.data = {}
            else:
                self.__load()

    def __load(self):
        for k, v in self.data.items():
            self.data[k] = self.__parse(k)

    def __parse(self, name):
        """
        Cannot work when the value is a list or dict, etc.
        :param name: the dict key
        :return:
        """

        matches = re.findall("\${{(.*?)}}", self.data[name])
        new_string = self.data[name]
        for ma in matches:
            if ma.strip() == "time":
                curr_time = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
                new_string = re.sub("\${{.*?}}", curr_time, self.data[name])
        return new_string
