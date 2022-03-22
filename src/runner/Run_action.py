import Main_action
import Main_new
import numpy as np

# np.linspace(0, 0.6, 11)[1:-1]
# ----- designed1_D ------
list_designed1_D_action_1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
                             0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]  # 0-1
list_designed1_D_action_2 = [0.01, 0.02, 0.03, 0.04, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11,
                             0.12, 0.13, 0.14, 0.16, 0.17, 0.18, 0.19]  # 0-0.2
list_designed1_D_action_3 = [0.191, 0.192, 0.193, 0.194, 0.195, 0.196, 0.197, 0.198, 0.199]  # 0.19-0.2
list_designed1_D_action_4 = [0.23, 0.26, 0.29, 0.32, 0.35, 0.38, 0.41, 0.44, 0.47]  # 0.2-0.5

list_designed1_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_designed1_D_position_2 = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19]
list_designed1_D_position_3 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
                               0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
list_designed1_D_position_4 = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]  # 1-10

list_designed1_D_interaction_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
list_designed1_D_interaction_2 = [1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6,
                                  3.8, 4, 4.2, 4.4, 4.6, 4.8]
list_designed1_D_interaction_3 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
list_designed1_D_interaction_4 = [5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10.5,
                                  11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5]

# ----- designed2_D ------
list_designed2_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_designed2_D_position_2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                               3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_designed2_D_position_3 = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3,
                               1.4, 1.6, 1.7, 1.8, 1.9]  # 0-2
list_designed2_D_interaction_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
list_designed2_D_interaction_2 = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]

list_designed2_D_action_1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # 0-1
list_designed2_D_action_2 = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]  # 0-1
list_designed2_D_action_3 = [0.01, 0.02, 0.03, 0.04, 0.06, 0.07, 0.08, 0.09, 0.11,
                             0.12, 0.13, 0.14, 0.16, 0.17, 0.18, 0.19]  # 0-0.2

# ---- designed3_D ----
list_designed3_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_designed3_D_position_2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                               3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_designed3_D_position_3 = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3,
                               1.4, 1.6, 1.7, 1.8, 1.9]  # 0-2

list_designed3_D_action_1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
                             0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]  # 0-1
list_designed3_D_action_2 = [0.015, 0.03, 0.045, 0.06, 0.075, 0.09, 0.105, 0.12, 0.135,
                             0.165, 0.18, 0.195, 0.21, 0.225, 0.24, 0.255, 0.27,
                             0.285]  # 0-0.3
list_designed3_D_action_3 = [0.31, 0.32, 0.33, 0.34, 0.36, 0.37, 0.38, 0.39]
list_designed3_D_interaction_1 = list_designed1_D_interaction_1
list_designed3_D_interaction_2 = list_designed1_D_interaction_2
list_designed3_D_interaction_3 = list_designed1_D_interaction_3
list_designed3_D_interaction_4 = list_designed1_D_interaction_4

# ---- random1_D ----
list_random1_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_random1_D_position_2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                             3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_random1_D_position_3 = [6, 7, 8, 9, 11, 12, 13, 14]
list_random1_D_action_1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55,
                           0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]  # 0-1
list_random1_D_action_2 = [0.12, 0.14, 0.16, 0.18, 0.22, 0.24, 0.26, 0.28, 0.32,
                           0.34, 0.36, 0.38, 0.42, 0.44, 0.46, 0.48]
list_random1_D_interaction_1 = list_designed1_D_interaction_1
list_random1_D_interaction_2 = list_designed1_D_interaction_2
list_random1_D_interaction_3 = list_designed1_D_interaction_3
list_random1_D_interaction_4 = list_designed1_D_interaction_4

# --- random2_D ---
list_random2_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_random2_D_position_2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                             3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_random2_D_position_3 = [6, 7, 8, 9, 11, 12, 13, 14]

list_random2_D_action_1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # 0-1
list_random2_D_action_2 = [0.115, 0.13, 0.145, 0.16, 0.175, 0.19, 0.205, 0.22, 0.235,
                           0.25, 0.265, 0.28, 0.295, 0.31, 0.325, 0.34, 0.355, 0.37,
                           0.385]
