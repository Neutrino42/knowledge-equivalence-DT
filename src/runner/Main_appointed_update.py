import getopt
import os
import sys
import copy
import numpy as np

import Loader
from Client import Client
from Comparator import Comparator
from SimServer import SimServer
import Util
from Config import Config
from datetime import datetime
import yaml
import random


def main(compare_method: str, human_seed: int, compare_window,
         tau=0, update_state_only=False, estimation_uncertainty=0.0, seed=3333, update_mode=None,
         init_time=1, update_time=1, duration=1000, ):
    """

    :param tau:
    :param compare_window:
    :param compare_method:
    :param theta:
    :param human_seed:
    :param verbose:
    :param k: for k-coverage
    :param update_mode: "clear_knowledge" or "keep_knowledge"
    :return:
    """
    # save parameters of this function
    func_params = copy.deepcopy(locals())

    # load configuration
    config = Config("config.yaml").data

    # save parameters of this function to a file
    os.makedirs(config["out_trace_dir"], exist_ok=True)
    with open(os.path.join(config["out_trace_dir"], 'parameters.yaml'), 'w') as f:
        yaml.dump(func_params, f, default_flow_style=False)

    # ------------------
    # read real trace ==
    # ------------------
    loader_real = Loader.TraceLoader(config["trace_real_path"])
    traces_real = loader_real.read_trace()
    time_real_list = [state["time"] for state in traces_real]
    init_scene = traces_real[time_real_list.index(init_time)]

    # export init scene
    init_scenario_path = os.path.join(config["out_scenario_dir"],
                                      'init_scenario{}.xml'.format(init_time))
    Util.export_XML_init_file(init_scene, init_scenario_path)

    # initialize the simulation server
    sim_server = SimServer(config["repast_jar_path"])
    sim_server.start()

    # initialize the simulation client
    # TODO: auto export init xml. Do not use both trace file and init xml file to initialise the simulator
    params = dict(
        randomSeed=seed,
        human_count=Loader.get_num_objs(traces_real[0]),
        camera_count=Loader.get_num_cams(traces_real[0]),
        update_knowledge=str(not update_state_only).lower(),
        init_scenario_path=init_scenario_path,
        output_trace_path=os.path.join(config["out_trace_dir"], "output_main.txt"),
        human_position_uncertainty=float(estimation_uncertainty),  # by default 0.0
        user_seed=human_seed
    )
    print(params)
    sim_client = Client(config["repast_rs"])
    sim_client.update_params(params)
    sim_client.load_and_init()

    # Record running parameters
    filename = "seed{}-compare_{}-human_seed{}.txt".format(seed, compare_method, human_seed)
    with open(os.path.join(config["out_trace_dir"], filename), 'w') as f:
        f.write('Create a new text file!')

    traces_pre = []
    try:
        sim_client.run_to(init_time, silence=True)
        traces_pre += sim_client.get_latest_trace()
        # TODO: 注意trace里第一秒是初始化，第二秒才开始sense-think-act-SEND_DATA

        # -----------------
        # Simulate to the update time to accumulate knowledge
        # -----------------
        for i in range(init_time, update_time):
            sim_client.step()
            traces_pre += sim_client.get_latest_trace()

        # -----------------
        # Update the simulator at `update_time'
        # -----------------
        # 1. export to a new init_scenario file
        # 2. update parameters.xml to point to that file
        # 3. reload simulator
        # 4. allow the simulator to run to the new starting time step
#        tmp_scenario_path = os.path.join(config["out_scenario_dir"],
#                                         'init_scenario{}.xml'.format(update_time))
#        if update_mode == "clear_knowledge":
#            print("clear knowledge when update")
#            state_tmp = copy.deepcopy(traces_real[time_real_list.index(update_time)])
#            for g in state_tmp["graph"]:
#                g['strength'] = 0.0
#            Util.export_XML_init_file(state_tmp, tmp_scenario_path)
#        elif update_mode == "keep_knowledge":
#            print("keep knowledge unchanged when update")
#            state_tmp = copy.deepcopy(traces_real[time_real_list.index(update_time)])
#            graph_tmp = copy.deepcopy(traces_pre[-1]["graph"])
#            state_tmp["graph"] = graph_tmp
#            Util.export_XML_init_file(state_tmp, tmp_scenario_path)
#        else:
#            Util.export_XML_init_file(traces_real[time_real_list.index(update_time)], tmp_scenario_path)
#        sim_client.update_params({"init_scenario_path": tmp_scenario_path})
#        sim_client.load_and_init()
#        sim_client.run_to(time_real_list.index(update_time), silence=True)

        # -----------------
        # Run `duration' time steps
        # -----------------
        for i in range(duration):
            sim_client.step()
            traces_pre += sim_client.get_latest_trace()

    except Exception as e:
        sim_client.terminate()
        sim_server.terminate()
        print(str(e))
        exit(-10)

    sim_client.terminate()
    sim_client.export_all_traces(os.path.join(config["out_trace_dir"], "output_main.txt"))
    sim_client.update_params({"init_scenario_path": config["init_scenario_path"]})  # restore to default init_scenario
    sim_server.terminate()

    # Calculate utility deviation
    traces_real_slice = traces_real[time_real_list.index(update_time): time_real_list.index(update_time + duration) + 1]
    comparator_util = Comparator("utility")
    distances_util = comparator_util.compare(traces_pre[-duration - 1:], traces_real_slice)
    distances_util = np.vstack(
        [time_real_list[time_real_list.index(update_time): time_real_list.index(update_time + duration) + 1],
         distances_util]).transpose()

    # write deviation record to file
    os.makedirs(config["out_statistics"], exist_ok=True)
    np.savetxt(os.path.join(config["out_statistics"], 'distances_utility.csv'),
               distances_util, delimiter=',', fmt="%f")


if __name__ == '__main__':
    main_seed_list = [1111, 2222, 4444, 5555, 6666, 7777,8888,9999,12345,67890]

    duration = 100  # run `duration' time steps and then stop simulation

    # generate random times by setting:     random.seed(42)
    random_times = [56, 94, 144, 149, 154, 209, 213, 270, 275, 320,
                    334, 334, 394, 398, 402, 417, 439, 479, 482, 509,
                    520, 653, 668, 764, 797, 827, 831, 875, 876, 878]

    for update_time in random_times:
        init_time = update_time - 50
        for update_mode in ["xxx"]:
            for seed in main_seed_list:
                main("position", 100, 1, estimation_uncertainty=0.0, seed=seed,
                     update_mode=update_mode, init_time=init_time, update_time=update_time, duration=duration)
