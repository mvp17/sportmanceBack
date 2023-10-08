from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, NotFound
from eventsKeyWords.serializers import EventsKeyWordsSerializer
from dataInput.models import DataInput
from utils.Functions import get_performance_variables_from_object_file, is_there_events_file_uploaded


# Create your views here.
class RegisterEventsKeyWordsView(APIView):
    @staticmethod
    def post(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        serializer = EventsKeyWordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetPerformanceVariablesFromEventsFile(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        data_files = DataInput.objects.all()
        if data_files.count() == 0:
            raise NotFound("Data files not uploaded. Not Found!")
        else:
            if is_there_events_file_uploaded(data_files):
                context_perf_vars = get_performance_variables_from_object_file(0, data_files)
            else:
                raise NotFound("There are not devices files uploaded. Not Found!")

        response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'performance_vars': context_perf_vars
        }
        return response
