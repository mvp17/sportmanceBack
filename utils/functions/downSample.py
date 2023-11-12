from utils.functions.processFile import float_data_to_int_data
import pandas as pd
import os


def down_sample(dict_csv, table_frequency, events_time_name, devices_time_name):
    # Frequency of dict_csv data is 1000 Hz
    if table_frequency != 1000:
        average = int(round(1000/table_frequency))
        time = []
        for key in dict_csv.keys():
            downsampled = dict_csv.get(key)[0::average]
            if key == events_time_name or key == devices_time_name:
                for element in downsampled:
                    time.append(round(element / 10) * 10)
                dict_csv[key] = time
            else:
                dict_csv[key] = downsampled
            dict_csv[key] = downsampled
    return dict_csv


def filter_time_files(dict_down_sampled_files, init_filter_time, fin_filter_time, events_time_name,
                      events_duration_time_name, devices_time_name):
    files_to_render = []
    for file in dict_down_sampled_files:
        df = pd.DataFrame.from_dict(file, orient="columns")
        df.to_csv("filtered_time_files.csv")
        csv = pd.read_csv("filtered_time_files.csv", header=0, index_col=[0])
        os.remove("filtered_time_files.csv")
        performance_variables = csv.columns.values.tolist()
        data = {}
        for var in performance_variables:
            data[var] = []
        for row in list(csv.values):
            filter_time = False
            for (element_row, element_perf_var) in zip(row, performance_variables):
                if element_perf_var == events_time_name or element_perf_var == devices_time_name:
                    if fin_filter_time >= element_row >= init_filter_time:
                        filter_time = True
                        data[element_perf_var].append(element_row)
                else:
                    if filter_time:
                        data[element_perf_var].append(element_row)
        float_data_to_int_data(data, events_duration_time_name)
        files_to_render.append(data)
    return files_to_render
