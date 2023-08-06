from typing import Dict, Any, Optional

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch
from rest_framework import serializers
from rest_framework.relations import Hyperlink


class SelfHrefField(serializers.HyperlinkedIdentityField):
    def __init__(self, view_name=None, **kwargs):
        if not view_name and hasattr(self.parent, "Meta"):
            view_name = getattr(self.parent.Meta, "self_view")
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(view_name, **kwargs)

    def _get_url_representation(self,
                                value: Any,
                                view_name: Optional[str] = None
                                ) -> Optional[str]:
        assert "request" in self.context, (
                "`%s` requires the request in the serializer"
                " context. Add `context={'request': request}` when instantiating "
                "the serializer." % self.__class__.__name__
        )

        request = self.context["request"]
        format_ = self.context.get("format", None)

        if format_ and self.format and self.format != format_:
            format_ = self.format

        try:
            reverse_view = view_name or self.view_name
            url = self.get_url(value, reverse_view, request, format_)
        except NoReverseMatch:
            msg = (
                "Could not resolve URL for hyperlinked relationship using "
                "view name '%s'. You may have failed to include the related "
                "model in your API, or incorrectly configured the "
                "`lookup_field` attribute on this field."
            )
            if value in ("", None):
                value_string = {"": "the empty string", None: "None"}[value]
                msg += (
                        " WARNING: The value of the field on the model instance "
                        "was %s, which may be why it didn't match any "
                        "entries in your URL conf." % value_string
                )
            raise ImproperlyConfigured(msg % self.view_name)

        if url is None:
            return None

        return Hyperlink(url, value)

    def to_representation(self, value) -> Dict[str, str]:
        url = self._get_url_representation(
            value, self.view_name
        )
        return {"href": url}
