from DigitalTwin import DigitalTwin

MONITOR_FREQUENCY = 1


def load_data(t):
    data = []
    return data


def compare(phy_trace, vir_trace):
    result = 1
    return result


def is_deviated(result):
    return True


def recordStat():
    pass


def main():
    end_time = 100
    my_twin = DigitalTwin(0, load_data(0))
    vir_trace = my_twin.predict(end_time)
    phy_trace = []

    t = 0
    while t <= end_time:
        if t % MONITOR_FREQUENCY == 0:
            cur_data = load_data(t)
            phy_trace += cur_data
            result = compare(phy_trace, vir_trace)
            if is_deviated(result):
                # update DT and predict again
                my_twin.update(t, cur_data)
                vir_trace = my_twin.predict(end_time)
                recordStat()
        t = t + 1


if __name__ == '__main__':
    main()
