import getopt
import os
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from xml.dom import minidom

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

from SimRunner import SimRunner
from Loader import Loader


def get_num_objs(state):
    cov_objs = []
    for cam in state["cameras"].values():
        obj_list = cam["objects"]
        cov_objs += obj_list
    cov_objs += state["objects"].keys()
    return len(set(cov_objs))


def get_num_cams(state):
    return len(state["cameras"])


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


def position_distance(state_p, state_r):  # p for predicted and r for real
    # store only the value [x,y] in the array, discarding id

    # read all cameras
    cams_r_array = []
    cams_p_array = []
    for cam_id, cam in state_r["cameras"].items():
        cams_r_array.append([cam["x"], cam["y"]])
        cam_p = state_p["cameras"].get(cam_id)
        cams_p_array.append([cam_p["x"], cam_p["y"]])
    cams_p_array = np.array(cams_p_array)
    cams_r_array = np.array(cams_r_array)

    # get all objects
    objs_r = get_all_covered_objects(state_r)
    if len(objs_r) != 0:
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

        p_array = np.concatenate([objs_p_array, cams_p_array])
        r_array = np.concatenate([objs_r_array, cams_r_array])
    else:
        p_array = cams_p_array
        r_array = cams_r_array
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


def compare_position(time_list_p: list, state_list_p: list, time_list_r: list, state_list_r: list):
    p_list, r_list, time_list, _, _, _, _ = get_common_parts(time_list_p, state_list_p, time_list_r, state_list_r)
    distances = [position_distance(p, r) for p, r in zip(p_list, r_list)]
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

    # concat a head list
    head_list = state_list_r[:start_index_r]

    augmented_p_list = head_list + p_list
    augmented_r_list = head_list + r_list
    assert len(augmented_r_list) == len(state_list_r[: end_index_r + 1])

    p_list_chunks = [augmented_p_list[max(0, i - window + 1): i + 1] for i in
                     range(len(head_list), len(augmented_p_list))]
    r_list_chunks = [augmented_r_list[max(0, i - window + 1): i + 1] for i in
                     range(len(head_list), len(augmented_r_list))]
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


def compare_by(_compare_method, time_pre_list, traces_pre, time_real_list, traces_real, final_end_time, _theta, _tau,
               _k=2):
    # find the deviation time step
    if _compare_method == "position" or _compare_method == "position-p" or _compare_method == "position-k":
        dists, time_list = compare_position(time_pre_list, traces_pre, time_real_list, traces_real)
    elif _compare_method == "interaction":
        dists, time_list = compare_interaction(time_pre_list, traces_pre, time_real_list, traces_real)
    elif _compare_method == "local_goals":
        dists, time_list = compare_local_goals(10, time_pre_list, traces_pre, time_real_list, traces_real)
    elif _compare_method == "global_goals":
        dists, time_list = compare_global_goal(_k, time_pre_list, traces_pre, time_real_list, traces_real)
    else:
        exit(-1)

    deviation_index, deviation_time = find_deviation_time(time_list, dists, _theta, final_end_time, _tau)

    state = traces_real[int(deviation_time - 1)]
    assert state["time"] == deviation_time

    return state, deviation_index, deviation_time


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


def find_deviation_time(time_list, dists_list, _theta, final_end_time, _tau):
    # find the time when there is deviation
    deviation_time = None
    deviation_index = None
    assert (_tau >= 0)
    count = 0

    # regard it as a deviation only when distance has been larger than _theta for _tau CONSECUTIVE times
    for i in range(len(dists_list)):
        if dists_list[i] > _theta:
            count += 1
        else:
            count = 0

        # check _tau criteria
        if count > _tau:
            deviation_time = time_list[i]  # the value is a float
            deviation_index = i
            break

    if deviation_time is None:
        deviation_time = final_end_time
        deviation_index = time_list.index(deviation_time)
    return deviation_index, deviation_time


