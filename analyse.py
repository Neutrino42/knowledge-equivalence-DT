import numpy as np
import csv
import pandas as pd


def get_statistics(compare_method: str, theta, human_seed):
    print("For " + compare_method)
    base_dir = "./result/seed3333/threshold{}/human_seed{}/compare_{}".format(theta, human_seed, compare_method)
    deviation_file = base_dir + "/" + "deviation_record3333_{}.csv".format(human_seed)
    archive_file = base_dir + "/" + "all_distances_3333_{}.csv".format(human_seed)
    with open(deviation_file) as f:
        f_csv = csv.reader(f)
        first_line = next(f_csv)  # read first line
        record = list(map(int, first_line))

        # how many deviation
        dev_count = len(record)
        print("number of deviations:")
        print(dev_count)

        # time spans between two deviations
        intervals = [record[0]] + [record[i] - record[i - 1] for i in range(1, len(record))]

        # print("deviation time steps: ")
        # print(record)
        print("deviation time intervals: ")
        print(intervals)
        print("mean and std: ")
        print(np.mean(intervals), np.std(intervals))
    df = pd.read_csv(archive_file)
    return df
    # print(df[['baseline', 'global_goal', 'interaction', 'local_goals']].mean())
    # print(df[['baseline', 'global_goal', 'interaction', 'local_goals']].std())


def main():
    compare_method_list = ["baseline", "interaction", "local_goals", "global_goals"]
    human_seed_list = list(range(100, 1001, 100))
    threshold_list = [30, 40]
    compare_method = "baseline"

    for threshold in threshold_list:
        df_list = []
        for seed in human_seed_list:
            df_list.append(get_statistics(compare_method, threshold, seed))

        result = pd.concat(df_list, axis=1, join="inner")


if __name__ == '__main__':
    main()

