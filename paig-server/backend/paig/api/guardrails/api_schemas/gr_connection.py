from typing import Optional

from pydantic import Field

from api.guardrails import GuardrailProvider
from core.api_schemas.base_view import BaseView
from core.factory.database_initiator import BaseAPIFilter


class GRConnectionView(BaseView):
    """
    A model representing the Guardrails connection.

    Inherits from:
        BaseView: The base model containing common fields.

    Attributes:
        name (str): The name of the Guardrail connection.
        description (str): The description of the Guardrail connection.
        guardrail_provider (str): The guardrails' provider.
        connection_details (dict): The connection details.
    """
    name: str = Field(default=None, description="The name of the Guardrail connection")
    description: Optional[str] = Field(default=None, description="The description of the Guardrail connection")
    guardrail_provider: Optional[GuardrailProvider] = Field(..., description="The guardrails provider", alias="guardrailsProvider")
    connection_details: dict = Field(..., description="The connection details", alias="connectionDetails")


class GRConnectionFilter(BaseAPIFilter):
    """
    Filter class for Guardrails connections.

    Attributes:
        name (str, optional): Filter by name.
        description (str, optional): Filter by description.
        guardrail_provider (str, optional): Filter by guardrails' provider.
    """

    name: Optional[str] = Field(default=None, description="Filter by name")
    description: Optional[str] = Field(default=None, description="Filter by description")
    guardrail_provider: Optional[GuardrailProvider] = Field(default=None, description="Filter by guardrails provider", alias="guardrailsProvider")
