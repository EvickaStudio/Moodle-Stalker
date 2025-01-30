from typing import Dict, Type, TypeVar

T = TypeVar("T")


class ServiceLocator:
    """Central registry for all service singletons."""

    _instance = None
    _services: Dict[str, object] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceLocator, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, service_name: str, service: object) -> None:
        """Register a service instance."""
        cls._services[service_name] = service

    @classmethod
    def get(cls, service_name: str, service_type: Type[T]) -> T:
        """Get a registered service by name."""
        service = cls._services.get(service_name)
        if service is None:
            raise KeyError(f"Service not registered: {service_name}")
        if not isinstance(service, service_type):
            raise TypeError(f"Service {service_name} is not of type {service_type}")
        return service