def main(compare_method: str, theta, human_seed: int, verbose: bool, k, compare_window,
         tau=0, update_state_only=False, estimation_uncertainty=0.0, quiet_mode=False):
    """

    :param tau:
    :param compare_window:
    :param compare_method:
    :param theta:
    :param human_seed:
    :param verbose:
    :param k: for k-coverage
    :return:
    """
    seed = 3333
    start_time = 0
    final_end_time = 1000
    result_dir = "./result/seed{}/compare_{}/threshold{}_{}/human_seed{}/".format(seed, compare_method, theta, tau,
                                                                                  human_seed)

    repast_dir = "../simulator/"
    repast_jar_path = repast_dir + "runnable_jar/mobileCameras.jar"

    trace_dir = repast_dir + "trace/"
    trace_real_file = "sample{}_999.txt".format(seed)
    trace_real_path = trace_dir + trace_real_file

    # Export path for xml init file
    xml_file = 'init_scenario{}_{}_0.xml'.format(seed, human_seed)
    trace_pre_dir = trace_dir + 'prediction/seed{}/compare_{}/threshold{}_{}/human_seed{}/'.format(
        seed, compare_method, theta, tau, human_seed)
    xml_path = trace_pre_dir + xml_file
    os.makedirs(trace_pre_dir, exist_ok=True)

    # Assume we already have a real trace, but no prediction trace
    # At first, generate init XML file for simulator to make prediction
    loader = Loader(repast_dir)
    traces_real = loader.read_trace(trace_real_path)
    loader.export_XML_init_file(traces_real[0], xml_path)

    # read real trace
    time_real_list = [state["time"] for state in traces_real]

    # initialize the simulation runner
    runner = SimRunner(repast_jar_path, repast_dir)

    # initialize simulator parameters
    runner.modify_repast_params('human_count', get_num_objs(traces_real[0]))  # number of humans/objects
    runner.modify_repast_params('camera_count', get_num_cams(traces_real[0]))  # number of cameras
    runner.modify_repast_params('update_knowledge', str(not update_state_only).lower())  # whether to update knowledge
    if estimation_uncertainty > 0:  # position uncertainty of human when estimating
        runner.modify_repast_params('human_position_uncertainty', estimation_uncertainty)

    # record for deviation time step
    deviation_record = []

    time_list_archive = []
    dists_list_archive = []
    dists_knowledge_list_archive = []
    dists_interaction_list_archive = []
    dists_lg_list_archive = []

    while start_time < final_end_time:
        # set output trace_pre path
        trace_pre_file = 'sample{}_{}_{}.txt'.format(seed, human_seed, start_time)
        trace_pre_path = trace_pre_dir + trace_pre_file

        # modify the init settings of Repast
        runner.modify_repast_params('init_scenario_path', xml_path)
        runner.modify_repast_params('output_trace_path', trace_pre_path)
        runner.modify_repast_params('user_seed', human_seed)

        runner.run()

        # read prediction traces, and read real traces:
        traces_pre = loader.read_trace(trace_pre_path)  # [{}, {}, {} ...]
        traces_pre = traces_pre[:compare_window]
        time_pre_list = [state["time"] for state in traces_pre]
        # DEBUG: ensure two traces has the same number of objects
        assert get_num_objs(traces_pre[0]) == get_num_objs(traces_real[0])

        # compare to find deviation time and state
        state, deviation_index, deviation_time = compare_by(compare_method, time_pre_list, traces_pre,
                                                            time_real_list, traces_real, final_end_time, theta, tau, k)

        # export state at this time to XML file for the next round simulation
        xml_file = 'init_scenario{}_{}_{}.xml'.format(seed, human_seed, int(deviation_time))
        xml_path = trace_pre_dir + xml_file
        loader.export_XML_init_file(state, xml_path)

        # calculate performance metrics on distances
        dists_knowledge, time_list = compare_global_goal(k, time_pre_list, traces_pre, time_real_list, traces_real)
        dists_simple, _ = compare_position(time_pre_list, traces_pre, time_real_list, traces_real)
        dists_interaction, _ = compare_interaction(time_pre_list, traces_pre, time_real_list, traces_real)
        dists_lg, _ = compare_local_goals(10, time_pre_list, traces_pre, time_real_list, traces_real)

        # write performance metrics (distances) to files
        os.makedirs(result_dir + "distances", exist_ok=True)
        if not quiet_mode:
            export_array = np.vstack([time_list,
                                      dists_simple,
                                      dists_knowledge,
                                      dists_interaction,
                                      dists_lg]).transpose()
            np.savetxt(result_dir + "distances/distances_raw{}_{}_{}.csv".format(seed, human_seed, int(deviation_time)),
                       export_array, delimiter=',', fmt='%d,%f,%f,%f,%f',
                       header="time,position,global_goal,interaction,local_goals")
            np.savetxt(result_dir + "distances/distances_sliced{}_{}_{}.csv".format(seed, human_seed, int(deviation_time)),
                       export_array[:deviation_index, :], delimiter=',', fmt='%d,%f,%f,%f,%f',
                       header="time,position,global_goal,interaction,local_goals")

        # record history for plotting
        time_list_archive += time_list[:deviation_index]
        dists_list_archive += dists_simple[:deviation_index]
        dists_knowledge_list_archive += dists_knowledge[:deviation_index]
        dists_interaction_list_archive += dists_interaction[:deviation_index]
        dists_lg_list_archive += dists_lg[:deviation_index]
        deviation_record.append(deviation_time)

        start_time = deviation_time

    plt.plot(np.array(time_list_archive), np.array(dists_list_archive))
    plt.title("position")
    plt.savefig(result_dir + "distance_plots{}_{}.pdf".format(seed, human_seed))
    plt.close("all")

    plt.plot(np.array(time_list_archive), np.array(dists_knowledge_list_archive))
    plt.title("global knowledge")
    plt.savefig(result_dir + "distance_knowledge_plots{}_{}.pdf".format(seed, human_seed))
    plt.close("all")

    plt.plot(np.array(time_list_archive), np.array(dists_interaction_list_archive))
    plt.title("interaction")
    plt.savefig(result_dir + "distance_interaction_plots{}_{}.pdf".format(seed, human_seed))
    plt.close("all")

    plt.plot(np.array(time_list_archive), np.array(dists_lg_list_archive))
    plt.title("local goals")
    plt.savefig(result_dir + "distance_lg_plots{}_{}.pdf".format(seed, human_seed))
    plt.close("all")

    # write deviation record to file
    dev_file = result_dir + 'deviation_record{}_{}.csv'.format(seed, human_seed)
    with open(dev_file, 'w+') as f:
        f.write(','.join(map(str, deviation_record)) + '\n')

    all_archive = np.vstack([time_list_archive,
                             dists_list_archive,
                             dists_knowledge_list_archive,
                             dists_interaction_list_archive,
                             dists_lg_list_archive]).transpose()
    np.savetxt(result_dir + "all_distances_{}_{}.csv".format(seed, human_seed), all_archive,
               delimiter=',', fmt='%d,%f,%f,%f,%f', header="time,position,global_goal,interaction,local_goals")


