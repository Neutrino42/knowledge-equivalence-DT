import io


def get_all_covered_objects(state):
    cov_objs = {}
    for cam in state["cameras"].values():
        for obj_id, obj_content in cam["objects"].items():
            if cov_objs.get(str(obj_id)) is True:
                assert cov_objs.get(str(obj_id)) == obj_content["x"], obj_content["y"]
            else:
                cov_objs[str(obj_id)] = [obj_content["x"], obj_content["y"]]
    return cov_objs


def get_num_cams(state):
    return len(state["cameras"])


def get_num_objs(state):
    cov_objs = []
    for cam in state["cameras"].values():
        obj_list = cam["objects"]
        cov_objs += obj_list
    cov_objs += state["objects"].keys()
    return len(set(cov_objs))


class TraceLoader(object):

    def __init__(self, trace_path):
        self.__trace_path = trace_path

    def set_trace_path(self, trace_path):
        self.__trace_path = trace_path

    def _parse_state_for_each_timestep(self, trace):
        """
        :param trace:
            the trace for a single time step
            {"time": 120.0, "cameras": "", "graph": "", "objs": ""}
        :return: dict state = {"time": int, "cameras": {}, "graph": [], "objects": {}}
        """

        time = trace["time"]
        camera_list = trace["cameras"]
        # camera_list = ["{0|0.66|21.39},objs,2,{4|0.86|22.03|48|false|0},{2|4.00|25.00|90|true|2},msg,0,act,{n|6|8|f|9}",
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
            state["cameras"][cam_id] = dict(x=float(cam_info[1]), y=float(cam_info[2]), objects={}, messages=[],
                                            actions={})

            # Add covered objects
            num_objs = int(trace_item[2])
            this_cam = state["cameras"][cam_id]
            for i in range(3, 3 + num_objs):
                obj_xml = trace_item[i].split("|")  # example: 4|0.86|22.03|48|false|0
                obj_id = obj_xml[0]
                this_cam["objects"][obj_id] = dict(x=float(obj_xml[1]), y=float(obj_xml[2]), angle=int(obj_xml[3]),
                                                   is_important=obj_xml[4], duration=int(obj_xml[5]))

            # Add messages
            index = trace_item.index("msg")
            num_msg = int(trace_item[index + 1])
            for i in range(num_msg):
                msg_xml = trace_item[i + (index + 2)].split("|")  # example: 119.0|0|2
                this_cam["messages"].append(
                    dict(time=float(msg_xml[0]), camera_id=int(msg_xml[1]), object_id=int(msg_xml[2])))

            # Add actions
            if "act" in trace_item:
                index = trace_item.index("act")
                notify = []
                follow = -1
                respond = -1
                random = -1
                action_info = trace_item[index + 1].split("|")
                if action_info[0] == "n":
                    index_f = action_info.index("f")
                    notify = [int(j) for j in action_info[1:index_f]]
                    follow = int(action_info[index_f + 1])
                elif action_info[0] == "f":
                    follow = int(action_info[1])
                elif action_info[0] == "re":
                    respond = int(action_info[1])
                    follow = int(action_info[2])
                elif action_info[0] == "rand":
                    random = 1
                this_cam["actions"] = dict(notify=notify, follow=follow, respond=respond, random=random)

        # Load each graph edge
        for edge_trace in edge_list:
            edge_trace = edge_trace.replace("{", "")
            edge_trace = edge_trace.replace("}", "")
            edge_xml = edge_trace.split("|")  # example: 0|1|0.000778
            state["graph"].append(
                dict(source_id=int(edge_xml[0]), target_id=int(edge_xml[1]), strength=float(edge_xml[2])))

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

    def read_trace(self, my_string=None):
        if my_string is None:
            with open(self.__trace_path, 'r') as f:
                tmp_traces = self._preprocess_trace(f)
                return [self._parse_state_for_each_timestep(_state) for _state in tmp_traces]
        else:
            tmp_traces = self._preprocess_trace(io.StringIO(my_string))
            return [self._parse_state_for_each_timestep(_state) for _state in tmp_traces]

    def _preprocess_trace(self, f):
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
