# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, List, Optional, Type, TypeVar, Union

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from protobuf3_models.models import Model

Input = TypeVar("Input")
Output = TypeVar("Output")
ValidatorType = Callable[[Input], None]


class Field(Generic[Input, Output]):

    __slots__ = ("_name", "_protobuf_name", "_required", "_validators")

    _name: Optional[str]
    _protobuf_name: Optional[str]
    _validators: List[ValidatorType]

    def __init__(
        self,
        *,
        protobuf_name: Optional[str] = None,
        required: bool = True,
        validators: Optional[List[ValidatorType]] = None,
    ):
        self._name = None
        self._protobuf_name = protobuf_name
        self._required = required
        self._validators = validators or []

    def __set_name__(self, owner: Type[Model], name: str) -> None:
        self._name = name

        if self._protobuf_name is None:
            self._protobuf_name = name

    def __get__(self, instance: Optional[Model], owner: Type[Model]) -> Union[Field[Input, Output], Output]:
        if instance is None:
            return self

        if instance.message is None:
            raise Exception("No message attached to model.")

        return self.get(instance)

    def __set__(self, instance: Model, value: Input) -> None:
        if instance.message is None:
            raise Exception("No message attached to model.")

        self.set(instance, value)

    def __delete__(self, instance: Model) -> None:
        if instance.message is None:
            raise Exception("No message attached to model.")

        self.clear(instance)

    @property
    def name(self) -> str:
        if self._name is None:
            raise Exception("Field is not attached to model class.")

        return self._name

    @property
    def protobuf_name(self) -> str:
        if self._protobuf_name is None:
            raise Exception("Field is not attached to model class.")

        return self._protobuf_name

    def get(self, model: Model) -> Output:
        raise NotImplementedError()

    def set(self, model: Model, value: Input) -> None:
        raise NotImplementedError()

    def clear(self, model: Model) -> None:
        raise NotImplementedError()


class Int(Field[int, int]):
    def get(self, model: Model) -> int:
        return int(getattr(model.message, self.protobuf_name))

    def set(self, model: Model, value: int) -> None:
        setattr(model.message, self.protobuf_name, value)

    def clear(self, model: Model) -> None:
        model.message.ClearField(self.protobuf_name)
