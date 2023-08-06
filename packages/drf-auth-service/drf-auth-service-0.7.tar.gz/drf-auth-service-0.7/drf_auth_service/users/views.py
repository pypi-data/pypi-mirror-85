from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from rest_framework.response import Response

from drf_auth_service.common.managers import BaseManager
from drf_auth_service.common.mixins import GenericEBSViewSet, UpdateEBSModelMixin
from drf_auth_service.models import ActivationCode, UserBlock
from drf_auth_service.settings import User
from drf_auth_service.settings import settings


class UserViewSet(
    GenericEBSViewSet,
    DestroyModelMixin,
    UpdateEBSModelMixin,
    ListModelMixin
):
    queryset = User.objects.all()
    serializer_class = settings.SERIALIZERS.USER_RETURN_SERIALIZER
    serializer_create_class = settings.SERIALIZERS.USER_SERIALIZER
    permission_classes_by_action = settings.PERMISSIONS.USER_PERMISSIONS

    @action(detail=False, methods=['POST'], serializer_create_class=settings.SERIALIZERS.USER_CONFIRM_SERIALIZER,
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER, url_path='confirm')
    def user_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password_token = serializer.validated_data['token']
        ActivationCode.make_user_active(reset_password_token.user)
        return Response(self.get_serializer(dict(message='User was successfully confirmed')).data)

    @action(detail=False, methods=['PATCH'], url_path='resend-confirmation',
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER,
            serializer_create_class=settings.SERIALIZERS.USER_IDENTIFIER)
    def resend_confirmation(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user_by_username(serializer.validated_data['username'])
        manager = BaseManager.load_manager(user, configs=None, request=request)
        manager.send_confirmation(user)
        return Response(self.get_serializer(dict(message='Confirmation was resent successfully')).data)

    @action(detail=False, methods=['POST'], url_path='block',
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER,
            serializer_create_class=settings.SERIALIZERS.BLOCK_USER_SERIALIZER)
    def block_user(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user_by_username(serializer.validated_data['username'])
        UserBlock.objects.create(reason=serializer.validated_data['reason'], user=user)
        return Response(
            self.get_serializer(dict(message=f"User {serializer['user'].username} was successfully blocked")).data
        )

    @action(detail=False, methods=['PATCH'], url_path='unblock',
            serializer_create_class=settings.SERIALIZERS.USER_IDENTIFIER,
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER)
    def unblock_user(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user_by_username(serializer.validated_data['username'])
        user.block.delete()
        return Response(
            self.get_serializer(dict(message=f"User {user.username} was successfully unblocked")).data
        )

    @action(detail=False, methods=['PATCH'], serializer_create_class=settings.SERIALIZERS.SET_PASSWORD_SERIALIZER,
            serializer_class=settings.SERIALIZERS.RETURN_SUCCESS_SERIALIZER, url_path='set-password')
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user_by_username(serializer.validated_data['username'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(
            self.get_serializer(dict(
                message=f"Password for user {user.username} was successfully set")).data
        )

    def get_queryset(self):
        if getattr(self.request, 'service', None):
            return super().get_queryset().filter(service=self.request.service)
        return super().get_queryset()

    @staticmethod
    def get_user_by_username(username):
        user = User.objects.filter(username=username).first()

        if user is None:
            raise ValidationError(dict(username='User does not exist'))

        return user