list_random2_D_interaction_1 = list_designed1_D_interaction_1
list_random2_D_interaction_2 = list_designed1_D_interaction_2
list_random2_D_interaction_3 = list_designed1_D_interaction_3
list_random2_D_interaction_4 = list_designed1_D_interaction_4
list_random2_d_action_new = [0.06, 0.12, 0.19, 0.26, 0.32, 0.39, 0.46, 0.52, 0.59, 0.66, 0.72, 0.79, 0.86, 0.92, 0.99]
# calculated according to 1/15, 2/15, 3/15, ...

# --- random3_D ---
list_random3_D_position_1 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
list_random3_D_position_2 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                             3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_random3_D_action_1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # 0-1
list_random3_D_action_2 = [0.12, 0.14, 0.16, 0.18, 0.22, 0.24, 0.26, 0.28, 0.32,
                           0.34, 0.36, 0.38, 0.42, 0.44, 0.46, 0.48]
list_random3_D_interaction_1 = list_designed1_D_interaction_1
list_random3_D_interaction_2 = list_designed1_D_interaction_2
list_random3_D_interaction_3 = list_designed1_D_interaction_3
list_random3_D_interaction_4 = list_designed1_D_interaction_4

# --- designed2_U
list_designed_U_position_1 = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                              3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75]
list_designed_U_position_2 = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

list_designed_U_action_1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]


def run_deviated(threshold_list, method, main_seed):
    human_seed = 100
    for th in threshold_list:
        print("th{}_seed{}".format(th, human_seed))
        if method == "action":
            Main_action.main(method, th, human_seed, 1, estimation_uncertainty=0.0)
        else:
            # If compare action directly, not using WIA
            if method == "action_direct":
                tmp_method = "action"
            else:
                tmp_method = method
            Main_new.main(tmp_method, th, human_seed, 1, estimation_uncertainty=0.0, seed=main_seed)
#            Main_new.main(tmp_method, th, human_seed, 1, estimation_uncertainty=0.0, seed=main_seed, update_mode="clear_knowledge")

def run_unknown(run_list, seed_list, method, main_seed, uncertainty=5.0):
    for th in run_list:
        for human_seed in seed_list:
            print("th{}_humanSeed{}".format(th, human_seed))
            if method == "action":
                Main_action.main(method, th, human_seed, 1, estimation_uncertainty=uncertainty)
            else:
                if method == "action_direct":
                    tmp_method = "action"
                else:
                    tmp_method = method
                Main_new.main(tmp_method, th, human_seed, 1, estimation_uncertainty=uncertainty, seed=main_seed)


human_seed_list = [100, 200, 300, 400, 500]

