import subprocess
import os


class SimServer(object):

    def __init__(self, jar_path, port=None):
        self.__jar_path = jar_path
        self.__process = None
        self.__port = port

    def start(self):
        assert os.path.exists(self.__jar_path)
        if self.__port is None:
            self.__process = subprocess.Popen(["java", "-jar", self.__jar_path])  # run in the background
        else:
            self.__process = subprocess.Popen(["java", "-jar", self.__jar_path, str(self.__port)])

    def terminate(self):
        if self.__process is not None:
            self.__process.terminate()
            self.__process.wait()
