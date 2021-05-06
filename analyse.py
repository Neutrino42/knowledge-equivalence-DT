import numpy as np
import csv


with open("deviation_record3333.csv") as f:
    f_csv = csv.reader(f)
    first_line = next(f_csv)  # read first line
    record = list(map(int, first_line))

    # how many deviation
    dev_count = len(record)

    # time spans between two deviations
    intervals = [record[0]] + [record[i] - record[i-1] for i in range(1, len(record))]

    print(record)
    print(intervals)
    print(np.mean(intervals), np.std(intervals))


