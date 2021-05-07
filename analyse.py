import numpy as np
import csv
import pandas as pd


def main():
    base_dir = "./result/seed3333"
    deviation_file = base_dir + "/" + "deviation_record3333.csv"
    archive_file = base_dir + "/" + "all_distances_3333.csv"

    with open(deviation_file) as f:
        f_csv = csv.reader(f)
        first_line = next(f_csv)  # read first line
        record = list(map(int, first_line))

        # how many deviation
        dev_count = len(record)

        # time spans between two deviations
        intervals = [record[0]] + [record[i] - record[i-1] for i in range(1, len(record))]

        # print("deviation time steps: ")
        # print(record)
        print("deviation time intervals: ")
        print(intervals)
        print("mean and std: ")
        print(np.mean(intervals), np.std(intervals))

    df = pd.read_csv(archive_file)
    print(df[['baseline', 'global_goal', 'interaction', 'local_goals']].mean())
    print(df[['baseline', 'global_goal', 'interaction', 'local_goals']].std())


if __name__ == '__main__':
    main()

