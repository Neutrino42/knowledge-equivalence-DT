import numpy as np
import Loader


class Comparator(object):
    def __init__(self, compare_method="position"):
        self.__method = compare_method
        self.__k = 2

    def set_compare_method(self, compare_method):
        self.__method = compare_method

    def compare(self, traces_pre, traces_real):
        """
        Compare two input traces. A trace can be a list or a state.
        :param traces_pre:
        :param traces_real:
        :return: deviation -- a list or a double
        """
        if not isinstance(traces_pre, list):
            traces_pre = [traces_pre]
        if not isinstance(traces_real, list):
            traces_real = [traces_real]

        distances = []
        if self.__method == "action":
            distances = self.__compare_action(traces_pre, traces_real)
        elif self.__method == "position":
            distances =  self.__compare_position(traces_pre, traces_real)
        elif self.__method == "interaction":
            distances = self.__compare_interaction(traces_pre, traces_real)
        else:
            exit(-1)

        if len(distances) == 1:
            return distances[0]
        else:
            return distances

    def __compare_action(self, traces_1, traces_2):
        distances = []
        for state_1, state_2 in zip(traces_1, traces_2):
            d = 0
            for ID in state_2["cameras"].keys():
                action_r = state_2["cameras"][ID]["actions"]
                action_p = state_1["cameras"][ID]["actions"]
                d += self.__action_deviation(action_p, action_r)
            distances.append(float(d)/len(state_2["cameras"]))
        return distances

    def __compare_position(self, traces_pre, traces_real):
        distances = []
        for state_pre, state_real in zip(traces_pre, traces_real):
            distances.append(self.__position_deviation(state_pre, state_real))
        return distances

    def __compare_interaction(self, traces_1, traces_2):
        distances = []
        for state_1, state_2 in zip(traces_1, traces_2):
            distances.append(self.__interaction_deviation(state_1["graph"], state_2["graph"]))
        return distances

    def __action_deviation(self, action_1, action_2):
        if action_1["random"] == 1 and action_2["random"] == 1:
            return 1
        elif action_1["respond"] != -1 and action_2["respond"] != -1:
            d = 0.7
            if action_1["respond"] == action_2["respond"]:
                d += 0.15
            if action_1["follow"] == action_2["follow"]:
                d += 0.15
            return d
        elif action_1["respond"] == -1 and action_2["respond"] == -1:
            if action_1["follow"] == action_2["follow"]:
                return 1
            else:
                return 0
        else:
            return 0

    def __position_deviation(self, state_p, state_r):  # p for predicted and r for real
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
        objs_r = Loader.get_all_covered_objects(state_r)
        if len(objs_r) != 0:
            sorted_objs_r = sorted(objs_r.items())
            objs_r_array = np.array([item[1] for item in sorted_objs_r])
            ids_r = [item[0] for item in sorted_objs_r]

            # find the covered real object ids in prediction trace
            objs_p = Loader.get_all_covered_objects(state_p)
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

    def __interaction_deviation(self, graph_1: list, graph_2: list):
        edge_list_1 = [[edge['source_id'], edge['target_id']] for edge in graph_1]
        edge_list_2 = [[edge['source_id'], edge['target_id']] for edge in graph_2]
        assert edge_list_1 == edge_list_2
        strengths_1 = [edge['strength'] for edge in graph_1]
        strengths_2 = [edge['strength'] for edge in graph_2]
        return np.linalg.norm(np.array(strengths_1) - np.array(strengths_2))


