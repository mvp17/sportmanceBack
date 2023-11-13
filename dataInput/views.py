from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAcceptable
from dataInput.models import DataInput
from dataInput.serializers import DataInputSerializer, FileSerializer
from utils.functions.checkData import check_auth_token


# Create your views here.
class RegisterDataInput(APIView):
    @staticmethod
    def post(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        csv_file = request.FILES['csv']
        serializer = DataInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) and csv_file.name.endswith('csv'):
            serializer.save()
            return Response(serializer.data)
        else:
            raise NotAcceptable("Should upload only csv files!")


class DeleteDataInput(APIView):
    @staticmethod
    def post(request, pk):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        file = DataInput.objects.get(pk=pk)
        if file is None:
            raise NotFound("File to delete Not Found!")
        else:
            file.delete()
            response = Response()
            response.data = {
                'message': 'File deleted successfully!'
            }
            return response


class GetAllDataFiles(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        check_auth_token(token)

        serializer = FileSerializer(DataInput.objects.all(), many=True)
        return Response(serializer.data)
