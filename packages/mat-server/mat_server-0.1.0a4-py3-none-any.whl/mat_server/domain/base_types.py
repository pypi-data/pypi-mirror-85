# mypy: ignore_errors
import abc


class Entity(abc.ABC):
    def serialize(self) -> dict:
        pass


class UseCase(abc.ABC):
    """領域的用例"""
    pass


class Service(abc.ABC):
    """領域的服務"""
    pass


class Repository(abc.ABC):
    """領域的儲存庫"""
    pass


class Helper(abc.ABC):
    """工具包"""
    pass