if __name__ == '__main__':

    main_seed_list = [1111, 2222, 4444, 5555, 6666]
    """
    for main_seed in [1111,2222,4444,5555,6666,7777,8888,9999, 12345,5342]:
        run_deviated([500], "position", main_seed=main_seed)
    """
    # no update with estimation
    # run_unknown([500], human_seed_list + [600, 700, 800, 900, 1000], "interaction", 3333, uncertainty=5.0)


    # designed1-U with estimation
    # run_unknown(list_designed1_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_designed1_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_designed1_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_designed1_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown(list_designed1_D_position_2, human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown(list_designed1_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed1_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed1_D_position_3, human_seed_list, "position", 3333, uncertainty=5.0)

    # designed2-U with estimation
    #run_unknown(list_designed2_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_designed2_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown([0.2,1.1,1.2,1.3,1.4,1.5], human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown([6, 7, 8, 9, 12, 14, 17, 18], human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown([55,60,65,70,75,80,90,100,110,120], human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_designed2_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown([5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 11, 12, 13, 14, 16, 17, 18, 19],
    #            human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown(list_designed2_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 11, 12, 13, 14, 16, 17, 18, 19],
    #            human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed2_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed2_D_position_3, human_seed_list, "position", 3333, uncertainty=5.0)


    # designed3-U with estimation
    #run_unknown(list_designed3_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown([6,7,8,9,12,14,17,18], human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown([55,60,65,70,75,80,90,100], human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown([5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 11, 12, 13, 14, 16, 17, 18, 19],
    #           human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_designed3_D_position_3, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 11, 12, 13, 14, 16, 17, 18, 19],
    #            human_seed_list, "position", 3333, uncertainty=5.0)

    # random1-U with estimation
    # run_unknown(list_random1_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random1_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random1_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown([55,60,65,70,80,90,100,110,120,130,140], human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown([6,7,8,9,12,14,17,18], human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random1_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown(list_random1_D_position_2, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 9.6, 9.7, 9.8, 9.9, 11, 12, 13, 14],
    #           human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown(list_random1_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_random1_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 9.6, 9.7, 9.8, 9.9, 11, 12, 13, 14],
    #          human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([0.3,0.4], human_seed_list, "position", 3333, uncertainty=5.0)

    # random2-U with estimation
    #run_unknown(list_random2_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_random2_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    #run_unknown(list_random2_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown([55,60,65,70,80,90,100,110,120,130,140], human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown([6,7,8,9,12,14,17,18], human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random2_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown(list_random2_D_position_2, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 9.6, 9.7, 9.8, 9.9, 11, 12, 13, 14],
    #            human_seed_list, "position_all", 3333, uncertainty=5.0)
    #run_unknown(list_random2_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown(list_random2_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 9.6, 9.7, 9.8, 9.9, 11, 12, 13, 14],
    #           human_seed_list, "position", 3333, uncertainty=5.0)
    #run_unknown([0.3,0.4], human_seed_list, "position", 3333, uncertainty=5.0)

    # random3-U with estimation
    # # uncertainty=2.0
    # run_unknown(list_random3_D_position_1, human_seed_list, "position", 3333, uncertainty=2.0)
    # run_unknown(list_random3_D_position_2, human_seed_list, "position", 3333, uncertainty=2.0)
    # run_unknown(list_random3_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=2.0)
    # run_unknown(list_random3_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=2.0)
    # run_unknown(list_random3_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=2.0)
    # run_unknown(list_random3_D_interaction_4, human_seed_list, "interaction", 3333, uncertainty=2.0)
    # # uncertainty=5.0
    # run_unknown(list_random3_D_interaction_1, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_interaction_2, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_interaction_3, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_interaction_4, human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown([60,70,80,90,100], human_seed_list, "interaction", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_position_1, human_seed_list, "position", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_position_2, human_seed_list, "position", 3333, uncertainty=5.0)
    # run_unknown([0.2,0.3, 0.4, 0.5, 0.6, 6, 7, 8, 9], human_seed_list, "position", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_position_1, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown(list_random3_D_position_2, human_seed_list, "position_all", 3333, uncertainty=5.0)
    # run_unknown([5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 9.6, 9.7, 9.8, 9.9, 11, 12, 13, 14],
    #            human_seed_list, "position_all", 3333, uncertainty=5.0)

    # random3-D-4444

#    for main_seed in [1111,2222,4444,5555,6666]:
#        run_deviated([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], "action_direct", main_seed=main_seed)  # v2
#        run_deviated(list_random3_D_action_2, "action_direct", main_seed=main_seed)
#        run_deviated(list_random3_D_action_1, "action_direct", main_seed=main_seed)
#        run_deviated(list_random3_D_position_2, "position", main_seed=main_seed)
#        run_deviated(list_random3_D_position_1, "position", main_seed=main_seed)
#        run_deviated([6,7,8,9,12.5], "position", main_seed=main_seed)
#        run_deviated(list_random3_D_interaction_1, "interaction", main_seed=main_seed)
#        run_deviated(list_random3_D_interaction_2, "interaction", main_seed=main_seed)
#        run_deviated(list_random3_D_interaction_3, "interaction", main_seed=main_seed)
#        run_deviated([60, 70, 80, 90, 100, 110, 120], "interaction", main_seed=main_seed)
#        run_deviated(list_random3_D_interaction_4, "interaction", main_seed=main_seed)


    # random2-D-4444

