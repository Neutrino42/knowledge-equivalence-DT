import getopt
import os
import sys

import numpy as np

import Loader
from Client import Client
from Comparator import Comparator
from SimServer import SimServer
import Util
from Config import Config
import copy

PORT1 = 25335
PORT2 = 25336


def main(compare_method: str, theta, human_seed: int, compare_window,
         tau=0, update_state_only=False, estimation_uncertainty=0.0):
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

    # load configuration
    config = Config("config.yaml").data

    # read real trace
    loader_real = Loader.TraceLoader(config["trace_real_path"])
    traces_real = loader_real.read_trace()
    time_real_list = [state["time"] for state in traces_real]

    # initialize the simulation server: for the main simulation and what-if analysis
    sim_server = SimServer(config["repast_jar_path"], PORT1)
    sim_server2 = SimServer(config["repast_jar_path"], PORT2)
    sim_server.start()
    sim_server2.start()

    # initialize the first simulation client
    # TODO: auto export init xml. Do not use both trace file and init xml file to initialise the simulator
    params = dict(
        human_count=Loader.get_num_objs(traces_real[0]),
        camera_count=Loader.get_num_cams(traces_real[0]),
        update_knowledge=str(not update_state_only).lower(),
        init_scenario_path=config["init_scenario_path"],
        output_trace_path=os.path.join(config["out_trace_dir"], "output_main.txt"),
        human_position_uncertainty=float(estimation_uncertainty),  # by default 0.0
        user_seed=human_seed
    )
    sim_client = Client(config["repast_rs"], PORT1)
    sim_client.update_params(params)
    sim_client.load_and_init()

    # Update parameters of the second simulation client (for what if analysis)
    wia_scenario_path = os.path.join(config["out_scenario_dir"], 'wia_scenario.xml')
    params2 = copy.deepcopy(params)
    params2["init_scenario_path"] = wia_scenario_path
    params2["output_trace_path"] = os.path.join(config["out_trace_dir"], "output_wia.txt")
    params2["human_position_uncertainty"] = float(0)
    sim_client2 = Client(config["repast_wia_rs"], PORT2)
    sim_client2.update_params(params2)

    # init comparator
    comparator = Comparator(compare_method)

    # Record running parameters
    filename = "seed{}-compare_{}-threshold{}_{}-human_seed{}.txt".format(seed, compare_method, theta, tau, human_seed)
    with open(os.path.join(config["out_trace_dir"], filename), 'w') as f:
        f.write('Create a new text file!')

    deviation_record = []
    traces_pre = []
    distances_action = np.zeros(shape=(len(time_real_list)-2, 2))  # depends on how many times we compare in the below
    try:
        # The first time step, initialisation
        sim_client.step()
        traces_pre += sim_client.get_latest_trace()
        # NOTICE:
        # Comparison starts from index 1, not 0, because the first time step is initialisation
        # The trace records the status at the end of that time step.
        #   - i.e. Simulated behaviour between two time steps (between t and t+1): sense->think->act->print_trace
        #   - e.g. Trace denoted with t=2 represents what the world is after sense-think-act and the actions have made.
        #   - Trace denoted with t=2 also represents the starting state of t=3 (before sense)
        for i in range(len(time_real_list) - 1):
            print(time_real_list[i])
            if i > 0:
                # -- run what-if analysis --
                #    e.g. when t = 2
                # 1. export to the predefined path of the tmp init_scenario file
                #    with perception and knowledge at the end of LAST time step t=1
                # 2. (re)load sim_client2
                # 3. set sim_client2 to start from last time step t=1
                # 4. run sim_client2.step() for one tick --> t=2
                # 5. get actions (at t=2) from sim_client
                if time_real_list[i - 1] in deviation_record:  # check whether there is an update at previous time step
                    tmp_state = copy.deepcopy(traces_real[i - 1])
                else:
                    tmp_state = copy.deepcopy(traces_real[i - 1])
                    tmp_state["graph"] = traces_pre[i - 1]["graph"]
                # TODO: this tmp_state is just a workaround, if we want to run WIA for more time steps,
                # TODO: ... we need to carefully think about how to update the state and estimate the uncovered objects
                Util.export_XML_init_file(tmp_state, wia_scenario_path)
                sim_client2.load_and_init()
                sim_client2.run_to(time_real_list[i - 1], silence=True)
                sim_client2.step()
                traces_wia = sim_client2.get_latest_trace()

                # -- read real trace and compare --
                # (at the end of current time step t=2)
                dists = comparator.compare(traces_wia, traces_real[i])
                distances_action[i-1, :] = [time_real_list[i], np.mean(dists)]
                if np.mean(dists) > theta:
                    # -- update the MAIN simulator --
                    # 1. export to a new init_scenario file
                    # 2. update parameters.xml to point to that file
                    # 3. reload simulator
                    # 4. set the simulator to start from the new starting time step
                    tmp_scenario_path = os.path.join(config["out_scenario_dir"],
                                                     'init_scenario{}.xml'.format(time_real_list[i]))
                    Util.export_XML_init_file(traces_real[i], tmp_scenario_path)
                    sim_client.update_params({"init_scenario_path": tmp_scenario_path})
                    sim_client.load_and_init()
                    sim_client.run_to(time_real_list[i], silence=True)
                    deviation_record.append(time_real_list[i])
            # -- simulate the next time step --
            sim_client.step()
            traces_pre += sim_client.get_latest_trace()
    except Exception as e:
        sim_client.terminate()
        sim_client2.terminate()
        sim_server.terminate()
        sim_server2.terminate()
        print(str(e))
        exit(-10)

    sim_client.terminate()
    sim_client2.terminate()
    sim_client.export_all_traces(os.path.join(config["out_trace_dir"], "output_main.txt"))
    sim_client.update_params(params)  # restore to default init_scenario
    sim_client2.update_params(params2)  # restore to default init_scenario
    sim_client2.export_all_traces(os.path.join(config["out_trace_dir"], "output_wia.txt"))
    sim_server.terminate()
    sim_server2.terminate()

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
    main("action", 0.1, 100, 1, estimation_uncertainty=5.0)
