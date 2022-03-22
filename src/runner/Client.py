from py4j.java_gateway import JavaGateway, GatewayParameters
from py4j.protocol import Py4JJavaError
import xml.etree.ElementTree as ET
import os
from Loader import TraceLoader
import time


class Client(object):
    def __init__(self, rs_dir=None, port=None):
        """
        Constructor
        :param rs_dir: the .rs directory of the Repast model
        :param port: the listening port of the simulator server
        """
        self.__port = port
        if rs_dir is not None:
            self.__rs_dir = rs_dir
        else:
            self.__rs_dir = "/Users/Nann/eclipse-workspace/mobileCameras/mobileCameras.rs"
        for i in range(10):
            try:
                if self.__port is not None:
                    self.__gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self.__port))
                else:
                    self.__gateway = JavaGateway()
                self.__runner = self.__gateway.entry_point.getRunner()
                break
            except:
                time.sleep(0.5)
                # TODO: change to a more elegant way of connection checking

        self.__trace_loader = TraceLoader("")
        self.trace_raw = ""

    def __load(self):
        try:
            self.__runner.load(self.__rs_dir)
            # print("loaded: " + self.__rs_dir)
        except:
            print("ERROR: load config file failed, please check your file path")
            exit(-2)
        # instantiate TraceLoader by reading output path from parameters.xml
        output_dir = ""
        root = ET.parse(os.path.join(self.__rs_dir, "parameters.xml")).getroot()
        for param in root.findall('parameter'):
            if param.get('name') == "output_trace_path":
                output_dir = param.get('defaultValue')
                break
        if output_dir == "":
            exit(-3)
        self.__trace_loader.set_trace_path(output_dir)

    def __run_init(self):
        self.__runner.runInitialize()
        self.__runner.setOutputStream()

    def load_and_init(self):
        try:
            self.__runner.stop()
            self.__runner.cleanUpRun()
        except Py4JJavaError:
            print("First initialisation")
        self.__load()
        self.__run_init()

    def step(self):
        if self.__runner.getActionCount() > 0:
            if self.__runner.getModelActionCount() == 0:
                self.__runner.setFinishing(True)
            self.__runner.step()
            self.trace_raw += self.__runner.getLatestTrace()

    def run_to(self, t, silence=False):
        """
        Simulate to a future time step. If t >= current time step, the simulation will not be executed.
        :param silence: whether to collect traces
        :param t: the time step that the simulation will proceed to.
        """
        self.__runner.runTo(float(t))
        if not silence:
            self.trace_raw += self.__runner.getLatestTrace()

    def terminate(self):
        self.__runner.stop()
        self.__runner.cleanUpRun()
        self.__runner.cleanUpBatch()
        self.__gateway.shutdown()

    def get_tick_count(self):
        return self.__gateway.jvm.repast.simphony.engine.environment.RunEnvironment \
            .getInstance().getCurrentSchedule().getTickCount()

    def get_gateway(self):
        return self.__gateway

    def set_rs_dir(self, rs_dir):
        self.__rs_dir = rs_dir

    def update_params(self, kv_pair: dict):
        params_path = os.path.join(self.__rs_dir, "parameters.xml")
        params = ET.parse(params_path)
        root = params.getroot()
        for k, v in kv_pair.items():
            for param in root.findall('parameter'):
                if param.get('name') == k:
                    param.set('defaultValue', str(v))
        params.write(params_path, encoding='utf-8', xml_declaration=True)

    def get_traces(self):
        return self.__trace_loader.read_trace()

    def get_latest_trace(self):
        return self.__trace_loader.read_trace(self.__runner.getLatestTrace())

    def export_all_traces(self, path):
        print(len(self.trace_raw))
        with open(path, 'w') as f:
            f.write(self.trace_raw)
