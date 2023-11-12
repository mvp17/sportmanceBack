from utils.functions.maxResample import max_re_sample
from utils.functions.processFile import float_data_to_int_data


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
