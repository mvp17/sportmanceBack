import pandas as pd
import math
# import json
from rest_framework.exceptions import NotFound, NotAcceptable, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from devicesKeyWords.models import DevicesKeyWords
from eventsKeyWords.models import EventsKeyWords
from settings.models import SessionParameters
from dataInput.models import DataInput
from utils.Functions import is_there_events_file_uploaded, is_there_devices_file_uploaded, remove_accent, \
    get_init_time_and_fin_time, swap_columns, down_sample, get_events_csv_dict, process_device_data, \
    filter_time_files, process_csv_values


# Create your views here.
class GetDataToAnalyseView(APIView):
    @staticmethod
    def get(request):
        perf_vars = []
        data_files = DataInput.objects.all()

        if data_files.count() == 0:
            raise NotFound("Data files not uploaded. Not Found!")
        elif DevicesKeyWords.objects.count() == 0 and is_there_devices_file_uploaded(data_files):
            raise NotAcceptable("No devices file key words registered, although there is/are devices file/s uploaded!")
        elif EventsKeyWords.objects.count() == 0 and is_there_events_file_uploaded(data_files):
            raise NotAcceptable("No events file key words registered, although there is events file uploaded!")
        elif SessionParameters.objects.count() == 0:
            raise NotFound("Settings Not Found!")
        else:
            frequency_data_table = SessionParameters.load().frequency
            init_time = SessionParameters.load().init_time_ms
            fin_time = SessionParameters.load().fin_time_ms
            time_ms_name_events_file = ""
            duration_time_ms_name_events_file = ""
            time_name_devices_file = ""
            if EventsKeyWords.objects.count() == 1 and is_there_events_file_uploaded(data_files):
                time_ms_name_events_file = EventsKeyWords.load().time_ms_name
                duration_time_ms_name_events_file = EventsKeyWords.load().duration_time_ms_name
            if DevicesKeyWords.objects.count() == 1 and is_there_devices_file_uploaded(data_files):
                time_name_devices_file = DevicesKeyWords.load().time_name
            dict_devices = []
            dict_down_sampled_files = []

            for obj in data_files:
                data = {}
                remove_accent(obj.csv.name)
                csv = pd.read_csv(obj.csv.name, ";")
                performance_variables = csv.columns.values.tolist()

                for perf_var in performance_variables:
                    data[perf_var.replace(" ", "_")] = []

                if obj.event_file == 0:
                    file_init_time, file_fin_time, event_file_dict = process_csv_values(
                                                                        csv, data, obj, time_ms_name_events_file,
                                                                        duration_time_ms_name_events_file)

                    if not (fin_time <= file_fin_time and init_time >= file_init_time):
                        raise MethodNotAllowed("It is not possible to analyse data with the settings time parameters. "
                                               "Please re-enter the 'settings time parameters.")

                    dict_down_sampled_files.append(swap_columns(
                        down_sample(event_file_dict, frequency_data_table,
                                    time_ms_name_events_file, time_name_devices_file),
                        time_ms_name_events_file)
                    )
                else:
                    for row in csv.values.tolist():
                        for (element_row, element_perf_var) in zip(row, performance_variables):
                            data[element_perf_var.replace(" ", "_")].append(element_row)
                    if is_there_events_file_uploaded(data_files):
                        events_csv_dict = get_events_csv_dict(data_files)
                        value = events_csv_dict.get(time_ms_name_events_file)[0]
                        dict_devices.append(process_device_data(data, value, obj.frequency, time_name_devices_file))
                    else:
                        dict_devices.append(process_device_data(data, 0, obj.frequency, time_name_devices_file))

            for device_data in dict_devices:
                file_init_time, file_fin_time = get_init_time_and_fin_time(device_data, time_name_devices_file)

                if not (fin_time <= file_fin_time and init_time >= file_init_time):
                    raise MethodNotAllowed("It is not possible to analyse data with the settings time parameters. "
                                           "Please re-enter the 'settings time parameters.")

                dict_down_sampled_files.append(down_sample(device_data, frequency_data_table, time_ms_name_events_file,
                                                           time_name_devices_file))

            render_data_files = filter_time_files(dict_down_sampled_files,
                                                  SessionParameters.load().init_time_ms,
                                                  SessionParameters.load().fin_time_ms, time_ms_name_events_file,
                                                  duration_time_ms_name_events_file, time_name_devices_file)
            for file in render_data_files:
                for value in file.values():
                    for element in value:
                        if isinstance(element, float) and math.isnan(element):
                            value[value.index(element)] = 'null'

            for file in render_data_files:
                for key in file.keys():
                    if key not in perf_vars:
                        perf_vars.append(key)

            response = Response()
            response.data = {
                'perf_vars': perf_vars,
                'dict_csv_files': render_data_files  # json.dumps(render_data_files)
            }
            return response
