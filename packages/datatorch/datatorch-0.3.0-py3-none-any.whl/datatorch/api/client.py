from typing import List, Union

from gql import Client as GqlClient, gql
from gql.transport.transport import Transport
from gql.transport.websockets import WebsocketsTransport
from gql.transport.requests import RequestsHTTPTransport
from graphql.language.ast import DocumentNode

from datatorch.utils import normalize_api_url
from datatorch.core import user_settings
from typing import Any, TypeVar, Type


T = TypeVar("T")


__all__ = "Client"


def _create_transport(
    url: str, use_sockets: bool = False
) -> Union[WebsocketsTransport, RequestsHTTPTransport]:
    if use_sockets:
        url = url.replace("http", "ws", 1)
        return WebsocketsTransport(headers={}, url=url)
    return RequestsHTTPTransport(headers={}, use_json=True, url=url)


class Client(object):
    """ Wrapper for the DataTorch API including GraphQL and uploading """

    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        use_sockets: bool = False,
    ):
        self.client = None
        self._use_sockets = use_sockets
        self.api_url = api_url or user_settings.api_url
        self.transport = _create_transport(self.graphql_url, use_sockets=use_sockets)
        self.client = GqlClient(
            transport=self.transport, fetch_schema_from_transport=True
        )
        self.api_key = api_key or user_settings.api_key

    @property
    def api_key(self) -> Union[str, None]:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        headers = self.transport.headers
        if self.client and isinstance(headers, dict):
            assert self.api_key is not None, "Invalid API Key"
            headers["datatorch-api-key"] = self.api_key

    @property
    def api_url(self) -> Union[str, None]:
        return self._api_url

    @api_url.setter
    def api_url(self, value):
        self._api_url = normalize_api_url(value)
        if self.client:
            self.transport.url = self.graphql_url

    @property
    def graphql_url(self) -> str:
        url = f"{self.api_url}/graphql"
        if self._use_sockets:
            url = url.replace("http", "ws")
        return url

    def execute_files(
        self, paths: List[str], *args, params: dict = {}, **kwargs
    ) -> dict:
        """ Combine and excute query of multiple GraphQL files """
        query = ""
        for path in paths:
            with open(path) as f:
                query += f.read()
        return self.execute(query, *args, params=params, **kwargs)

    def execute_file(self, path: str, *args, params: dict = {}, **kwargs) -> dict:
        """ Excute query from GraphQL file """
        with open(path) as f:
            return self.execute(f.read(), *args, params=params, **kwargs)

    def execute(
        self, query: Union[DocumentNode, str], *args, params: dict = {}, **kwargs
    ) -> dict:
        """ Wrapper around execute """
        removed_none = dict((k, v) for k, v in params.items() if v is not None)
        query_doc = gql(query) if isinstance(query, str) else query
        return self.client.execute(
            query_doc, *args, variable_values=removed_none, **kwargs
        )

    def query_to_class(
        self, Entity: Type[T], query: str, path: str = "", params: dict = {}
    ) -> Union[T, List[T]]:
        results = self.execute(query, params=params)
        return self.to_class(Entity, results, path=path)

    def to_class(self, Entity, results: Union[dict, list, None], path: str = ""):

        for key in path.split("."):
            results = results.get(key)  # type: ignore

        if results is None:
            raise ValueError("Result value is null.")

        if type(results) == list:
            return list(map(lambda e: Entity(e, self), results))

        return Entity(results, self)
