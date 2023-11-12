import unidecode
import math


def remove_accent(feed):
    csv_f = open(feed, encoding='latin-1', mode='r')
    csv_str = csv_f.read()
    csv_str_removed_accent = unidecode.unidecode(csv_str)
    csv_f.close()
    csv_f = open(feed, 'w')
    csv_f.write(csv_str_removed_accent)


def swap_columns(old_dict, time_name):
    # In the EVENTS file put the time in milliseconds column in the first place of the csv,
    # in order to do the time filter well.
    new_dict = {}

    for key in old_dict.keys():
        if key == time_name:
            new_dict[key] = old_dict[key]
            del old_dict[key]
            break

    for key in old_dict.keys():
        new_dict[key] = old_dict[key]

    return new_dict


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
