from rest_framework import viewsets, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters, status, viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user_byemail = User.objects.filter(email=email)
        user_byname = User.objects.filter(username=username)
        if user_byemail.exists() or user_byname.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # @action(
    #     methods=['get', 'patch', ],
    #     detail=False,
    #     # permission_classes=[IsAuthenticated, ]
    # )

    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)
        # if request.method == 'PATCH':
        #     serializer = UserSerializerRead(
        #         user, data=request.data, partial=True)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(
        #         data=serializer.data, status=status.HTTP_200_OK)