#    for main_seed in main_seed_list:
        #run_deviated(list_random2_d_action_new, "action_direct", main_seed=main_seed)  # v2
#        run_deviated(list_random2_D_action_2, "action_direct", main_seed=main_seed)
#        run_deviated(list_random2_D_action_1, "action_direct", main_seed=main_seed)
#       run_deviated(list_random2_D_position_2, "position", main_seed=main_seed)
#        run_deviated(list_random2_D_position_1, "position", main_seed=main_seed)
#        run_deviated(list_random2_D_position_3, "position", main_seed=main_seed)
#        run_deviated(list_random2_D_interaction_1, "interaction", main_seed=main_seed)
#        run_deviated(list_random2_D_interaction_2, "interaction", main_seed=main_seed)
#        run_deviated(list_random2_D_interaction_3, "interaction", main_seed=main_seed)
#        run_deviated(list_random2_D_interaction_4, "interaction", main_seed=main_seed)
#        run_deviated([60, 70, 80, 90, 100, 110, 120], "interaction", main_seed=main_seed)

# random1-D-4444

#    for main_seed in main_seed_list:
#        run_deviated(list_random1_D_interaction_1, "interaction", main_seed=main_seed)
#        run_deviated(list_random1_D_interaction_2, "interaction", main_seed=main_seed)
#        run_deviated(list_random1_D_interaction_3, "interaction", main_seed=main_seed)
#        run_deviated(list_random1_D_interaction_4, "interaction", main_seed=main_seed)
#        run_deviated([55,60,65,70,75,80,90,100,110], "interaction", main_seed=main_seed)

#        run_deviated(list_random1_D_position_1, "position", main_seed=main_seed)
#        run_deviated(list_random1_D_position_2, "position", main_seed=main_seed)
#        run_deviated(list_random1_D_position_3, "position", main_seed=main_seed)
#        run_deviated(list_random1_D_action_1, "action_direct", main_seed=main_seed)
#        run_deviated(list_random1_D_action_2, "action_direct", main_seed=main_seed)
        #run_deviated([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], "action_direct", main_seed=main_seed)  # v2

    # designed3-D-4444

    #for main_seed in main_seed_list:
        #run_deviated([0.08, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9], "action_direct", main_seed=main_seed)  # v2
        
        #run_deviated(list_designed3_D_action_3, "action_direct", main_seed=main_seed)
        #run_deviated(list_designed3_D_action_2, "action_direct", main_seed=main_seed)
        #run_deviated(list_designed3_D_action_1, "action_direct", main_seed=main_seed)
        #run_deviated(list_designed3_D_position_2, "position", main_seed=main_seed)
        #run_deviated(list_designed3_D_position_1, "position", main_seed=main_seed)
        #run_deviated([6,7,8,9], "position", main_seed=main_seed)
        #run_deviated(list_designed3_D_interaction_1, "interaction", main_seed=main_seed)
        #run_deviated(list_designed3_D_interaction_2, "interaction", main_seed=main_seed)
        #run_deviated(list_designed3_D_interaction_3, "interaction", main_seed=main_seed)
        #run_deviated(list_designed3_D_interaction_4, "interaction", main_seed=main_seed)
        #run_deviated([55,60,65,70,75,80,90,100,110], "interaction", main_seed=main_seed)
        #run_deviated(list_designed3_D_position_2, "position_all", main_seed=main_seed)
        #run_deviated(list_designed3_D_position_1, "position_all", main_seed=main_seed)
        #run_deviated([6, 7, 8, 9], "position_all", main_seed=main_seed)

    # designed2-D-4444

