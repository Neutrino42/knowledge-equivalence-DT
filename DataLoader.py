import os
import xml.etree.ElementTree as ET
from collections import Counter
from xml.dom import minidom

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

from SimRunner import SimRunner


def _preprocess_trace(file_path):
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


def deprecated_export_XML_init_file(trace, out_file):
    """
    :param trace: {"time": 120.0, "cameras": "", "graph": "", "objs": ""}
    :return:
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

    # Init the structure of XML file
    root_xml = ET.Element('scenario', {'time': str(time)})
    cameras_xml = ET.SubElement(root_xml, 'cameras')
    graph_xml = ET.SubElement(root_xml, 'graph')
    uncovered_objects_xml = ET.SubElement(root_xml, 'uncovered_objects')

    # Load XML with each camera and its objects + messages
    for cam_traces in camera_list:
        cam_traces = cam_traces.replace("{", "")
        cam_traces = cam_traces.replace("}", "")
        trace_item = cam_traces.split(",")

        # Add camera info to XML
        cam_info = trace_item[0].split("|")
        cam_xml = ET.SubElement(cameras_xml, 'camera', {'id': cam_info[0], 'x': cam_info[1], 'y': cam_info[2]})

        # Add covered objects to XML
        num_objs = int(trace_item[2])
        objs_xml = ET.SubElement(cam_xml, 'objects')
        for i in range(3, 3 + num_objs):
            obj_xml = trace_item[i].split("|")  # example: 4|0.86|22.03|48|false|0
            ET.SubElement(objs_xml, 'object',
                          {'id': obj_xml[0], 'x': obj_xml[1], 'y': obj_xml[2],
                           'angle': obj_xml[3], 'is_important': obj_xml[4]})
        # Add messages to XML
        num_msg = int(trace_item[4 + num_objs])
        msgs_xml = ET.SubElement(cam_xml, 'messages')
        for i in range(-num_msg, 0):
            msg_xml = trace_item[i].split("|")  # example: 119.0|0|2
            ET.SubElement(msgs_xml, 'message',
                          {'time': msg_xml[0], 'camera_id': msg_xml[1], 'object_id': msg_xml[2]})

    # Load XML with each graph edge
    for edge_trace in edge_list:
        edge_trace = edge_trace.replace("{", "")
        edge_trace = edge_trace.replace("}", "")
        edge_xml = edge_trace.split("|")  # example: 0|1|0.000778
        ET.SubElement(graph_xml, 'edge',
                      {'source_id': edge_xml[0], 'target_id': edge_xml[1], 'strength': edge_xml[2]})

    # Load XML with each uncovered objects
    for uncovered_obj_trace in uncovered_obj_list:
        uncovered_obj_trace = uncovered_obj_trace.replace("{", "")
        uncovered_obj_trace = uncovered_obj_trace.replace("}", "")
        uncovered_obj_xml = uncovered_obj_trace.split("|")  # example: 0|18.00|3.00|0|true|3
        ET.SubElement(uncovered_objects_xml, 'object',
                      {'id': uncovered_obj_xml[0], 'x': uncovered_obj_xml[1], 'y': uncovered_obj_xml[2],
                       'angle': uncovered_obj_xml[3], 'is_important': uncovered_obj_xml[4]})

    ET.dump(root_xml)

    xmlstr = minidom.parseString(ET.tostring(root_xml, encoding='utf8')).toprettyxml(indent="    ")
    with open(out_file, 'wb') as f:
        f.write(xmlstr.encode('utf-8'))


def export_XML_init_file(state, out_file):
    """
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
                          dict(id=obj_id, x=str(obj_trace["x"]), y=str(obj_trace["y"]), angle=str(obj_trace["angle"]),
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
                           angle=str(uncovered_obj_trace["angle"]), is_important=uncovered_obj_trace["is_important"]))

    # ET.dump(root_xml)

    xmlstr = minidom.parseString(ET.tostring(root_xml, encoding='utf8')).toprettyxml(indent="    ")
    with open(out_file, 'wb') as f:
        f.write(xmlstr.encode('utf-8'))


def _parse_state_for_each_timestep(trace):
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


