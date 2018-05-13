from src.Error.ErrorManager import ErrorManager, ErrorCode


def test_add_error():
    error_mgr = ErrorManager()
    error_mgr.clear_error()
    assert len(error_mgr.error_log) == 0

    error_mgr.add_error()
    assert len(error_mgr.error_log) == 1

    error_mgr.add_error(ErrorCode.INVALID_SYNTAX, "test", ["toto"])
    assert len(error_mgr.error_log) == 2

    assert error_mgr.error_log[0].error_type == ErrorCode.INTERNAL_ERROR
    assert error_mgr.error_log[0].error_args == []
    assert error_mgr.error_log[1].error_type == ErrorCode.INVALID_SYNTAX
    assert error_mgr.error_log[1].error_args == ["toto"]
