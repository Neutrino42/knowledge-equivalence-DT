import subprocess
import os


class SimServer(object):

    def __init__(self, jar_path):
        self.__jar_path = jar_path
        self.__process = None

    def start(self):
        assert os.path.exists(self.__jar_path)
        self.__process = subprocess.Popen(["java", "-jar", self.__jar_path])  # run in the background

    def terminate(self):
        if self.__process is not None:
            self.__process.terminate()
            self.__process.wait()
