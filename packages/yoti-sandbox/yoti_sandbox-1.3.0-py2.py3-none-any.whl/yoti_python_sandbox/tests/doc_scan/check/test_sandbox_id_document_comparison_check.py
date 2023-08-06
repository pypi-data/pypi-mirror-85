from mock import Mock

from yoti_python_sandbox.doc_scan.check import SandboxIdDocumentComparisonCheckBuilder
from yoti_python_sandbox.doc_scan.check.sandbox_id_document_comparison_check import (
    SandboxIdDocumentComparisonCheck,
)
from yoti_python_sandbox.doc_scan.check.report.breakdown import SandboxBreakdown
from yoti_python_sandbox.doc_scan.check.report.recommendation import (
    SandboxRecommendation,
)
from yoti_python_sandbox.doc_scan.document_filter import SandboxDocumentFilter


def test_should_build_sandbox_id_document_comparison_check():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)

    check = (
        SandboxIdDocumentComparisonCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .build()
    )

    assert check.result.report.recommendation is not None
    assert check.result.report.recommendation == recommendation_mock
    assert len(check.result.report.breakdown) == 1
    assert check.result.report.breakdown[0] == breakdown_mock


def test_builder_method_should_return_builder():
    check = SandboxIdDocumentComparisonCheck.builder().build()

    assert check.result.report is not None


def test_should_accept_document_filter():
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    check = (
        SandboxIdDocumentComparisonCheckBuilder()
        .with_secondary_document_filter(document_filter_mock)
        .build()
    )

    assert check.secondary_document_filter == document_filter_mock


def test_json_should_include_document_filter():
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    check = (
        SandboxIdDocumentComparisonCheckBuilder()
        .with_secondary_document_filter(document_filter_mock)
        .build()
    )

    json = check.to_json()

    assert json.get("secondary_document_filter") == document_filter_mock


def test_json_includes_breakdowns():
    breakdowns_mock = [Mock(spec=SandboxBreakdown), Mock(spec=SandboxBreakdown)]

    check = (
        SandboxIdDocumentComparisonCheckBuilder()
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
        SandboxIdDocumentComparisonCheckBuilder()
        .with_recommendation(recommendation_mock)
        .build()
    )

    json = check.to_json()

    assert (
        json.get("result").to_json().get("report").to_json().get("recommendation")
        == recommendation_mock
    )
