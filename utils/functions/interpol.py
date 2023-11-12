from utils.functions.processFile import float_data_to_int_data


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