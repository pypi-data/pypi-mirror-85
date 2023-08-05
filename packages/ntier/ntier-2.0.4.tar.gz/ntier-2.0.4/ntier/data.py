"""Contains the transaction Data class."""
from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping

from .paging import Paging

TransactionInput = Mapping[str, Any]
TransactionState = MutableMapping[str, Any]


@dataclass(frozen=True)
class TransactionData:
    """Contains input and state data for an API Transaction."""

    input: TransactionInput
    state: TransactionState
    paging: Paging
