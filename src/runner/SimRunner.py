import subprocess
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from Loader import TraceLoader


class SimRunner(object):

    def __init__(self, jar_path, repast_rs, final_end_time, output_dir):
        self.__jar_path = jar_path
        self.__repast_rs = repast_rs
        self.__repast_param_path = repast_rs + "parameters.xml"
        self.__final_end_time = str(final_end_time)
        self.__output_dir = output_dir
        self.__params = ET.parse(self.__repast_param_path)
        self.__trace_loader = TraceLoader(output_dir)

    def run(self):
        assert os.path.exists(self.__jar_path)
        os.makedirs(self.__output_dir, exist_ok=True)
        subprocess.run(["java", "-jar", self.__jar_path, self.__repast_rs, self.__final_end_time], timeout=60)

    def modify_repast_params(self, kv_pair: dict):
        root = self.__params.getroot()
        for k, v in kv_pair.items():
            for param in root.findall('parameter'):
                if param.get('name') == k:
                    param.set('defaultValue', str(v))
        self.__params.write(self.__repast_param_path, encoding='utf-8', xml_declaration=True)

    def get_traces(self):
        return self.__trace_loader.read_trace()