def read_trace(trace_path):
    tmp_traces = _preprocess_trace(trace_path)
    return [_parse_state_for_each_timestep(_state) for _state in tmp_traces]


def get_num_objs(state):
    cov_objs = []
    for cam in state["cameras"].values():
        obj_list = cam["objects"]
        cov_objs += obj_list
    cov_objs += state["objects"].keys()
    return len(set(cov_objs))


def calc_k_coverage_value(k, state):
    num_objs = get_num_objs(state)
    return len(filter_k_coverage(k, state)) / float(num_objs)


def filter_k_coverage(k, state):
    assert k >= 0
    coverage = calc_cov_for_objs(state)
    return {key: v for key, v in coverage.items() if v >= k}


def calc_cov_for_objs(state):
    """

    :param state:
    :return: a dict, indicating which object (id) has been covered by how many cameras
    {'objID': coverage}
    """
    cov_objs = []
    for cam in state["cameras"].values():
        obj_list = cam["objects"]
        cov_objs += obj_list
    return dict(Counter(cov_objs))


def get_all_covered_objects(state):
    cov_objs = {}
    for cam in state["cameras"].values():
        for obj_id, obj_content in cam["objects"].items():
            if cov_objs.get(str(obj_id)) is True:
                assert cov_objs.get(str(obj_id)) == obj_content["x"], obj_content["y"]
            else:
                cov_objs[str(obj_id)] = [obj_content["x"], obj_content["y"]]
    return cov_objs


def simple_distance(state_p, state_r):  # p for predicted and r for real
    # get all objects
    # store only the value [x,y] in the array, discarding id
    objs_r = get_all_covered_objects(state_r)
    sorted_objs_r = sorted(objs_r.items())
    objs_r_array = np.array([item[1] for item in sorted_objs_r])
    ids_r = [item[0] for item in sorted_objs_r]

    # find the covered real object ids in prediction trace
    objs_p = get_all_covered_objects(state_p)
    objs_p_array = []
    for i in ids_r:
        if objs_p.get(i):
            objs_p_array.append(objs_p.get(i))
        else:
            uncov_obj_p = state_p["objects"].get(i)
            assert uncov_obj_p is not None
            objs_p_array.append([uncov_obj_p["x"], uncov_obj_p["y"]])
    objs_p_array = np.array(objs_p_array)

    # read all cameras
    cams_r_array = []
    cams_p_array = []
    for cam_id, cam in state_r["cameras"].items():
        cams_r_array.append([cam["x"], cam["y"]])
        cam_p = state_p["cameras"].get(cam_id)
        cams_p_array.append([cam_p["x"], cam_p["y"]])
    cams_p_array = np.array(cams_p_array)
    cams_r_array = np.array(cams_r_array)

    p_array = np.concatenate([objs_p_array, cams_p_array])
    r_array = np.concatenate([objs_r_array, cams_r_array])
    return np.linalg.norm(p_array - r_array)


def knowledge_distance(k, state_1, state_2):
    knowledge_1 = calc_k_coverage_value(k, state_1)
    knowledge_2 = calc_k_coverage_value(k, state_2)
    return np.linalg.norm(np.array(knowledge_1) - np.array(knowledge_2))


def interaction_distance(state_p, state_r):
    edge_list_p = [[edge['source_id'], edge['target_id']] for edge in state_p["graph"]]
    edge_list_r = [[edge['source_id'], edge['target_id']] for edge in state_r["graph"]]
    assert edge_list_p == edge_list_r
    edge_array_p = [edge['strength'] for edge in state_p["graph"]]
    edge_array_r = [edge['strength'] for edge in state_r["graph"]]
    return np.linalg.norm(np.array(edge_array_p) - np.array(edge_array_r))


