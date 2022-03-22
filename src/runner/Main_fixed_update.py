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


def main(compare_method: str, theta, human_seed: int, compare_window,
         tau=0, update_state_only=False, estimation_uncertainty=0.0, seed=3333, update_mode=None, frequency=30):
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

    # load configuration
    config = Config("config.yaml").data

    # ------------------
    # read real trace ==
    # ------------------
    loader_real = Loader.TraceLoader(config["trace_real_path"])
    traces_real = loader_real.read_trace()
    time_real_list = [state["time"] for state in traces_real]

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
        init_scenario_path=config["init_scenario_path"],
        output_trace_path=os.path.join(config["out_trace_dir"], "output_main.txt"),
        human_position_uncertainty=float(estimation_uncertainty),  # by default 0.0
        user_seed=human_seed
    )
    print(params)
    sim_client = Client(config["repast_rs"])
    sim_client.update_params(params)
    sim_client.load_and_init()

    # init comparator
    comparator = Comparator(compare_method)

    # Record running parameters
    filename = "seed{}-compare_{}-threshold{}_{}-human_seed{}.txt".format(seed, compare_method, theta, tau, human_seed)
    with open(os.path.join(config["out_trace_dir"], filename), 'w') as f:
        f.write('Create a new text file!')

    # record for deviation time step
    deviation_record = []
    traces_pre = []
    distances_action = np.zeros(shape=(len(time_real_list), 2))  # depends on how many times we compare in the below
    try:
        sim_client.step()
        traces_pre += sim_client.get_latest_trace()
        # TODO: 注意trace里第一秒是初始化，第二秒才开始sense-think-act-SEND_DATA
        for i in range(len(time_real_list) - 1):
            # compare to calculate deviation
            dists = comparator.compare(
                traces_pre[max(0, i + 1 - compare_window): i + 1],
                traces_real[max(0, i + 1 - compare_window): i + 1]
            )

            distances_action[i, :] = [time_real_list[i], np.mean(dists)]
            if i != 0 and i % frequency == 0:
                # 1. export to a new init_scenario file
                # 2. update parameters.xml to point to that file
                # 3. reload simulator
                # 4. allow the simulator to run to the new starting time step
                tmp_scenario_path = os.path.join(config["out_scenario_dir"],
                                                 'init_scenario{}.xml'.format(time_real_list[i]))
                if update_mode == "clear_knowledge":
                    print("clear knowledge when update")
                    state_tmp = copy.deepcopy(traces_real[i])
                    for g in state_tmp["graph"]:
                        g['strength'] = 0.0
                    Util.export_XML_init_file(state_tmp, tmp_scenario_path)
                elif update_mode == "keep_knowledge":
                    print("keep knowledge unchanged when update")
                    state_tmp = copy.deepcopy(traces_real[i])
                    graph_tmp = copy.deepcopy(traces_pre[i]["graph"])
                    state_tmp["graph"] = graph_tmp
                    Util.export_XML_init_file(state_tmp, tmp_scenario_path)
                else:
                    Util.export_XML_init_file(traces_real[i], tmp_scenario_path)
                sim_client.update_params({"init_scenario_path": tmp_scenario_path})
                sim_client.load_and_init()
                sim_client.run_to(time_real_list[i], silence=True)
                deviation_record.append(time_real_list[i])
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
    comparator_util = Comparator("utility")
    distances_util = comparator_util.compare(traces_pre, traces_real)
    distances_util = np.vstack([time_real_list, distances_util]).transpose()

    # write deviation record to file
    dev_file = os.path.join(config["out_statistics"], 'deviation_record.csv')
    os.makedirs(os.path.dirname(dev_file), exist_ok=True)
    with open(dev_file, 'w+') as f:
        f.write(','.join(map(str, deviation_record)) + '\n')
    np.savetxt(os.path.join(config["out_statistics"], 'distances_{}.csv'.format(compare_method)),
               distances_action, delimiter=',', fmt="%f")
    np.savetxt(os.path.join(config["out_statistics"], 'distances_utility.csv'),
               distances_util, delimiter=',', fmt="%f")


if __name__ == '__main__':
    main_seed_list = [1111, 2222, 4444, 5555, 6666]
    #main_seed_list = [7777,8888,9999,12345,67890]

    for update_mode in ["keep_knowledge", "clear_knowledge", "xxx"]:
        os.makedirs("/Users/Nann/workspace/icws2021/output/{}_{}".format(datetime.now().strftime('%Y-%m-%d--%H-%M-%S-%f')[:-3], update_mode),
                    exist_ok=True)
        #for frequency in [5,10,20,30,40,60,100]:
        #for frequency in [25,35,45,55,65,70,75,80]:
        for frequency in [25, 35, 45, 55, 65, 70, 75, 80]:
            for seed in main_seed_list:
                main("position", frequency, 100, 1, estimation_uncertainty=0.0, seed=seed, frequency=frequency,
                     update_mode=update_mode)