#    for main_seed in [1111,2222,4444,5555,6666]:
#        run_deviated([0.08, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9], "action_direct", main_seed=main_seed)  # v2
#        #run_deviated([0.1,0.2,0.3,0.4,0.75,1.25,1.75], "interaction", main_seed=main_seed)
#        run_deviated(list_designed2_D_action_3, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed2_D_action_2, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed2_D_action_1, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed2_D_interaction_2, "interaction", main_seed=main_seed)
#        run_deviated(list_designed2_D_interaction_1, "interaction", main_seed=main_seed)
#        run_deviated([6, 7, 8, 9, 12, 14, 16, 18, 22, 24], "interaction", main_seed=main_seed)
#        run_deviated(list_designed2_D_position_3, "position", main_seed=main_seed)
#        run_deviated(list_designed2_D_position_2, "position", main_seed=main_seed)
#        run_deviated(list_designed2_D_position_1, "position", main_seed=main_seed)
#        run_deviated([6,7,8,9,12,14,16,18,22,24], "position", main_seed=main_seed)

    # for designed1_new

#    for main_seed in [1111,2222,4444,5555,6666]:
        # run_unknown([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], seed_list, "action_direct", main_seed=main_seed) # v2
        # run_unknown(list_designed1_D_action_2, seed_list, "action_direct")
        # run_unknown(list_designed1_D_action_1, seed_list, "action_direct")
        # run_unknown(list_designed1_D_action_3, seed_list, "action_direct")
        # run_unknown(list_designed1_D_action_4, seed_list, "action_direct")
        # run_unknown(list_designed1_D_interaction_1, seed_list, "interaction")
        # run_unknown(list_designed1_D_interaction_2, seed_list, "interaction")
        # run_unknown(list_designed1_D_interaction_3, seed_list, "interaction")
        # run_unknown(list_designed1_D_interaction_4, seed_list, "interaction")
        # run_unknown(list_designed1_D_position_1, seed_list, "position")
        # run_unknown(list_designed1_D_position_2, seed_list, "position")
        # run_deviated(list_designed1_D_position_1, "position")
        # run_deviated(list_designed1_D_position_2, "position")
        # run_deviated(list_designed1_D_position_3, "position")
        # run_deviated(list_designed1_D_action_1, "action")
        # run_deviated(list_designed1_D_action_2, "action")
        # run_deviated(list_designed1_D_action_3, "action")
        # run_deviated(list_designed1_D_action_4, "action")