if __name__ == '__main__':
    # default values
    compare_window = 1000
    theta_list = [80, 85, 70, 65, 60, 55, 50, 45, 40, 35, 30]
    human_seed_list = list(range(100, 1001, 100))  # real trace is obtained by setting human_seed = 999
    compare_method_list = ["position", "position-k", "position-p", "interaction", "local_goals", "global_goals"]
    compare_method = compare_method_list[1]
    verbose = True
    k = 2  # k for k-coverage
    tau = 0
    update_state_only = False
    # TODO: here it's a bit tricky to have this variable of "update_state_only" rather than "update_knowledge"
    # TODO: The reason is to be compatible with previous version of this file
    # TODO: future work can try to modify this variable in the simulator jar file
    estimation_uncertainty = 0
    quiet_mode = False  # reduce unnecessary output logs

    # parsing cli arguments
    argument_list = sys.argv[1:]
    options = "t:a:s:c:w:e:uqh"
    long_options = ["theta =", "tau =", "seed =", "compare =", "window =", "estimation_uncertainty =",
                    "update_state_only", "quiet", "help"]
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        if len(arguments) == 0:
            print("error: please specify cli arguments, use -h to check help")
            exit(-3)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-t", "--theta"):
                currentValue.replace(" ", "")
                theta_list = list(map(lambda v: int(v) if '.' not in v else float(v), currentValue.split(",")))

            elif currentArgument in ("-a", "--tau"):
                currentValue.replace(" ", "")
                tau = int(currentValue)

            elif currentArgument in ("-s", "--seed"):
                currentValue.replace(" ", "")
                human_seed_list = list(map(int, currentValue.split(",")))

            elif currentArgument in ("-w", "--window"):
                currentValue.replace(" ", "")
                compare_window = int(currentValue)

            elif currentArgument in ("-c", "--compare"):
                compare_method = currentValue.strip()
                if compare_method not in compare_method_list:
                    print("error: compare method must be one of the following:")
                    print(compare_method_list)
                    exit(-2)

            elif currentArgument in ("-u", "--update_state_only"):
                update_state_only = True

            elif currentArgument in ("-q", "--quiet"):
                quiet_mode = True

            elif currentArgument in ("-e", "--estimation_uncertainty"):
                currentValue.replace(" ", "")
                estimation_uncertainty = float(currentValue)

            elif currentArgument in ("-h", "--help"):
                print("Usage: python3 Main.py -t <threshold-list> -t <tau value> -s <seed-list> -c <compare-method> "
                      "-w <compare-window> -e <estimation-uncertainty>")
                print("Example: python3 Main.py -t '30,40,50' -a 1 -s '100,200' -c position -w 100")
                exit(-4)
    except getopt.error as err:
        print(str(err))
        exit(-1)

    print("threshold values:")
    print(theta_list)
    print("tau value:")
    print(tau)
    print("human seed values:")
    print(human_seed_list)
    print("compare by:")
    print(compare_method)
    print("compare window:")
    print(compare_window)

    for theta in theta_list:
        for human_seed in human_seed_list:
            print(compare_method, theta, human_seed, tau)
            main(compare_method, theta, human_seed, verbose, k, compare_window,
                 tau=tau, update_state_only=update_state_only, estimation_uncertainty=estimation_uncertainty,
                 quiet_mode=quiet_mode)
