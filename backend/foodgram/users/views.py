from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .models import User, Subscription
from .serializers import (SetPasswordSerializer, UserReadSerializer,
                          UserCreateSerializer)
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .mixins import CreateDestroyListViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'user_id'
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'retrieve' or self.action_map['get'] == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return UserReadSerializer
        else:
            return UserCreateSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user_byemail = User.objects.filter(email=email)
        user_byname = User.objects.filter(username=username)
        if user_byemail.exists() or user_byname.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        user = request.user
        serializer = UserReadSerializer(
            user, context={'request': self.request})
        return Response(
            data=serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                serializer.data.get("current_password")
            ):
                return Response({"current_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['user_id'])
        serializer = UserReadSerializer(
            user, context={'request': self.request}
        )
        return Response(serializer.data)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserReadSerializer(
            queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class SubscriptionsViewSet(CreateDestroyListViewSet):
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        publishers = User.objects.filter(publishers__user=user)
        serializer = SubscriptionSerializer(
            publishers, many=True, context={'request': request})
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    def create(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if request.user.id != author.id:
            Subscription.objects.create(author=author, user=request.user)
        serializer = UserReadSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        get_object_or_404(
            Subscription, author=author, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
