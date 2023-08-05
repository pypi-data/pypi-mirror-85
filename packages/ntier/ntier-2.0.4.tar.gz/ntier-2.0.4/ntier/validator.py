"""Validator and Validations."""
import inspect
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import (Any, Awaitable, Callable, List, Mapping, MutableMapping,
                    Optional, Sequence, Type, Union, cast)

from .validation_result import ValidationResult

Record = Mapping[str, Any]
MutableRecord = MutableMapping[str, Any]
ValidateFieldSync = Callable[[Any], bool]
ValidateFieldAsync = Callable[[Any], Awaitable[bool]]
ValidateField = Union[ValidateFieldSync, ValidateFieldAsync]
ValidateRecordSync = Callable[[Record], bool]
ValidateRecordAsync = Callable[[Record], Awaitable[bool]]
ValidateRecord = Union[ValidateRecordSync, ValidateRecordAsync]

NUMBER_TYPES = (int, float, Decimal)
Number = Union[int, float, Decimal]


@dataclass
class FieldValidator:
    """Information to validate a single field."""

    field_name: str
    message: str
    validator: ValidateField

    async def validate(self, value: Any) -> bool:
        """Properly calls the validator."""
        if inspect.iscoroutinefunction(self.validator):
            return await cast(ValidateFieldAsync, self.validator)(value)
        return cast(ValidateFieldSync, self.validator)(value)


@dataclass
class RecordValidator:
    """Information to validate a whole record."""

    message: str
    validator: ValidateRecord
    field_name: Optional[str]

    async def validate(self, record: Record) -> bool:
        """Properly calls the validator."""
        if inspect.iscoroutinefunction(self.validator):
            return await cast(ValidateRecordAsync, self.validator)(record)
        return cast(ValidateRecordSync, self.validator)(record)


ValidatorType = Union[FieldValidator, RecordValidator]


class Validator:
    """Records validators for a record."""

    def __init__(self, validators: Optional[List[ValidatorType]] = None):
        self.validators: List[ValidatorType] = validators or []

    @staticmethod
    def field(field_name, message: str, validate: ValidateField) -> FieldValidator:
        return FieldValidator(field_name, message, validate)

    @staticmethod
    def record(
        message: str, validate: ValidateRecord, field_name: str = None
    ) -> RecordValidator:
        return RecordValidator(message, validate, field_name)

    async def validate(self, record: Record) -> ValidationResult:
        return await ValidatorInstance(self, record).validate()


class ValidatorInstance:
    """Holds results for a run of validation."""

    def __init__(self, validator: Validator, record: Record) -> None:
        self.validator = validator
        self.record = record
        self.validation_result = ValidationResult()

    async def validate(self) -> ValidationResult:
        """Executes all validators against the record until one fails."""
        for validator in self.validator.validators:
            if isinstance(validator, FieldValidator):
                await self.validate_field(validator)
            elif isinstance(validator, RecordValidator):
                await self.validate_record(validator)
            else:
                raise Exception("Invalid validator")

            if not self.validation_result:
                return self.validation_result

        return self.validation_result

    async def validate_field(self, validator: FieldValidator) -> None:
        """Validate a single field."""
        field_name = validator.field_name
        value = self.record.get(field_name, None)
        result = await validator.validate(value)

        if not result:
            self.validation_result.add_message(field_name, validator.message)

    async def validate_record(self, validator: RecordValidator) -> None:
        """Validate an entire record."""
        result = await validator.validate(self.record)

        if not result:
            if validator.field_name:
                self.validation_result.add_message(
                    validator.field_name, validator.message
                )
            else:
                self.validation_result.add_general_message(validator.message)


class Validators:
    """Contains validator methods."""

    @staticmethod
    def is_present(val: Any) -> bool:
        """Validate that a value is not None"""
        if val is None:
            return False
        return True

    @staticmethod
    def optional(validator: ValidateFieldSync) -> ValidateFieldSync:
        """Makes a validator ignore None values"""

        def checker(val: Any) -> bool:
            if val is None:
                return True
            return validator(val)

        return checker

    @staticmethod
    def any(validators: List[ValidateFieldSync]) -> ValidateFieldSync:
        """Validates a value matches at least one validator."""

        def checker(val: Any) -> bool:
            for validator in validators:
                if validator(val):
                    return True
            return False

        return checker

    @staticmethod
    def is_type(typ: Type) -> ValidateFieldSync:
        """Validates that a value is of a type."""

        def checker(val: Any) -> bool:
            return isinstance(val, typ)

        return checker

    @staticmethod
    def is_member(members: Sequence) -> ValidateFieldSync:
        """Validates that a value is a member of a sequence."""

        def checker(val: Any) -> bool:
            return val in members

        return checker

    @staticmethod
    def is_not_empty(val: Any) -> ValidateFieldSync:
        """Validates that a string is not empty."""

        if not isinstance(val, str):
            return False
        return bool(val)

    @staticmethod
    def is_match(pattern: str) -> ValidateFieldSync:
        """Validates that a value matches a regular expression"""

        def checker(val: Any) -> bool:
            if not isinstance(val, str):
                return False
            return bool(re.match(pattern, val))

        return checker

    @staticmethod
    def is_length(min_len: Optional[int], max_len: Optional[int]) -> ValidateFieldSync:
        """Validates that a string value is within certain length bounds"""

        def checker(val: Any) -> bool:
            if not isinstance(val, str):
                return False
            if min_len is not None and len(val) < min_len:
                return False
            if max_len is not None and max_len < len(val):
                return False
            return True

        return checker

    @staticmethod
    def is_greater(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val > bound

        return checker

    @staticmethod
    def is_lesser(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val < bound

        return checker

    @staticmethod
    def is_greater_or_equal(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val >= bound

        return checker

    @staticmethod
    def is_lesser_or_equal(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val <= bound

        return checker

    @staticmethod
    def is_between(lbound: Number, ubound: Number) -> ValidateFieldSync:
        """Validates that a number is between two other numbers, inclusive."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return lbound <= val <= ubound

        return checker
