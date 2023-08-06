from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class CreateEBSModelMixin:

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_obj = self.perform_create(serializer)
        serializer_display = self.get_serializer(model_obj)
        headers = self.get_success_headers(serializer_display.data)
        return Response(serializer_display.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateEBSModelMixin:

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer_create(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        model_obj = self.perform_update(serializer)
        serializer_display = self.get_serializer(model_obj)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer_display.data)

    def perform_update(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class GenericEBSViewSet(GenericViewSet):
    serializer_create_class = None
    permission_classes_by_action = {"default": [AllowAny]}
    action_serializers = {}
    permission_classes = None
    serializer_query_class = None

    def get_serializer_class(self):
        if self.action in self.action_serializers:
            return self.action_serializers[self.action]

        return super().get_serializer_class()

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes

            if self.permission_classes:
                return [permission() for permission in self.permission_classes]
            return [permission() for permission in self.permission_classes_by_action['default']]

    def get_serializer_create(self, *args, **kwargs):
        serializer_class = self.get_serializer_create_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_query_serializer(self):
        if self.action == ['retrieve', 'post', 'patch']:
            return None
        return self.serializer_query_class

    def get_serializer_create_class(self):
        return self.serializer_create_class if self.serializer_create_class is not None else self.serializer_class


class EBSModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    CreateEBSModelMixin,
    UpdateEBSModelMixin,
    GenericEBSViewSet
):
    pass