def local_goal_distance(state_chunk_p, state_chunk_r):
    cam_ids = list(state_chunk_p[0]["cameras"].keys())
    count_list_p = []
    for cam_id in cam_ids:
        count = 0
        for state_p in state_chunk_p:
            objects = state_p["cameras"].get(cam_id).get("objects")
            cov_count = sum([1 for obj in objects.values() if obj["is_important"].lower() == 'true'])
            if cov_count > 0:
                count += 1
        count_list_p.append(count)

    count_list_r = []
    for cam_id in cam_ids:
        count = 0
        for state_r in state_chunk_r:
            objects = state_r["cameras"].get(cam_id).get("objects")
            cov_count = sum([1 for obj in objects.values() if obj["is_important"].lower() == 'true'])
            if cov_count > 0:
                count += 1
        count_list_r.append(count)

    freq_array_r = np.array(count_list_r) / float(len(state_chunk_r))
    freq_array_p = np.array(count_list_p) / float(len(state_chunk_p))
    return np.linalg.norm(freq_array_p - freq_array_r)


def compare_simple(time_list_p: list, state_list_p: list, time_list_r: list, state_list_r: list):
    p_list, r_list, time_list, _, _, _, _ = get_common_parts(time_list_p, state_list_p, time_list_r, state_list_r)
    distances = [simple_distance(p, r) for p, r in zip(p_list, r_list)]
    return distances, time_list


def compare_interaction(time_list_p: list, state_list_p: list, time_list_r: list, state_list_r: list):
    p_list, r_list, time_list, _, _, _, _ = get_common_parts(time_list_p, state_list_p, time_list_r, state_list_r)
    distances = [interaction_distance(p, r) for p, r in zip(p_list, r_list)]
    return distances, time_list


def compare_global_goal(k: int, time_list_p: list, state_list_p: list, time_list_r: list, state_list_r: list):
    p_list, r_list, time_list, _, _, _, _ = get_common_parts(time_list_p, state_list_p, time_list_r, state_list_r)
    distances = [knowledge_distance(k, p, r) for p, r in zip(p_list, r_list)]
    return distances, time_list


def compare_local_goals(window, time_list_p, state_list_p, time_list_r, state_list_r: list):
    """
    calculate by a moving window
    only works well if we compare the entire trace (from time updateTime to endTime)
    :type state_list_r: list
    :param window:
    :param time_list_p:
    :param state_list_p:
    :param time_list_r:
    :param state_list_r: the full trace, from time 1 to endTime, each item is the state at that time step
    :return:
    """
    p_list, r_list, time_list, start_index_p, end_index_p, start_index_r, end_index_r = get_common_parts(
        time_list_p, state_list_p, time_list_r, state_list_r)
    assert window <= len(time_list)

    # concat a head list
    head_list = state_list_r[:start_index_r]

    augmented_p_list = head_list + p_list
    augmented_r_list = head_list + r_list
    assert len(augmented_r_list) == len(state_list_r[: end_index_r + 1])

    p_list_chunks = [augmented_p_list[max(0, i-window+1): i+1] for i in range(len(head_list), len(augmented_p_list))]
    r_list_chunks = [augmented_r_list[max(0, i-window+1): i+1] for i in range(len(head_list), len(augmented_r_list))]
    assert len(p_list_chunks) == len(time_list)
    assert len(r_list_chunks) == len(time_list)
    assert p_list_chunks[0][-1] == state_list_p[start_index_p]
    assert r_list_chunks[0][-1] == state_list_r[start_index_r]

    distances = []
    for p, r in zip(p_list_chunks, r_list_chunks):
        if len(p) < window:
            distances.append(0)
        else:
            distances.append(local_goal_distance(p, r))

    return distances, time_list


def get_common_parts(time_steps_1: list, list_1: list, time_steps_2: list, list_2: list):
    """
    find the common part of the two lists
    sequence 1: [ x x x x x x x x x x x]
    sequence 2:      [ x x x x x x x x x ]
    sequence 2:      [ x x x x ]

    :param time_steps_1: time steps of sequence 1, e.g. [3,4,5,6,7,...]
    :param list_1: value of each corresponding time step in time_steps_1
    :param time_steps_2: time steps of sequence 2, e.g. [7,8,9,10,...]
    :param list_2: value of each corresponding time step in time_steps_2
    :return: common part of the two lists, and the overlapping time list
    """

    start_time = max(time_steps_1[0], time_steps_2[0])
    end_time = min(time_steps_1[-1], time_steps_2[-1])

    start_index_1 = time_steps_1.index(start_time)
    start_index_2 = time_steps_2.index(start_time)
    end_index_1 = time_steps_1.index(end_time)
    end_index_2 = time_steps_2.index(end_time)

    list_1_trim = list_1[start_index_1: end_index_1 + 1]
    list_2_trim = list_2[start_index_2: end_index_2 + 1]
    time_steps_trim = time_steps_2[start_index_2: end_index_2 + 1]

    return list_1_trim, list_2_trim, time_steps_trim, start_index_1, end_index_1, start_index_2, end_index_2


