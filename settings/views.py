import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from eventsKeyWords.models import EventsKeyWords
from devicesKeyWords.models import DevicesKeyWords
from dataInput.models import DataInput
from settings.serializers import SettingsSerializer
from utils.functions.checkData import is_there_events_file_uploaded
from utils.functions.getData import get_init_time_and_fin_time_from_events_file, get_events_csv_dict, \
    get_init_time_and_fin_time
from utils.functions.processFile import remove_accent
from utils.functions.resample import process_device_data


# Create your views here.
class RegisterSettingsView(APIView):
    @staticmethod
    def post(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetInitAndFinTimesView(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        data_input_files = DataInput.objects.all()
        context_init_time = 0
        context_fin_time = 0
        time_ms_name_events_file = ""
        duration_time_ms_name_events_file = ""
        time_name_devices_file = ""

        if EventsKeyWords.objects.count() == 1:
            time_ms_name_events_file = EventsKeyWords.load().time_ms_name
            duration_time_ms_name_events_file = EventsKeyWords.load().duration_time_ms_name
        if DevicesKeyWords.objects.count() == 1:
            time_name_devices_file = DevicesKeyWords.load().time_name

        for obj in data_input_files:
            remove_accent(obj.csv.name)
            csv = pd.read_csv(obj.csv.name, sep=';')
            performance_variables = csv.columns.values.tolist()
            data = {}

            for perf_var in performance_variables:
                data[perf_var.replace(" ", "_")] = []

            if obj.is_event_file:
                context_init_time, context_fin_time, _ = get_init_time_and_fin_time_from_events_file(
                                                            csv, data, obj, time_ms_name_events_file,
                                                            duration_time_ms_name_events_file)
            else:
                for row in list(csv.values):
                    for (element_row, perf_var) in zip(row, performance_variables):
                        data[perf_var.replace(" ", "_")].append(element_row)

                if is_there_events_file_uploaded(data_input_files):
                    events_csv_dict = get_events_csv_dict(data_input_files)
                    value = events_csv_dict.get(time_ms_name_events_file)[0]
                    file_dict = process_device_data(data, value, obj.frequency, time_name_devices_file)
                    context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_name_devices_file)
                else:
                    file_dict = process_device_data(data, 0, obj.frequency, time_name_devices_file)
                    context_init_time, context_fin_time = get_init_time_and_fin_time(file_dict, time_name_devices_file)

        response = Response()
        response.data = {
            'initTime': context_init_time,
            'finTime': context_fin_time
        }
        return response
