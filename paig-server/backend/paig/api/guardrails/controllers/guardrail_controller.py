from typing import List

from api.guardrails.api_schemas.guardrail import GuardrailFilter, GuardrailView, GRVersionHistoryFilter
from api.guardrails.services.guardrails_service import GuardrailService
from core.controllers.paginated_response import Pageable
from core.db_session import Transactional, Propagation
from core.utils import SingletonDepends


class GuardrailController:
    """
    Controller class specifically for handling Guardrail entities.

    Args:
        guardrail_service (GuardrailService): The service class for handling Guardrail entities.
    """

    def __init__(self, guardrail_service: GuardrailService = SingletonDepends(GuardrailService)):
        self.guardrail_service = guardrail_service

    async def list(self, filter: GuardrailFilter, page_number: int, size: int, sort: List[str]) -> Pageable:
        """
        List Guardrails based on the provided filter, pagination, and sorting parameters.

        Args:
            filter (GuardrailFilter): The filter object containing the search parameters.
            page_number (int): The page number to retrieve.
            size (int): The number of records to retrieve per page.
            sort (List[str]): The sorting parameters to apply.

        Returns:
            Pageable: The paginated response containing the list of Guardrails.
        """
        return await self.guardrail_service.list(
            filter=filter,
            page_number=page_number,
            size=size,
            sort=sort
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, request: GuardrailView) -> GuardrailView:
        """
        Create a new Guardrail.

        Args:
            request (GuardrailView): The view object representing the Guardrail to create.

        Returns:
            GuardrailView: The created Guardrail view object.
        """
        return await self.guardrail_service.create(request)

    async def get_by_id(self, id: int, extended: bool) -> GuardrailView:
        """
        Retrieve a Guardrail by its ID.

        Args:
            id (int): The ID of the Guardrail to retrieve.
            extended (bool): Include extended information

        Returns:
            GuardrailView: The Guardrail view object corresponding to the ID.
        """
        return await self.guardrail_service.get_by_id(id, extended)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update(self, id: int, request: GuardrailView) -> GuardrailView:
        """
        Update a Guardrail identified by its ID.

        Args:
            id (int): The ID of the Guardrail to update.
            request (GuardrailView): The updated view object representing the Guardrail.

        Returns:
            GuardrailView: The updated Guardrail view object.
        """
        return await self.guardrail_service.update(id, request)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(self, id: int):
        """
        Delete a Guardrail by its ID.

        Args:
            id (int): The ID of the Guardrail to delete.
        """
        await self.guardrail_service.delete(id)

    async def get_history(self, id: int = None, filter: GRVersionHistoryFilter = None, page_number: int = None,
                          size: int = None, sort: List[str] = None) -> Pageable:
        """
        Get the history of a guardrail by its ID.

        Args:
            id (int): The ID of the Guardrail to retrieve the history for.
            filter (GRVersionHistoryFilter): The filter object containing the search parameters.
            page_number (int): The page number to retrieve.
            size (int): The number of records to retrieve per page.
            sort (List[str]): The sorting parameters to apply.

        Returns:
            Pageable: The paginated response containing the history of the Guardrail.
        """
        return await self.guardrail_service.get_history(id, filter, page_number, size, sort)
