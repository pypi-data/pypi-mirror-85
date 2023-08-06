from benchling_api_client.client import Client

from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.base_service import BaseService
from benchling_sdk.services.schema.dropdown_service import DropdownService


class SchemaService(BaseService):
    _dropdown_service: DropdownService

    def __init__(
        self, client: Client, retry_strategy: RetryStrategy,
    ):
        super().__init__(client, retry_strategy)
        self._dropdown_service = DropdownService(client, retry_strategy)

    @property
    def dropdowns(self) -> DropdownService:
        return self._dropdown_service
