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


def main(compare_method: str, theta, human_seed: int, compare_window,
         tau=0, update_state_only=False, estimation_uncertainty=0.0, seed=3333, update_mode=None):
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
        for i in range(len(time_real_list)-1):
            # compare to calculate deviation
            dists = comparator.compare(
                traces_pre[max(0, i+1-compare_window): i+1],
                traces_real[max(0, i+1-compare_window): i+1]
            )

            distances_action[i, :] = [time_real_list[i], np.mean(dists)]
            if np.mean(dists) > theta:
                # 1. export to a new init_scenario file
                # 2. update parameters.xml to point to that file
                # 3. reload simulator
                # 4. allow the simulator to run to the new starting time step
                tmp_scenario_path = os.path.join(config["out_scenario_dir"], 'init_scenario{}.xml'.format(time_real_list[i]))
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
    main("interaction", 300, 999, 1, estimation_uncertainty=0.0)
    exit(0)

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
    simulation_time = 1000

    # parsing cli arguments
    argument_list = sys.argv[1:]
    options = "t:a:s:c:w:e:i:uqh"
    long_options = ["theta =", "tau =", "seed =", "compare =", "window =", "estimation_uncertainty =",
                    "simulation_time","update_state_only", "quiet", "help"]
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

            elif currentArgument in ("-i", "--simulation_time"):
                currentValue.replace(" ", "")
                simulation_time = int(currentValue)

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
            main(compare_method, theta, human_seed, compare_window,
                 tau=tau, update_state_only=update_state_only, estimation_uncertainty=estimation_uncertainty)
