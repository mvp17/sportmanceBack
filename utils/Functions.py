import pandas as pd
import os
import math
import unidecode


def is_there_events_file_uploaded(objects):
    for obj in objects:
        if obj.event_file == 0:
            return True
    return False


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
        csv = pd.read_csv(obj.csv.name, ";")
        performance_variables = csv.columns.values.tolist()

        for perf_var in performance_variables:
            data[perf_var.replace(" ", "_")] = []

        if obj.event_file == 0:
            for row in csv.values.tolist():
                for (element_row, perf_var) in zip(row, performance_variables):
                    data[perf_var.replace(" ", "_")].append(element_row)

    return data


def is_there_devices_file_uploaded(objects):
    for obj in objects:
        if obj.event_file == 1:
            return True
    return False


def remove_accent(feed):
    csv_f = open(feed, encoding='latin-1', mode='r')
    csv_str = csv_f.read()
    csv_str_removed_accent = unidecode.unidecode(csv_str)
    csv_f.close()
    csv_f = open(feed, 'w')
    csv_f.write(csv_str_removed_accent)


# Frequency target 1000 Hz.
def process_event_data(csv_dict, curr_frequency, events_time_name, events_duration_time_name):
    float_data_to_int_data(csv_dict, events_duration_time_name)
    time_lasting = csv_dict[events_duration_time_name]
    time = csv_dict[events_time_name]
    first_time = time[0]
    last_time = time[-1]

    # Hesitation here
    limit = int(round(last_time/1000))*1000
    if limit < last_time:
        limit = last_time
    # if (time_lasting[-1] + last_time) != limit + first_time:
    time_lasting[-1] = limit + first_time - last_time

    # Maximum re-sample = 1000 Hz
    return max_re_sample(csv_dict, curr_frequency, time_lasting, 0, events_time_name, events_duration_time_name)


def float_data_to_int_data(csv_dict, events_duration_time_name):
    keys_floats = {}
    # Handle float numbers except nan
    for key in csv_dict.keys():
        for value in csv_dict[key]:
            if isinstance(value, float):
                if key not in keys_floats.keys() and not math.isnan(value):
                    keys_floats[key] = []
                if key in keys_floats.keys():
                    if math.isnan(value):
                        # If a value list (column) from the csv has a NaN value
                        # and that column is the duration time (milliseconds), change it to value 0 because it matters
                        # above the others. The other NaN values of the csv will be changed to 'null' value.
                        if key == events_duration_time_name:
                            keys_floats[key].append(0)
                        else:
                            keys_floats[key].append(value)
                    else:
                        keys_floats[key].append(int(math.floor(value)))

    for key in keys_floats:
        csv_dict[key] = keys_floats[key]


# Frequency target 1000 Hz.
def process_device_data(data_to_csv, value_first_time, curr_frequency, time_name):
    new_array_time = []
    length_new_array = 0

    if curr_frequency == 100:
        length_new_array = int(len(data_to_csv.get(time_name))/curr_frequency)*1000+value_first_time
        for time in range(value_first_time, int(round(length_new_array)), 10):
            new_array_time.append(time)
    elif curr_frequency == 10:
        length_new_array = int(len(data_to_csv.get(time_name))/curr_frequency)*1000+value_first_time
        for time in range(value_first_time, int(length_new_array) + 100, 100):
            new_array_time.append(time)
    data_to_csv[time_name] = new_array_time

    # Maximum re-sampling = 1000 Hz
    return max_re_sample(data_to_csv, curr_frequency, None, length_new_array, time_name, None)


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
        for row in csv.values.tolist():
            for (element_row, element_perf_var) in zip(row, performance_variables):
                data[element_perf_var].append(element_row)
    else:
        interpol_events(data, csv, performance_variables, time_lasting, time_name, events_duration_time_name)
    return data


def interpol_events(data, csv, perf_vars, time_lasting, events_time_name, events_duration_time_name):
    for row, time in zip(csv.values.tolist(), time_lasting):
        for (element_row, element_perf_var) in zip(row, perf_vars):
            if isinstance(element_row, int) and element_perf_var == events_time_name:
                extreme_time_value_to_interpolate = element_row
                # Interpolate time
                for new_time in range(extreme_time_value_to_interpolate, time + extreme_time_value_to_interpolate):
                    data[element_perf_var].append(new_time)
            else:
                # Interpolate str value
                for str_value in range(time):
                    data[element_perf_var].append(element_row)
    float_data_to_int_data(data, events_duration_time_name)


def interpol_devices(data, csv, perf_vars, interpol_value, limit_length):
    extreme_time_value_to_interpolate = 0
    for row in csv.values.tolist():
        for (element_row, element_perf_var) in zip(row, perf_vars):
            if isinstance(element_row, int):
                extreme_time_value_to_interpolate = element_row
            if not (extreme_time_value_to_interpolate + interpol_value > limit_length):
                if not isinstance(element_row, int):
                    for str_value in range(interpol_value):
                        # Interpolate value str
                        data[element_perf_var].append(element_row)
                if isinstance(element_row, int):
                    # Interpolate time
                    for time in range(extreme_time_value_to_interpolate,
                                      extreme_time_value_to_interpolate + interpol_value):
                        data[element_perf_var].append(time)
