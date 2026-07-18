from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseConnector(ABC):
    """
    Base class for all external data connectors.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Fetch data from the external service.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check whether the external service is reachable.
        """
        pass

    def success(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "connector": self.name,
            "status": "success",
            "data": data,
        }

    def error(self, message: str) -> Dict[str, Any]:
        return {
            "connector": self.name,
            "status": "error",
            "message": message,
        }
