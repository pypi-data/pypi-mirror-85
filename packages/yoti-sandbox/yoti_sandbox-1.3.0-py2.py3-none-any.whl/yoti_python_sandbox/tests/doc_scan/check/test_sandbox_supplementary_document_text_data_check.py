from mock import Mock

from yoti_python_sandbox.doc_scan.check import (
    SandboxSupplementaryDocumentTextDataCheckBuilder,
)
from yoti_python_sandbox.doc_scan.check.sandbox_supplementary_document_text_data_check import (
    SandboxSupplementaryDocumentTextDataCheck,
)
from yoti_python_sandbox.doc_scan.check.report.breakdown import SandboxBreakdown
from yoti_python_sandbox.doc_scan.check.report.recommendation import (
    SandboxRecommendation,
)
from yoti_python_sandbox.doc_scan.document_filter import SandboxDocumentFilter


def test_should_build_sandbox_document_authenticity_check():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .build()
    )

    assert check.result.report.recommendation is not None
    assert check.result.report.recommendation == recommendation_mock
    assert len(check.result.report.breakdown) == 1
    assert check.result.report.breakdown[0] == breakdown_mock


def test_should_accept_document_filter():
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_document_filter(document_filter_mock)
        .build()
    )

    assert check.document_filter == document_filter_mock


def test_json_should_include_document_filter():
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_document_filter(document_filter_mock)
        .build()
    )

    json = check.to_json()

    assert json.get("document_filter") == document_filter_mock


def test_should_accept_with_breakdowns():
    breakdowns_mock = [Mock(spec=SandboxBreakdown), Mock(spec=SandboxBreakdown)]

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_breakdowns(breakdowns_mock)
        .build()
    )

    assert check.result.report.breakdown == breakdowns_mock


def test_json_includes_breakdowns():
    breakdowns_mock = [Mock(spec=SandboxBreakdown), Mock(spec=SandboxBreakdown)]

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_breakdowns(breakdowns_mock)
        .build()
    )

    json = check.to_json()

    assert (
        json.get("result").to_json().get("report").to_json().get("breakdown")
        == breakdowns_mock
    )


def test_json_includes_recommendation():
    recommendation_mock = Mock(spec=SandboxRecommendation)

    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_recommendation(recommendation_mock)
        .build()
    )

    json = check.to_json()

    assert (
        json.get("result").to_json().get("report").to_json().get("recommendation")
        == recommendation_mock
    )


def test_should_allow_document_fields_set_with_dictionary():
    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_document_fields({"someKey": "someValue"})
        .build()
    )

    assert check.result.document_fields.get("someKey") == "someValue"


def test_json_should_include_document_fields_when_set():
    check = (
        SandboxSupplementaryDocumentTextDataCheckBuilder()
        .with_document_field("someKey", "someValue")
        .build()
    )

    json = check.to_json()

    assert (
        json.get("result").to_json().get("document_fields").get("someKey")
        == "someValue"
    )


def test_json_should_exclude_document_fields_when_not_set():
    check = SandboxSupplementaryDocumentTextDataCheckBuilder().build()

    json = check.to_json()

    assert json.get("result").to_json().get("document_fields") is None


def test_builder_should_create_new_builder():
    builder = SandboxSupplementaryDocumentTextDataCheck.builder()

    assert isinstance(builder, SandboxSupplementaryDocumentTextDataCheckBuilder)
