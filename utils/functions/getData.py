from utils.functions.processFile import remove_accent
from utils.functions.resample import process_event_data
import pandas as pd


def get_init_time_and_fin_time(file_dict, time_name):
    init_time = 0
    fin_time = 0

    for key in file_dict.keys():
        if key == time_name:
            init_time = file_dict[key][0]
            fin_time = file_dict[key][-1]

    return init_time, fin_time


def get_events_csv_dict(objects_data):
    data = {}

    for obj in objects_data:
        remove_accent(obj.csv.name)
        csv = pd.read_csv(obj.csv.name, sep=';')
        performance_variables = csv.columns.values.tolist()

        for perf_var in performance_variables:
            data[perf_var.replace(" ", "_")] = []

        if obj.is_event_file:
            for row in list(csv.values):
                for (element_row, perf_var) in zip(row, performance_variables):
                    data[perf_var.replace(" ", "_")].append(element_row)

    return data


def get_init_time_and_fin_time_from_events_file(csv, data, obj, time_ms_name_events_file,
                                                duration_time_ms_name_events_file):
    performance_variables = csv.columns.values.tolist()

    for row in csv.values.tolist():
        for (element_row, perf_var) in zip(row, performance_variables):
            data[perf_var.replace(" ", "_")].append(element_row)
    file_dict = process_event_data(data, obj.frequency, time_ms_name_events_file,
                                   duration_time_ms_name_events_file)
    context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_ms_name_events_file)

    return context_init_time, context_fin_time, file_dict


def get_performance_variables_from_object_file(is_events_or_devices_file, data_files):
    context_perf_vars = []
    for obj in data_files:
        if obj.is_event_file == is_events_or_devices_file:
            remove_accent(obj.csv.name)
            csv = pd.read_csv(obj.csv.name, sep=';')
            performance_variables = csv.columns.values.tolist()
            for perf_var in performance_variables:
                perf_var = perf_var.replace(" ", "_")
                if perf_var not in context_perf_vars:
                    context_perf_vars.append(perf_var)
    return context_perf_vars
