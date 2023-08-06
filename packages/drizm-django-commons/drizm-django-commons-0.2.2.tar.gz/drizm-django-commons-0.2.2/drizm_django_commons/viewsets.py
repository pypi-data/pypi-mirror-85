from rest_framework.mixins import CreateModelMixin


class DetailSerializerMixin:
    serializer_detail_class = None
    queryset_detail = None

    def get_serializer_class(self):
        error_message = "" \
                        "'{0}' should include a " \
                        "'serializer_detail_class' attribute".format(
            self.__class__.__name__)
        assert self.serializer_detail_class is not None, error_message
        if self.request_is_to_detail_endpoint():
            return self.serializer_detail_class
        else:
            return super().get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        if self.request_is_to_detail_endpoint() and self.queryset_detail is not None:
            return self.queryset_detail.all()
        else:
            return super().get_queryset(*args, **kwargs)

    def request_is_to_detail_endpoint(self) -> bool:
        if hasattr(self, 'lookup_url_kwarg'):
            lookup = self.lookup_url_kwarg or self.lookup_field
        return lookup and lookup in self.kwargs


class OverwriteModelMixin(CreateModelMixin):
    def update(self, request, *args, **kwargs):
        return self.create(
            request,
            *args,
            **kwargs
        )


__all__ = ["DetailSerializerMixin", "OverwriteModelMixin"]