def my_test():
    k = 2  # k for k-coverage

    # read real trace and calculate k-coverage for each time step
    trace_real_path = "/Users/Nann/eclipse-workspace/mobileCameras/trace/sample3333.txt"
    traces_real = read_trace(trace_real_path)
    time_real_list = [state["time"] for state in traces_real]
    knowledge_real_list = [calc_k_coverage_value(k, state) for state in traces_real]
    # print(knowledge_real_list)

    export_XML = False
    if export_XML:
        state = traces_real[0]
        export_XML_init_file(state, '/Users/Nann/eclipse-workspace/mobileCameras/trace/init_scenario.xml')

    # read prediction traces
    trace_pre_path = "/Users/Nann/eclipse-workspace/mobileCameras/trace/sample.txt"
    traces_pre = read_trace(trace_pre_path)
    time_pre_list = [state["time"] for state in traces_pre]
    knowledge_pre_list = [calc_k_coverage_value(k, state) for state in traces_pre]

    # ensure two traces has the same number of objects
    assert get_num_objs(traces_pre[0]) == get_num_objs(traces_real[0])

    # compare the position difference for all cameras and covered objects
    dists_simple, time_list_simple = compare_simple(time_pre_list, traces_pre, time_real_list, traces_real)

    # compare interaction
    dists_inter, time_list_inter = compare_interaction(time_pre_list, traces_pre, time_real_list, traces_real)

    # compare global knowledge trace with prediction
    dists_knowledge, time_list_knowledge = compare_global_goal(time_pre_list, knowledge_pre_list, time_real_list,
                                                               knowledge_real_list)

    # compare local goals
    dists_local_goals, time_local_goals = compare_local_goals(10, time_pre_list, traces_pre, time_real_list,
                                                              traces_real)

    plt.plot(np.array(time_list_simple), np.array(dists_simple))
    plt.show()
    plt.plot(np.array(time_list_knowledge), np.array(dists_knowledge))
    plt.show()
    plt.plot(np.array(time_list_inter), np.array(dists_inter))
    plt.show()
    plt.plot(np.array(time_local_goals), np.array(dists_local_goals))
    plt.show()


def eval_base_line(k, trace_real_path, xml_file_path, trace_pre_path):
    """

    :param int k: k for k-coverage
    :param trace_real_path:
    :param xml_file_path:
    :param trace_pre_path:
    :return:
    """

    # read real trace and calculate k-coverage for each time step
    traces_real = read_trace(trace_real_path)
    time_real_list = [state["time"] for state in traces_real]
    knowledge_real_list = [calc_k_coverage_value(k, state) for state in traces_real]

    # read prediction traces
    traces_pre = read_trace(trace_pre_path)
    time_pre_list = [state["time"] for state in traces_pre]
    knowledge_pre_list = [calc_k_coverage_value(k, state) for state in traces_pre]

    # ensure two traces has the same number of objects
    assert get_num_objs(traces_pre[0]) == get_num_objs(traces_real[0])

    # compare the position difference for all cameras and covered objects
    dists_simple, time_list_simple = compare_simple(time_pre_list, traces_pre, time_real_list, traces_real)

    # compare interaction
    dists_inter, time_list_inter = compare_interaction(time_pre_list, traces_pre, time_real_list, traces_real)

    # compare global knowledge trace with prediction
    dists_knowledge, time_list_knowledge = compare_global_goal(time_pre_list, knowledge_pre_list, time_real_list,
                                                               knowledge_real_list)

    # compare local goals
    dists_local_goals, time_local_goals = compare_local_goals(10, time_pre_list, traces_pre, time_real_list,
                                                              traces_real)


