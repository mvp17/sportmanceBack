from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt


# Create your views here.
class EventsKeyWordsView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        # user = User.objects.filter(id=payload['id']).first()
        # serializer = UserSerializer(user)

        # return Response(serializer.data)