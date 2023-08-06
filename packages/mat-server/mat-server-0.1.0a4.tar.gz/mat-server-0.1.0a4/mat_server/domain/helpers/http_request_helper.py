import abc

from mat_server.domain import base_types, entities


class HTTPRequestHelperBase(base_types.Helper):

    @abc.abstractmethod
    def send(self, request: entities.HTTPRequest) -> entities.HTTPResponse:
        pass