def modify_repast_params(file, name, value):
    tree = ET.parse(file)
    root = tree.getroot()
    for param in root.findall('parameter'):
        if param.get('name') == name:
            param.set('defaultValue', value)
    tree.write(file, encoding='utf-8', xml_declaration=True)


def find_deviation_time(time_list, dists_list, theta_baseline, final_end_time):
    # find the time when there is deviation
    deviation_time = None
    deviation_index = None
    for i in range(len(dists_list)):
        if dists_list[i] > theta_baseline:
            deviation_time = time_list[i]  # the value is a float
            deviation_index = i
            break
    assert time_list[-1] >= final_end_time
    if deviation_time is None:
        deviation_time = final_end_time
        deviation_index = time_list.index(deviation_time)
    return deviation_index, deviation_time


def main():
    k = 2  # k for k-coverage
    seed = 3333
    theta_baseline = 40
    start_time = 0
    final_end_time = 1000

    repast_param_file = "/Users/Nann/eclipse-workspace/mobileCameras/mobileCameras.rs/parameters.xml"

    base_dir = "/Users/Nann/eclipse-workspace/mobileCameras/trace/"
    trace_real_file = "sample{}.txt".format(seed)
    xml_file = 'init_scenario{}_0.xml'.format(seed)

    trace_real_path = base_dir + trace_real_file
    xml_file_path = base_dir + xml_file

    # Assume we already have a real trace, but no prediction trace
    # At first, generate init XML file for simulator to make prediction
    traces_real = read_trace(trace_real_path)
    export_XML_init_file(traces_real[0], xml_file_path)

    # read real trace
    time_real_list = [state["time"] for state in traces_real]

    # initialize the simulation runner
    repast_jar_path = "/Users/Nann/eclipse-workspace/mobileCameras/runnable_jar/mobileCameras.jar"
    runner = SimRunner(repast_jar_path)

    # record for deviation time step
    record = []

    time_list_archive = []
    dists_list_archive = []
    dists_knowledge_list_archive = []
    dists_interaction_list_archive = []
    dists_lg_list_archive = []

    while start_time < final_end_time:
        xml_file = 'init_scenario{}_{}.xml'.format(seed, start_time)
        trace_pre_file = 'prediction/sample{}_{}.txt'.format(seed, start_time)

        xml_file_path = base_dir + xml_file
        trace_pre_path = base_dir + trace_pre_file

        # modify the init settings of Repast
        modify_repast_params(repast_param_file, 'init_scenario_path', xml_file_path)
        modify_repast_params(repast_param_file, 'output_trace_path', trace_pre_path)

        # ---------------
        # load XML to simulator
        # ---------------
        # prompt = ("Last simulation ends at: {}\n"
        #          "Please modify Repast parameters.xml as follows first, then press any key to continue: \n"
        #          "a. change xml init path to:                   {}\n"
        #          "b. change prediction output file to:          {}\n"
        #          "c. change scheduling time tick starting from: {}\n"
        #          "d. change seeding in Repast GUI as:           {}\n"
        #          "e. run simulation\n"
        #          ).format(start_time, xml_file, trace_pre_file, start_time, seed)
        # input(prompt)

        runner.run()

        # ------------------
        # read prediction traces, and read real traces:
        # ------------------
        traces_pre = read_trace(trace_pre_path)  # [{}, {}, {} ...]
        time_pre_list = [state["time"] for state in traces_pre]

        # DEBUG: ensure two traces has the same number of objects
        assert get_num_objs(traces_pre[0]) == get_num_objs(traces_real[0])

        # ------------------
        # baseline comparison
        # ------------------
        # compare prediction, get the distance
        dists_simple, time_list = compare_simple(time_pre_list, traces_pre, time_real_list, traces_real)
        dists_knowledge, _ = compare_global_goal(k, time_pre_list, traces_pre, time_real_list, traces_real)
        dists_interaction, _ = compare_interaction(time_pre_list, traces_pre, time_real_list, traces_real)
        dists_lg, _ = compare_local_goals(10, time_pre_list, traces_pre, time_real_list, traces_real)

        # find the deviation time step
        deviation_index, deviation_time = find_deviation_time(time_list, dists_simple, theta_baseline,
                                                              final_end_time)

        # get the real state at this deviation time step
        state = traces_real[int(deviation_time - 1)]
        assert state["time"] == deviation_time

        # export state at this time to XML file
        export_XML = True
        if export_XML:
            xml_file = 'init_scenario{}_{}.xml'.format(seed, int(deviation_time))
            xml_file_path = base_dir + xml_file
            export_XML_init_file(state, xml_file_path)

        # write distances to file
        os.makedirs("./result/baseline", exist_ok=True)
        export_array = np.vstack([time_list, dists_simple]).transpose()
        np.savetxt("./result/baseline/distances_raw{}_{}.csv".format(seed, int(deviation_time)),
                   export_array, delimiter=',', fmt='%d, %f')
        np.savetxt("./result/baseline/distances_sliced{}_{}.csv".format(seed, int(deviation_time)),
                   export_array[:deviation_index, :], delimiter=',', fmt='%d, %f')

        os.makedirs("./result/global_goal", exist_ok=True)
        export_knowledge_array = np.vstack([time_list, dists_knowledge]).transpose()
        np.savetxt("./result/global_goal/distances_knowledge_raw{}_{}.csv".format(seed, int(deviation_time)),
                   export_knowledge_array, delimiter=',', fmt='%d, %f')
        np.savetxt("./result/global_goal/distances_knowledge_sliced{}_{}.csv".format(seed, int(deviation_time)),
                   export_knowledge_array[:deviation_index, :], delimiter=',', fmt='%d, %f')

        os.makedirs("./result/interaction", exist_ok=True)
        export_interaction_array = np.vstack([time_list, dists_interaction]).transpose()
        np.savetxt("./result/interaction/distances_interaction_raw{}_{}.csv".format(seed, int(deviation_time)),
                   export_interaction_array, delimiter=',', fmt='%d, %f')
        np.savetxt("./result/interaction/distances_interaction_sliced{}_{}.csv".format(seed, int(deviation_time)),
                   export_interaction_array[:deviation_index, :], delimiter=',', fmt='%d, %f')

        os.makedirs("./result/local_goals", exist_ok=True)
        export_lg_array = np.vstack([time_list, dists_lg]).transpose()
        np.savetxt("./result/local_goals/distances_lg_raw{}_{}.csv".format(seed, int(deviation_time)),
                   export_lg_array, delimiter=',', fmt='%d, %f')
        np.savetxt("./result/local_goals/distances_lg_sliced{}_{}.csv".format(seed, int(deviation_time)),
                   export_lg_array[:deviation_index, :], delimiter=',', fmt='%d, %f')

        # record history for plotting
        time_list_archive += time_list[:deviation_index]
        dists_list_archive += dists_simple[:deviation_index]
        dists_knowledge_list_archive += dists_knowledge[:deviation_index]
        dists_interaction_list_archive += dists_interaction[:deviation_index]
        dists_lg_list_archive += dists_lg[:deviation_index]
        record.append(deviation_time)

        start_time = deviation_time

    plt.plot(np.array(time_list_archive), np.array(dists_list_archive))
    plt.title("baseline")
    plt.savefig("./result/distance_plots{}.pdf".format(seed))
    plt.show()

    plt.plot(np.array(time_list_archive), np.array(dists_knowledge_list_archive))
    plt.title("global knowledge")
    plt.savefig("./result/distance_knowledge_plots{}.pdf".format(seed))
    plt.show()

    plt.plot(np.array(time_list_archive), np.array(dists_interaction_list_archive))
    plt.title("interaction")
    plt.savefig("./result/distance_interaction_plots{}.pdf".format(seed))
    plt.show()

    plt.plot(np.array(time_list_archive), np.array(dists_lg_list_archive))
    plt.title("local goals")
    plt.savefig("./result/distance_lg_plots{}.pdf".format(seed))
    plt.show()

    # write deviation record to file
    dev_file = './result/deviation_record{}.csv'.format(seed)
    with open(dev_file, 'w+') as f:
        f.write(','.join(map(str, record)) + '\n')


if __name__ == '__main__':
    main()
