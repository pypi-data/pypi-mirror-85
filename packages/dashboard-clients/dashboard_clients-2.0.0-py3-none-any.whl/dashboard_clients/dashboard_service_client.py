from typing import Any
from clients_core.service_clients import E360ServiceClient
from marshmallow import EXCLUDE
from .models import TabbedDashboardModel


class DashboardsClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = ""
    extra_headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json"
    }

    def create(self, payload: TabbedDashboardModel, **kwargs: Any) -> TabbedDashboardModel:
        """
        Creates a dashboard, returns a deserialised model instance.

        Args:
            payload: a serialised object for a dashboard

        """
        payload_json = TabbedDashboardModel.Schema().dump(payload)
        response = self.client.post('', json=payload_json, headers=self.service_headers, raises=True, **kwargs)
        response_json = response.json()
        return TabbedDashboardModel.Schema(unknown=EXCLUDE).load(response_json)  # type: ignore
