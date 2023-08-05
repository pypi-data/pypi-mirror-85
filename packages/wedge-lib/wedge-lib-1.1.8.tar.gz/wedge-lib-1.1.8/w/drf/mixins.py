from rest_framework import mixins
from rest_framework.exceptions import ValidationError

from w.drf.viewsets import GenericViewSet
from w.services.abstract_model_service import AbstractModelService


class CreateModelMixin(mixins.CreateModelMixin):
    service: AbstractModelService

    def check_is_valid(self: GenericViewSet):
        try:
            validated_data = self.get_validated_data()
        except ValidationError as e:
            return self.get_error_validation_response(e)
        return validated_data

    def create(self, request, *args, **kwargs):
        instance = self.service.create(**self.check_is_valid())
        return self.get_post_response(instance)

    def get_post_response(self: GenericViewSet, instance):
        return self.get_post_response(instance)


class ListModelMixin(mixins.ListModelMixin):
    pass


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    pass


class UpdateModelMixin(mixins.UpdateModelMixin):
    pass


class DestroyModelMixin(mixins.DestroyModelMixin):
    pass