#        run_deviated([0.1,0.3,0.5,0.7,0.9], "action_direct", main_seed=main_seed)
#        run_deviated(list_designed1_D_action_1, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed1_D_action_2, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed1_D_action_3, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed1_D_action_4, "action_direct", main_seed=main_seed)
#        run_deviated(list_designed1_D_position_1, "position", main_seed=main_seed)
#        run_deviated(list_designed1_D_position_2, "position", main_seed=main_seed)
#        run_deviated(list_designed1_D_position_3, "position", main_seed=main_seed)
#        run_deviated([1.3,1.5,1.6,2.2,2.4,2.6,2.8], "position", main_seed=main_seed)
#        run_deviated(list_designed1_D_interaction_1, "interaction", main_seed=main_seed)
#        run_deviated(list_designed1_D_interaction_2, "interaction", main_seed=main_seed)
#        run_deviated(list_designed1_D_interaction_3, "interaction", main_seed=main_seed)
#        run_deviated(list_designed1_D_interaction_4, "interaction", main_seed=main_seed)


    # random2_new
    # run_deviated(list_random2_d_action_new, "action")

    # run_deviated(list_random2_d_action_new, "action_direct")
    # run_deviated(list_random2_D_position_1, "position")
    # run_deviated(list_random2_D_position_2, "position")
    # run_deviated([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], "action_direct")

    # random1_new
    # run_deviated(list_designed1_D_interaction_2, "interaction")
    # run_deviated(list_designed1_D_interaction_3, "interaction")
    # run_deviated(list_random1_D_action_1, "action_direct")
    # run_deviated(list_random1_D_action_2, "action_direct")
    # run_deviated(list_random2_D_position_1, "position")
    # run_deviated(list_random2_D_position_2, "position")
    # run_deviated(list_designed1_D_action_1, "action_direct")
    # run_deviated(list_designed1_D_action_2, "action_direct")
    # run_deviated(list_designed1_D_action_3, "action_direct")
    # run_deviated(list_designed1_D_action_4, "action_direct")

    # use action_deviation_v2 for designed1
    # run_deviated(list_designed1_D_action_1, "action_direct")
    # run_deviated(list_designed1_D_action_2, "action_direct")
    # run_deviated(list_designed1_D_action_3, "action_direct")
    # run_deviated(list_designed1_D_action_4, "action_direct")

    # use action_deviation_v2 for designed2
    # run_deviated(list_designed2_D_action_1, "action_direct")
    # run_deviated(list_designed2_D_action_2, "action_direct")
    # run_deviated(list_designed2_D_action_3, "action_direct")

    # updated WIA after debugging
    # run_deviated(list_designed2_D_action_3, "action")
    # run_deviated(list_designed2_D_action_2, "action")
    # run_deviated(list_designed2_D_action_1, "action")

    ## Direct compare action, no WIA
    # run_deviated(list_designed2_D_action_3, "action_direct")
    # run_deviated(list_designed2_D_action_2, "action_direct")
    # run_deviated(list_designed2_D_action_1, "action_direct")
    # run_deviated(list_designed1_D_action_2, "action_direct")
    # run_deviated(list_designed1_D_action_1, "action_direct")

    # run_unknown(list_designed_U_action_1, seed_list, "action")
    # run_unknown(list_designed_U_position_2, seed_list, "position")
    # run_unknown(list_designed_U_position_1, seed_list, "position")

    # run_unknown(list_designed_U_position_1, seed_list, "position")

    # run_deviated(list_random3_D_action_2, "action")
    # run_deviated(list_random3_D_action_1, "action")
    # run_deviated(list_random3_D_position_2, "position")
    # run_deviated(list_random3_D_position_1, "position")

    # run_deviated(list_random2_D_action_2, "action")
    # run_deviated(list_random2_D_action_1, "action")

    # run_deviated(list_random2_D_position_2, "position")
    # run_deviated(list_random2_D_position_1, "position")

    # run_deviated(list_random1_D_action_2, "action")
    # run_deviated(list_random1_D_action_1, "action")

    # run_deviated(list_random1_D_position_2, "position")
    # run_deviated(list_random1_D_position_1, "position")

    # run_deviated(list_designed3_D_action_3, "action")
    # run_deviated(list_designed3_D_action_2, "action")
    # run_deviated(list_designed3_D_action_1, "action")

    # run_deviated(list_designed3_D_position_2, "position")
    # run_deviated(list_designed3_D_position_1, "position")

    # run_deviated(list_designed2_D_action_3, "action")
    # run_deviated(list_designed2_D_action_2, "action")
    # run_deviated(list_designed2_D_action_1, "action")
    # run_deviated(list_designed2_D_interaction_2, "interaction")
    # run_deviated(list_designed2_D_interaction_1, "interaction")
    # run_deviated(list_designed2_D_position_3, "position")
    # run_deviated(list_designed2_D_position_2, "position")
    # run_deviated(list_designed2_D_position_1, "position")

    # run_deviated(list_designed1_D_interaction_4, "interaction")
    # run_deviated(list_designed1_D_interaction_3, "interaction")
    # run_deviated(list_designed1_D_interaction_2, "interaction")
    # run_deviated(list_designed1_D_interaction_1, "interaction")
    # run_deviated(list_designed1_D_position_4, "position")
    # run_deviated(list_designed1_D_position_3, "position")
    # run_deviated(list_designed1_D_position_2, "position")
    # run_deviated(list_designed1_D_position_1, "position")
    # run_deviated(list_designed1_D_action_4, "action")
    # run_deviated(list_designed1_D_action_3, "action")
    # run_deviated(list_designed1_D_action_2, "action")
    # run_deviated(list_designed1_D_action_1, "action")
