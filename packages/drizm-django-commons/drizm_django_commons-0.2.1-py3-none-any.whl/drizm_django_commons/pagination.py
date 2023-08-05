from rest_framework.pagination import (
    LimitOffsetPagination,
    _positive_int  # noqa access to protected
)
from typing import ClassVar

from rest_framework.response import Response
from rest_framework import status


class MaxLimitOffsetPagination(LimitOffsetPagination):
    max_page_size: ClassVar[int] = 100

    def get_limit(self, request) -> int:
        if self.limit_query_param:
            try:
                param = request.query_params[self.limit_query_param]
            except KeyError:
                return self.default_limit

            try:
                amount = int(param)
            except ValueError:
                amount = param
                if type(amount) == str and amount == "max":
                    amount = self.max_limit
                else:
                    return self.default_limit
            return _positive_int(
                amount,
                strict=True,
                cutoff=self.max_limit
            )

    def get_paginated_response(self, data) -> Response:
        default = super(
            MaxLimitOffsetPagination, self
        ).get_paginated_response(data)
        default.status_code = status.HTTP_206_PARTIAL_CONTENT
        default.data["prev"] = default.data.pop("previous")
        return default

    def get_paginated_response_schema(self, schema) -> dict:
        default = super(
            MaxLimitOffsetPagination, self
        ).get_paginated_response_schema(schema)
        previous = default["properties"].pop("previous")
        default["properties"]["prev"] = previous
        return default
