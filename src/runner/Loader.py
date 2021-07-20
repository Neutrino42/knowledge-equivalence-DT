import xml.etree.ElementTree as ET
from xml.dom import minidom


class Loader(object):

    def __init__(self, repast_dir):
        self.__repast_dir = repast_dir

    def _parse_state_for_each_timestep(self, trace):
        """
        :param trace:
            the trace for a single time step
            {"time": 120.0, "cameras": "", "graph": "", "objs": ""}
        :return: dict state = {"time": int, "cameras": {}, "graph": [], "objects": {}}
        """

        time = trace["time"]
        camera_list = trace["cameras"]
        # camera_list = ["{0|0.66|21.39},objs,2,{4|0.86|22.03|48|false|0},{2|4.00|25.00|90|true|2},msg,0",
        #               "{3|25.51|49.67},objs,1,{3|28.34|43.74|149|true|23},msg,2,{119.0|0|2},{120.0|0|2}"]
        edge_list = trace["graph"]
        # edge_list = ["{0|1|0.000778}",
        #             "{0|2|0.000586}",
        #             "{0|3|0.001327}"]
        uncovered_obj_list = trace["objs"]
        # uncovered_obj_list = ["{0|18.00|3.00|0|true|3}",
        #                      "{1|18.00|10.00|0|false|0}"]

        state = dict(time=time, cameras={}, graph=[], objects={})

        # Load each camera and its objects + messages
        for cam_traces in camera_list:
            cam_traces = cam_traces.replace("{", "")
            cam_traces = cam_traces.replace("}", "")
            trace_item = cam_traces.split(",")

            # Add this camera info
            cam_info = trace_item[0].split("|")
            cam_id = cam_info[0]
            state["cameras"][cam_id] = dict(x=float(cam_info[1]), y=float(cam_info[2]), objects={}, messages=[])

            # Add covered objects
            num_objs = int(trace_item[2])
            this_cam = state["cameras"][cam_id]
            for i in range(3, 3 + num_objs):
                obj_xml = trace_item[i].split("|")  # example: 4|0.86|22.03|48|false|0
                obj_id = obj_xml[0]
                this_cam["objects"][obj_id] = dict(x=float(obj_xml[1]), y=float(obj_xml[2]), angle=int(obj_xml[3]),
                                                   is_important=obj_xml[4], duration=int(obj_xml[5]))

            # Add messages
            num_msg = int(trace_item[4 + num_objs])
            for i in range(-num_msg, 0):
                msg_xml = trace_item[i].split("|")  # example: 119.0|0|2
                this_cam["messages"].append(
                    dict(time=float(msg_xml[0]), camera_id=int(msg_xml[1]), object_id=int(msg_xml[2])))

        # Load each graph edge
        for edge_trace in edge_list:
            edge_trace = edge_trace.replace("{", "")
            edge_trace = edge_trace.replace("}", "")
            edge_xml = edge_trace.split("|")  # example: 0|1|0.000778
            state["graph"].append(dict(source_id=int(edge_xml[0]), target_id=int(edge_xml[1]), strength=float(edge_xml[2])))

        # Load each uncovered objects
        for uncovered_obj_trace in uncovered_obj_list:
            uncovered_obj_trace = uncovered_obj_trace.replace("{", "")
            uncovered_obj_trace = uncovered_obj_trace.replace("}", "")
            uncovered_obj_xml = uncovered_obj_trace.split("|")  # example: 0|18.00|3.00|0|true|3
            obj_id = uncovered_obj_xml[0]
            state["objects"][obj_id] = dict(x=float(uncovered_obj_xml[1]), y=float(uncovered_obj_xml[2]),
                                            angle=int(uncovered_obj_xml[3]), is_important=uncovered_obj_xml[4],
                                            duration=int(uncovered_obj_xml[5]))
        return state

    def read_trace(self, trace_path):
        tmp_traces = self._preprocess_trace(trace_path)
        return [self._parse_state_for_each_timestep(_state) for _state in tmp_traces]

    def _preprocess_trace(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

            start_time = lines[0].split(",")[0]
            time = start_time
            traces = []
            camera_list = []
            edge_list = []
            uncovered_obj_list = []
            for line in lines:
                line = line.strip()

                if not line:
                    # skip empty lines (this may only happen at the end of the file)
                    continue

                line_items = line.split(",")
                if line_items[0] != time:
                    trace_item = {"time": int(float(time)),
                                  "cameras": camera_list,
                                  "graph": edge_list,
                                  "objs": uncovered_obj_list}
                    traces.append(trace_item)
                    time = line_items[0]
                    camera_list = []
                    edge_list = []
                    uncovered_obj_list = []

                if line_items[1] == "cam":
                    camera_list.append(line.split(",", 2)[-1])
                elif line_items[1] == "graph":
                    edge_list = line_items[2:]
                elif line_items[1] == "objs":
                    uncovered_obj_list = line_items[3:]

            trace_item = {"time": int(float(time)),
                          "cameras": camera_list,
                          "graph": edge_list,
                          "objs": uncovered_obj_list}
            traces.append(trace_item)

            return traces

    def export_XML_init_file(self, state, out_file):
        """
        :param out_file:
        :param state: {"time": 120.0, "cameras": "", "graph": "", "objs": ""}
        :return:
        """

        time = state["time"]
        camera_list = state["cameras"]
        edge_list = state["graph"]
        uncovered_obj_list = state["objects"]

        # Init the structure of XML file
        root_xml = ET.Element('scenario', {'time': str(time)})
        cameras_xml = ET.SubElement(root_xml, 'cameras')
        graph_xml = ET.SubElement(root_xml, 'graph')
        uncovered_objects_xml = ET.SubElement(root_xml, 'uncovered_objects')

        # Load XML with each camera and its objects + messages
        for cam_id, cam_trace in camera_list.items():

            # Add camera info to XML
            cam_xml = ET.SubElement(cameras_xml, 'camera',
                                    dict(id=cam_id, x=str(cam_trace["x"]), y=str(cam_trace["y"])))

            # Add covered objects to XML
            objs_xml = ET.SubElement(cam_xml, 'objects')
            for obj_id, obj_trace in cam_trace["objects"].items():
                ET.SubElement(objs_xml, 'object',
                              dict(id=obj_id, x=str(obj_trace["x"]), y=str(obj_trace["y"]),
                                   angle=str(obj_trace["angle"]),
                                   is_important=obj_trace["is_important"]))
            # Add messages to XML
            msgs_xml = ET.SubElement(cam_xml, 'messages')
            for msg_trace in cam_trace["messages"]:
                ET.SubElement(msgs_xml, 'message',
                              dict(time=str(int(msg_trace["time"])), camera_id=str(msg_trace["camera_id"]),
                                   object_id=str(msg_trace["object_id"])))

        # Load XML with each graph edge
        for edge_trace in edge_list:
            ET.SubElement(graph_xml, 'edge',
                          dict(source_id=str(edge_trace["source_id"]), target_id=str(edge_trace["target_id"]),
                               strength=str(edge_trace["strength"])))

        # Load XML with each uncovered objects
        for uncov_obj_id, uncovered_obj_trace in uncovered_obj_list.items():
            ET.SubElement(uncovered_objects_xml, 'object',
                          dict(id=uncov_obj_id, x=str(uncovered_obj_trace["x"]), y=str(uncovered_obj_trace["y"]),
                               angle=str(uncovered_obj_trace["angle"]),
                               is_important=uncovered_obj_trace["is_important"]))

        # ET.dump(root_xml)

        xmlstr = minidom.parseString(ET.tostring(root_xml, encoding='utf8')).toprettyxml(indent="    ")
        with open(out_file, 'wb') as f:
            f.write(xmlstr.encode('utf-8'))


