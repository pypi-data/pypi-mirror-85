from yoti_python_sandbox.doc_scan.task import (
    SandboxTextDataExtractionReasonBuilder,
)


def test_json_should_include_value_user_error():
    reason = SandboxTextDataExtractionReasonBuilder().for_user_error().build()

    assert reason.to_json().get("value") == "USER_ERROR"


def test_json_should_include_value_quality():
    reason = SandboxTextDataExtractionReasonBuilder().for_quality().build()

    assert reason.to_json().get("value") == "QUALITY"


def test_json_should_include_detail_when_set():
    some_detail = "some-detail"

    reason = SandboxTextDataExtractionReasonBuilder().with_detail(some_detail).build()

    assert reason.to_json().get("detail") == some_detail


def test_json_should_not_include_detail_when_not_set():
    reason = SandboxTextDataExtractionReasonBuilder().build()

    assert reason.to_json().get("detail") is None
