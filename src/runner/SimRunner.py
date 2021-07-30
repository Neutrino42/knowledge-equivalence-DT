import subprocess
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


class SimRunner(object):

    def __init__(self, jar_path, repast_dir, final_end_time):
        self.__path = jar_path
        self.__repast_dir = repast_dir
        self.__repast_param_path = repast_dir + "mobileCameras.rs/parameters.xml"
        self.__repast_rs = repast_dir + "mobileCameras.rs"
        self.__final_end_time = final_end_time

    def run(self):
        assert os.path.exists(self.__path)
        subprocess.run(["java", "-jar", self.__path, self.__repast_rs, self.__final_end_time], timeout=60)

    def modify_repast_params(self, name, value):
        tree = ET.parse(self.__repast_param_path)
        root = tree.getroot()
        for param in root.findall('parameter'):
            if param.get('name') == name:
                param.set('defaultValue', str(value))
        tree.write(self.__repast_param_path, encoding='utf-8', xml_declaration=True)
