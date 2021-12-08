import xml.etree.ElementTree as ET
from xml.dom import minidom
import os


def export_XML_init_file(state, out_file):
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

    # write to file
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'wb') as f:
        f.write(xmlstr.encode('utf-8'))
