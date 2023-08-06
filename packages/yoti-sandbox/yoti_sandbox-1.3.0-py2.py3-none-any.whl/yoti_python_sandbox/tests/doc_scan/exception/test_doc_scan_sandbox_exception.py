import json

from yoti_python_sandbox.doc_scan.exception import DocScanSandboxException
from yoti_python_sdk.tests.mocks import MockResponse


def test_return_message():
    response = MockResponse(status_code=400, text="some response")
    exception = DocScanSandboxException("some error", response)

    assert exception.message == "some error"


def test_return_status_code():
    response = MockResponse(status_code=400, text="")
    exception = DocScanSandboxException("some error", response)

    assert exception.status_code == 400


def test_return_content():
    response = MockResponse(status_code=400, text="", content="some content")
    exception = DocScanSandboxException("some error", response)

    assert exception.content == "some content"


def test_return_text():
    response = MockResponse(status_code=400, text="some response")
    exception = DocScanSandboxException("some error", response)

    assert exception.text == "some response"


def test_return_only_message_when_html_response():
    response = MockResponse(
        status_code=400,
        text="<html>some html</html>",
        headers={"Content-Type": "text/html"},
    )
    exception = DocScanSandboxException("some error", response)

    assert exception.message == "some error"


def test_return_only_message_when_json_response_has_no_message_property():
    response = MockResponse(
        status_code=400,
        text=json.dumps({}),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanSandboxException("some error", response)

    assert exception.message == "some error"


def test_return_formatted_response_code_and_message():
    response = MockResponse(
        status_code=400,
        text=json.dumps({"code": "SOME_CODE", "message": "some message"}),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanSandboxException("some error", response)

    assert exception.message == "some error - SOME_CODE - some message"


def test_return_formatted_response_code_message_and_errors():
    response = MockResponse(
        status_code=400,
        text=json.dumps(
            {
                "code": "SOME_CODE",
                "message": "some message",
                "errors": [
                    {"property": "some.property", "message": "some message"},
                    {
                        "property": "some.other.property",
                        "message": "some other message",
                    },
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanSandboxException("some error", response)

    assert (
        exception.message
        == 'some error - SOME_CODE - some message: some.property "some message", some.other.property "some other message"'
    )


def test_excludes_errors_without_property_or_message():
    response = MockResponse(
        status_code=400,
        text=json.dumps(
            {
                "code": "SOME_CODE",
                "message": "some message",
                "errors": [
                    {"message": "some message"},
                    {"property": "some.other.property"},
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanSandboxException("some error", response)

    assert exception.message == "some error - SOME_CODE - some message"
