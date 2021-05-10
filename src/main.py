import glob
import os
from threading import Timer
from src.Circuit import *
import xlsxwriter
import time

timer_flag = 1


def timeout():
    print("TimeOut Alarm!")
    global timer_flag
    timer_flag = 0
    

def bfsSearchDiagnosis(cir, outputs_observation):
    global timer_flag
    start_time = time.time_ns()
    t = Timer(60.0, timeout)
    t.start()

    number_of_diagnosis = 0
    res_diagnosis = list()
    min_cardinality = len(cir.gates)

    if are_outputs_equal(cir.getOutputValues(), outputs_observation):
        number_of_diagnosis += 1
        return res_diagnosis, 0, number_of_diagnosis

    bfs_queue = list()
    for gate in cir.gates:  # init first level of the bfs tree with gates
        if isDiagnosis(cir, {gate}, outputs_observation):
            res_diagnosis.append({gate})
            number_of_diagnosis += 1
            if 1 < min_cardinality:
                min_cardinality = 1
        else:
            bfs_queue.append({gate})

    while len(bfs_queue) != 0 and timer_flag == 1:
        dig_set = bfs_queue.pop(0)

        for gate in cir.gates:
            if gate not in dig_set:
                new_child = dig_set.copy()
                new_child.add(gate)
                if is_minimal_subset(new_child, res_diagnosis) and \
                        not child_already_exists_in_queue(new_child, bfs_queue):
                    if isDiagnosis(cir, new_child, outputs_observation):
                        number_of_diagnosis += 1
                        len_dig = len(dig_set)
                        if len_dig < min_cardinality:
                            min_cardinality = len_dig
                        res_diagnosis.append(new_child)
                    else:
                        bfs_queue.append(new_child)

    end_time = time.time_ns()
    total_time = (end_time-start_time)/1000000
    t.cancel()

    return res_diagnosis, min_cardinality, number_of_diagnosis, total_time


def is_minimal_subset(new_child, diagnosis):
    for dig in diagnosis:
        if new_child.intersection(dig) == dig:
            return 0
    return 1


def child_already_exists_in_queue(child, bfs_queue):
    for set_in_queue in bfs_queue:
        if set_in_queue == child:
            return 1
    return 0


def isDiagnosis(circle, digSet, outputsObservation):
    for dig in digSet:
        dig.setIsDiagnosis()

    outputs_of_gates_with_diagnosis = circle.getOutputValues()

    for dig in digSet:
        dig.ResetIsDiagnosis()

    for i in range(len(outputsObservation)):
        if outputsObservation[i] != outputs_of_gates_with_diagnosis[i]:
            return 0
    return 1


def are_outputs_equal(output1, output2):
    for i in range(len(output1)):
        if output1[i] != output2[i]:
            return 0

    return 1


def parse_observation(file_name):
    with open(file_name, 'r') as file_obs:
        data = file_obs.read()
    lines = data.split("\n")

    res = []
    for idx, line in enumerate(lines):
        input_list = []
        output_list = []
        system_and_index, arr = line.split("[")
        system_id = system_and_index.split(",")[0]
        system_id = system_id.replace("(", "")
        system_id = system_id
        arr = arr.replace("]).", "")
        arr = arr.split(",")
        for val in arr:
            if "i" in val:
                input_list.append(0 if "-" in val else 1)
            else:
                output_list.append(0 if "-" in val else 1)

        res.append((system_id, idx + 1, input_list, output_list))
    return res

if __name__ == "__main__":

    workbook = xlsxwriter.Workbook('results.xlsx')
    worksheet = workbook.add_worksheet()

    data = []


    systems = list()
    observations = list()

    curr_dir = os.path.dirname(__file__)  # <-- absolute dir to the script is in
    data_systems_rel_path = 'Data_Systems'
    data_observations_rel_path = 'Data_Observations'

    data_systems_dir = os.path.join(curr_dir, data_systems_rel_path)  # <-- absolute dir to the txt is in
    data_observations_dir = os.path.join(curr_dir, data_observations_rel_path)  # <-- absolute dir to the txt is in

    for system in glob.glob(os.path.join(data_systems_dir, '*.sys')):  # filter txt files only
        systems.append(system)
    for observation in glob.glob(os.path.join(data_observations_dir, '*.obs')):  # filter txt files only
        observations.append(observation)

    for (system_name, observation_name) in zip(systems, observations):


        res_parse = parse_observation(observation_name)
        print(system_name)
        for res in res_parse:

            timer_flag = 1

            (system, index, input_obs, output_obs) = res

            cir = Circuit(system_name, input_obs)
            for c   in cir.get_connectors():
                print(c)




