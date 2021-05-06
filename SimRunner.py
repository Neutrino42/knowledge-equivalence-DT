import subprocess
import os


class SimRunner(object):

    def __init__(self, jar_path):
        self.__path = jar_path

    def run(self):
        assert os.path.exists(self.__path)
        subprocess.run(["java", "-jar", self.__path], timeout=20)

