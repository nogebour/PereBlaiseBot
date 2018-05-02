from src.Error.Error import Error, ErrorCode

from unittest.mock import MagicMock
import datetime


def test_error_code_0():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.INTERNAL_ERROR, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.INTERNAL_ERROR
    assert default_error.error_code == 0
    assert default_error.error_message == "Internal error"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp


def test_error_code_1():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.NO_DOCUMENT_FOUND, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.NO_DOCUMENT_FOUND
    assert default_error.error_code == 1
    assert default_error.error_message == "No document found"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp


def test_error_code_2():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.NO_DOCUMENT_INSERTED, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.NO_DOCUMENT_INSERTED
    assert default_error.error_code == 2
    assert default_error.error_message == "No document inserted"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp


def test_error_code_3():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.INVALID_REST_QUALITY, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.INVALID_REST_QUALITY
    assert default_error.error_code == 3
    assert default_error.error_message == "Invalid rest quality"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp


def test_error_code_4():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.INVALID_WALK_SPEED, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.INVALID_WALK_SPEED
    assert default_error.error_code == 4
    assert default_error.error_message == "Invalid walk speed"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp


def test_error_code_5():
    default_timestamp = datetime.datetime(2018, 1, 2, 3, 4, 5, 6)
    default_context = "test"
    default_error = Error(ErrorCode.NOT_AN_INTEGER, default_context, default_timestamp)
    assert default_error.error_type == ErrorCode.NOT_AN_INTEGER
    assert default_error.error_code == 5
    assert default_error.error_message == "Not an integer"
    assert default_error.context == default_context
    assert default_error.timestamp == default_timestamp
