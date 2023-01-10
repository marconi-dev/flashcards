from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserCreateSerializer



# Create your views here.
@api_view(['POST'])
def user_apiview(request, *args, **kwargs):
    """
    Cria um usuario com os dados informados
    """
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    