from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import (UserCreateSerializer, UserListSerializer,
                          UserWithRecipesSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif (self.request.method == 'POST'):
            return UserCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        subscribed_to_user = get_object_or_404(User, pk=pk)
        subscriber_user = request.user

        if request.method == 'POST':

            if subscribed_to_user == subscriber_user:
                return Response(
                    {'errors': 'You cannot subscribe to yourself.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_subscription = Subscribe.objects.filter(
                subscriber=subscriber_user,
                subscribed_to=subscribed_to_user
            ).exists()
            if existing_subscription:
                return Response(
                    {'errors': 'You are already subscribed to this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            subscription = Subscribe.objects.create(
                subscriber=subscriber_user,
                subscribed_to=subscribed_to_user
            )
            serializer = UserWithRecipesSerializer(
                subscribed_to_user,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            subscription = Subscribe.objects.filter(
                subscriber=subscriber_user,
                subscribed_to=subscribed_to_user
            ).first()
            if not subscription:
                return Response(
                    {'errors': 'You are not subscribed to this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='subscriptions',
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):

        subscribed_to_users_id = Subscribe.objects.filter(
            subscriber=request.user
        ).values_list('subscribed_to', flat=True)

        subscribed_to_users = get_list_or_404(
            User, id__in=subscribed_to_users_id
        )
        paginator = self.pagination_class()
        paginated_subscribed_to_users = paginator.paginate_queryset(
            subscribed_to_users, request)

        serializer = UserWithRecipesSerializer(
            paginated_subscribed_to_users,
            context={'request': request},
            many=True
        )
        return paginator.get_paginated_response(serializer.data)
