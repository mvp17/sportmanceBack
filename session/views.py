from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from devicesKeyWords.models import DevicesKeyWords
from eventsKeyWords.models import EventsKeyWords
from settings.models import SessionParameters
from utils.functions.checkData import check_auth_token


# Create your views here.
class ExitSession(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        is_there_settings = 0
        if EventsKeyWords.objects.count() == 1 or DevicesKeyWords.objects.count() == 1 or \
                SessionParameters.objects.count() == 1:
            is_there_settings = 1

        response = Response()
        response.data = {
            'is_there_settings': is_there_settings,
        }
        return response


class DeleteSessionData(APIView):
    @staticmethod
    def post(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        EventsKeyWords.load().delete()
        DevicesKeyWords.load().delete()
        SessionParameters.load().delete()

        response = Response()
        response.data = {
            'message': 'Session data deleted successfully!'
        }
        return response


class GetSessionData(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        init_time = 0
        fin_time = 0
        frequency = 0
        is_there_settings = 0
        is_there_key_words_events = 0
        is_there_key_words_devices = 0
        is_there_chart_perf_vars = 0
        time_ms_name_events = ""
        duration_time_ms_name_events = ""
        chart_perf_vars = ""
        time_name_devices = ""

        if SessionParameters.objects.count() == 1:
            is_there_settings = 1
            frequency = SessionParameters.load().frequency
            init_time = SessionParameters.load().init_time_ms
            fin_time = SessionParameters.load().fin_time_ms
        if EventsKeyWords.objects.count() == 1:
            is_there_key_words_events = 1
            time_ms_name_events = EventsKeyWords.load().time_ms_name
            duration_time_ms_name_events = EventsKeyWords.load().duration_time_ms_name
            if EventsKeyWords.load().chart_perf_vars is None or not EventsKeyWords.load().chart_perf_vars:
                is_there_chart_perf_vars = 1
            else:
                chart_perf_vars = EventsKeyWords.load().chart_perf_vars
        if DevicesKeyWords.objects.count() == 1:
            is_there_key_words_devices = 1
            time_name_devices = DevicesKeyWords.load().time_name

        response = Response()
        response.data = {
            'init_time': init_time,
            'fin_time': fin_time,
            'frequency': frequency,
            'is_there_settings': is_there_settings,
            'time_ms_name_events': time_ms_name_events,
            'duration_time_ms_name_events': duration_time_ms_name_events,
            'chart_perf_vars': chart_perf_vars,
            'time_name_devices': time_name_devices,
            'is_there_key_words_events': is_there_key_words_events,
            'is_there_key_words_devices': is_there_key_words_devices,
            'is_there_chart_perf_vars': is_there_chart_perf_vars
        }
        return response
