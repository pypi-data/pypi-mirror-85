from benchling_api_client.client import Client

from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.base_service import BaseService
from benchling_sdk.services.inventory.container_service import ContainerService
from benchling_sdk.services.inventory.plate_service import PlateService


class InventoryService(BaseService):
    _container_service: ContainerService
    _plate_service: PlateService

    def __init__(
        self, client: Client, retry_strategy: RetryStrategy,
    ):
        super().__init__(client, retry_strategy)
        self._container_service = ContainerService(client, retry_strategy)
        self._plate_service = PlateService(client, retry_strategy)

    @property
    def containers(self) -> ContainerService:
        return self._container_service

    @property
    def plates(self) -> PlateService:
        return self._plate_service
