from django.db.models import QuerySet
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from w.services.abstract_model_service import AbstractModelService


class SerializerViewSetMixin:
    serializers = {"default": None}

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_key = kwargs.pop("serializer_key", None)
        serializer_class = self.get_serializer_class(serializer_key)
        return serializer_class(*args, **kwargs)

    @classmethod
    def get_serializer_by_key(cls, key):
        """
        Args:
            key: serializer key

        Returns:
            Serializer
        """
        return cls.serializers.get(key, cls.serializers["default"])

    def get_serializer_class(self, serializer_key=None):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)

        Returns:
            Serializer: Drf or Serpy
        """
        serializer_key = serializer_key if serializer_key else self.action  # noqa
        return self.get_serializer_by_key(serializer_key)


class ViewSet(SerializerViewSetMixin, viewsets.ViewSet):
    def get_action(self):
        # noinspection PyUnresolvedReferences
        return self.action_map.get(self.request.method.lower())

    def get_response(self, data, **params) -> Response:
        """
        Get response from data.

        Automatically serialize data from action name or parameter serializer_key

        Args:
            data(mixed): data to return in response
            **params:
                - serializer_key: serializer to use (default: action name)
                - status_code: default is status.HTTP_200_OK

        Returns:
            Response
        """
        default = {
            "serializer_key": None,
            "status_code": status.HTTP_200_OK,
        }
        params = {**default, **params}
        serializer_class = self.get_serializer_class(params["serializer_key"])
        many = isinstance(data, list)
        serializer = serializer_class(data, many=many)

        return Response(serializer.data, status=params.get("status"))

    def get_validated_data(self, serializer_key=None):
        """
        Validate request data (throw exception if invalid) and return validated data

        Args:
            serializer_key(None|str): serializer to use,
                default is "<action name>_validation"

        Returns:
            dict
        """
        if serializer_key is None:
            serializer_key = f"{self.action}_validation"
        serializer_class = self.get_serializer_class(serializer_key)
        serializer = serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def get_error_validation_response(error: ValidationError):
        """
        Build validation error response with status code of 422 and
        by keeping only first validation message
        """
        data = {}
        for attr, errors in error.detail.items():
            data[attr] = str(errors[0])
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GenericViewSet(SerializerViewSetMixin, viewsets.GenericViewSet):
    service: AbstractModelService

    """
    A viewset using w.drf.serializer.SerpySerializer.get_optimized_queryset for list
    and retrieve action

    To use it, override the class and set the `.queryset` and `.serializers` attributes
    """

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(
            *args, context=self.get_serializer_context(), **kwargs
        )

    def get_queryset(self):
        """
        Get optimized queryset for retrieve or list action

        Returns:
            QuerySet
        """
        queryset = super().get_queryset()
        if self.action in ("retrieve", "list"):
            serializer = self.get_serializer_class()
            return serializer.get_optimized_queryset(queryset).all()
        return queryset.all()

    def get_optimized_queryset(self, serializer_key) -> QuerySet:
        """
        Get viewset optimized queryset for a serializer to enhance serialization
        performance

        Args:
            serializer_key(str): serializer key

        Returns:
            QuerySet
        """
        queryset = super().get_queryset()
        serializer = self.get_serializer_class(serializer_key)
        return serializer.get_optimized_queryset(queryset).all()

    def get_response(self, **params):
        """
        Build response

        Args:
            **params:
                instance: default: None,
                queryset": default: None,
                serializer_key: default: None,
                status_code: default: status.HTTP_200_OK

        Returns:

        """
        default = {
            "instance": None,
            "queryset": None,
            "serializer_key": None,
            "status_code": status.HTTP_200_OK,
        }
        params = {**default, **params}
        serializer_class = self.get_serializer_class(params["serializer_key"])
        if params["instance"]:
            serializer = serializer_class(params["instance"])
        else:
            queryset = params.get("queryset")
            if queryset is None:
                queryset = super().get_queryset()
            optimized_queryset = serializer_class.get_optimized_queryset(queryset)
            if self.request.query_params:
                optimized_queryset = optimized_queryset.filter(
                    **self.request.query_params.dict()
                )
            else:
                optimized_queryset = optimized_queryset.all()
            serializer = serializer_class(optimized_queryset, many=True)
        return Response(serializer.data, status=params.get("status"))

    def get_post_response(self, instance, serializer_key=None) -> Response:
        """
        Build post response from instance

        Args:
            instance(Model): model instance created
            serializer_key(str|None): override action serializer

        Returns:
            Response
        """
        return self.get_response(
            instance=instance,
            serializer_key=serializer_key,
            status=status.HTTP_201_CREATED,
        )

    def get_delete_response(self, instance=None, serializer_key=None) -> Response:
        """
        Build delete response from instance

        Returns:
            Response
        """
        if instance:
            return self.get_response(instance=instance, serializer_key=serializer_key)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions and the ability to define a
    test serializer class.

    To use it, override the class and set the `.queryset` and `.serializers` attributes.
    """

    pass
