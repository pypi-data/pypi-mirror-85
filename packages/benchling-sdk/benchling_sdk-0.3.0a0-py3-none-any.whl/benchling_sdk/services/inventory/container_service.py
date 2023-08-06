from benchling_api_client.api.containers import get_container
from benchling_api_client.models.container import Container

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class ContainerService(BaseService):
    @api_method
    def get_by_id(self, container_id: str) -> Container:
        response = get_container.sync_detailed(client=self.client, container_id=container_id)
        return model_from_detailed(response)
