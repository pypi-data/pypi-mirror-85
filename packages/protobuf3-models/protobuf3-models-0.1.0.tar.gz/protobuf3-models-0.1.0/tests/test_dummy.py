# -*- coding:utf-8 -*-
import tests.protobuf3_models_tests_pb2 as pb2  # pylint: disable=unused-import
from protobuf3_models.add import add
from protobuf3_models.fields import Int
from protobuf3_models.models import Model


def test_dummy() -> None:
    assert 2 + 2 == 4


def test_add() -> None:
    assert add(2, 2) == 4


def test_model() -> None:
    class ModelOptional(Model, protobuf_message=pb2.Int64):
        value = Int()

    model = ModelOptional()
    model._message = pb2.Int64()  # pylint: disable=protected-access
    model.value = 9
