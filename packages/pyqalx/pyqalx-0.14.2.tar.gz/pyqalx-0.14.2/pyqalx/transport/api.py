from .core import BasePyQalxAPI, PyQalxAPIException


class PyQalxAPI(BasePyQalxAPI):
    def get(self, endpoint, **kwargs):
        """
        Performs a GET request to the specified endpoint
        :param endpoint: The endpoint you want to query: 'item/<item_guid>'
        :param kwargs: Any arguments you want to pass to the request:
                json={'data': 'filter__by=gte=4, 'limit':5, 'sort':<sort>, }
        :return: response
        """
        url = self._get_url(endpoint)
        if kwargs.get("data", None) and kwargs.get("params", None):
            # They have supplied params and data.  Raise an exception as we
            # can't safely merge them
            raise PyQalxAPIException(
                "qalx GET parameters must be supplied"
                "using the `params` parameter for API"
                "consistency"
            )
        data_removed = kwargs.pop("data", None)
        if data_removed and kwargs.get("params") is None:
            # For API consistency the `params` for a query are stored on `data`
            # but need to be moved to `params` for the request. Any user using
            # the transport layer on its own can send either `data` or `params`.
            # The querystring cannot be in the request body
            kwargs["params"] = data_removed
        return self._build_request(url=url, method="GET", **kwargs)

    def post(self, endpoint, **kwargs):
        """
        Performs a POST request to the specified endpoint
        :param endpoint: The endpoint you want to query: 'item'
        :param kwargs: Any data you want to pass to the request.
        :return: response
        """
        return self._build_non_safe_request(
            method="POST", endpoint=endpoint, **kwargs
        )

    def patch(self, endpoint, **kwargs):
        """
        Performs a PATCH request to the specified endpoint
        :param endpoint: The endpoint you want to query: 'item/<item_guid>'
        :param kwargs: Any data you want to pass to the request.
        :return: response
        """
        return self._build_non_safe_request(
            method="PATCH", endpoint=endpoint, **kwargs
        )

    def put(self, endpoint, **kwargs):
        """
        Performs a PUT request to the specified endpoint
        :param endpoint: The endpoint you want to query: 'item/<item_guid>'
        :param kwargs: Any data you want to pass to the request.
        :return: response
        """
        return self._build_non_safe_request(
            method="PUT", endpoint=endpoint, **kwargs
        )

    def delete(self, endpoint, **kwargs):
        """
        Performs a DELETE request to the specified endpoint
        :param endpoint: The endpoint you want to query: 'item/<item_guid>'
        """
        url = self._get_url(endpoint)
        return self._build_request(url=url, method="DELETE")
