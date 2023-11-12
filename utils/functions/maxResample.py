from utils.functions.interpol import interpol_devices, interpol_events
import pandas as pd
import os


def max_re_sample(csv_dict, curr_freq, time_lasting, length_array, time_name, events_duration_time_name):
    df = pd.DataFrame.from_dict(csv_dict, orient="columns")
    df.to_csv("data_interpol.csv")
    csv = pd.read_csv("data_interpol.csv", header=0, index_col=[0])
    os.remove("data_interpol.csv")
    performance_variables = csv.columns.values.tolist()
    data = {}
    for var in performance_variables:
        data[var] = []
    if curr_freq == 100:
        interpol_devices(data, csv, performance_variables, 10, length_array)
    elif curr_freq == 10:
        interpol_devices(data, csv, performance_variables, 100, length_array)
    elif curr_freq == 1000:
        for row in list(csv.values):
            for (element_row, element_perf_var) in zip(row, performance_variables):
                data[element_perf_var].append(element_row)
    else:
        interpol_events(data, csv, performance_variables, time_lasting, time_name, events_duration_time_name)
    return data
