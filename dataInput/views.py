from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, NotFound, NotAcceptable
from dataInput.models import DataInput
from dataInput.serializers import DataInputSerializer


# Create your views here.
class RegisterDataInput(APIView):
    @staticmethod
    def post(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")
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
        if not token:
            raise AuthenticationFailed("Unauthenticated")

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
