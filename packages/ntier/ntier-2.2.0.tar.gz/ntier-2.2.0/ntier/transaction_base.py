"""Contains the StructuredTransaction class."""
# pylint: disable=unused-argument
from typing import Optional

from .data import TransactionData, TransactionInput, TransactionState
from .paging import Paging
from .policy_result import PolicyResult
from .transaction_result import TransactionResult
from .validation_result import ValidationResult


class TransactionBase:
    """Allows child classes to define parts of a standard transaction life-cycle:
    - initialize
    - authenticate
    - find
    - authorize
    - validate
    - perform
    """

    async def execute(
        self, input_data: TransactionInput, paging: Optional[Paging] = None
    ) -> TransactionResult:
        """Calls and response properly to overridden methods to run a standard API request."""
        state = await self.initialize(input_data)
        data: TransactionData = TransactionData(
            input_data, state, paging or Paging.default()
        )

        is_authenticated = await self.authenticate(data)
        if not is_authenticated:
            return TransactionResult.not_authenticated()

        missing_entity_name = await self.find(data)
        if missing_entity_name:
            return TransactionResult.not_found(missing_entity_name)

        policy_result = await self.authorize(data)
        if not policy_result.is_valid:
            return TransactionResult.not_authorized(policy_result)

        validation_result = await self.validate(data)
        if not validation_result.is_valid:
            return TransactionResult.not_valid(validation_result)

        result = await self.perform(data)
        return result

    async def __call__(
        self, input_data: TransactionInput, paging: Optional[Paging] = None
    ) -> TransactionResult:
        return await self.execute(input_data, paging)

    async def initialize(self, input_data: TransactionInput) -> TransactionState:
        return {}

    async def authenticate(self, data: TransactionData) -> bool:
        return True

    async def find(self, data: TransactionData) -> Optional[str]:
        return None

    async def authorize(self, data: TransactionData) -> PolicyResult:
        return PolicyResult.success()

    async def validate(self, data: TransactionData) -> ValidationResult:
        return ValidationResult.success()

    async def perform(self, data: TransactionData) -> TransactionResult:
        return TransactionResult.success()
