import math
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView
from dataInput.models import DataInput
from eventsKeyWords.models import EventsKeyWords
from utils.functions.checkData import is_there_events_file_uploaded
from utils.functions.getData import get_events_csv_dict
from utils.functions.processFile import float_data_to_int_data
from utils.functions.checkData import check_auth_token


# Create your views here.
class GetChartData(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        data_files = DataInput.objects.all()

        if not is_there_events_file_uploaded(data_files):
            raise NotFound("No events file uploaded. Not Found!")
        elif EventsKeyWords.objects.count() == 0 and is_there_events_file_uploaded(data_files):
            raise NotAcceptable("No events file key words known, although there is events file uploaded.")
        else:
            lists_labels, lists_data, chart_vars = get_info_chart(data_files)
            lists_labels = to_format_csv(lists_labels)

            response = Response()
            response.data = {
                'datasource': lists_data,
                'labels': lists_labels,
                'chartVars': chart_vars
            }
            return response


# Data of which perf variables as key words for events file
def get_info_chart(data_files):
    events_data = get_events_csv_dict(data_files)
    chart_perf_vars = ""
    duration_time_name_events_ms = ""

    if EventsKeyWords.objects.count() == 1 and is_there_events_file_uploaded(data_files):
        chart_perf_vars = EventsKeyWords.load().chart_perf_vars
        duration_time_name_events_ms = EventsKeyWords.load().duration_time_ms_name

    float_data_to_int_data(events_data, duration_time_name_events_ms)

    # Worst case
    chart_perf_vars = chart_perf_vars.replace(" ", "")
    perf_vars = chart_perf_vars.split(",")
    sub_events = {}

    for key in events_data.keys():
        if key in perf_vars:
            sub_events[key] = events_data[key]

    labels_and_data = get_data_and_labels(sub_events.values())
    labels, data = split_labels_data(labels_and_data)

    return labels, data, perf_vars


def get_data_and_labels(elements):
    different_values = {}
    labels_data = []

    for element in elements:
        for value in element:
            if value not in different_values:
                # Don't count with the NaN values
                if isinstance(value, float) and math.isnan(value):
                    continue
                different_values[value] = 1
            else:
                different_values[value] += 1
        labels_data.append(different_values)
        different_values = {}

    return labels_data


def split_labels_data(labels_and_data):
    labels_list = []
    data_list = []
    labels = []
    data = []

    for element in labels_and_data:
        for key in element.keys():
            labels.append(key)
        labels_list.append(labels)
        labels = []

        for value in element.values():
            data.append(value)
        data_list.append(data)
        data = []

    return labels_list, data_list


def to_format_csv(labels_list):
    formatted_labels_list = []
    formatted_labels = []

    for label_list in labels_list:
        for label in label_list:
            if isinstance(label, str):
                if ',' in label:
                    label = label.replace(',', '.')
                    formatted_labels.append(label)
                else:
                    formatted_labels.append(label)
            else:
                formatted_labels.append(label)
        formatted_labels_list.append(formatted_labels)
        formatted_labels = []
    return formatted_labels_list
