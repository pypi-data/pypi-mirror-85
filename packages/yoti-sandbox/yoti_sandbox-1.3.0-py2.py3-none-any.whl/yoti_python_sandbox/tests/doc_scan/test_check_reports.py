from mock import Mock

from yoti_python_sandbox.doc_scan import SandboxCheckReportsBuilder
from yoti_python_sandbox.doc_scan.check_reports import SandboxCheckReports
from yoti_python_sandbox.doc_scan.check.sandbox_document_authenticity_check import (
    SandboxDocumentAuthenticityCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_face_match_check import (
    SandboxDocumentFaceMatchCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_text_data_check import (
    SandboxDocumentTextDataCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_liveness_check import (
    SandboxLivenessCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_id_document_comparison_check import (
    SandboxIdDocumentComparisonCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_supplementary_document_text_data_check import (
    SandboxSupplementaryDocumentTextDataCheck,
)


def test_should_build_with_correct_properties():
    authenticity_check_mock = Mock(spec=SandboxDocumentAuthenticityCheck)
    face_match_check_mock = Mock(spec=SandboxDocumentFaceMatchCheck)
    text_data_check_mock = Mock(spec=SandboxDocumentTextDataCheck)
    liveness_check_mock = Mock(spec=SandboxLivenessCheck)
    comparison_check_mock = Mock(spec=SandboxIdDocumentComparisonCheck)
    supplementary_text_data_check_mock = Mock(
        spec=SandboxSupplementaryDocumentTextDataCheck
    )
    async_report_delay = 12

    check_reports = (
        SandboxCheckReportsBuilder()
        .with_document_authenticity_check(authenticity_check_mock)
        .with_document_face_match_check(face_match_check_mock)
        .with_document_text_data_check(text_data_check_mock)
        .with_liveness_check(liveness_check_mock)
        .with_id_document_comparison_check(comparison_check_mock)
        .with_supplementary_document_text_data_check(supplementary_text_data_check_mock)
        .with_async_report_delay(async_report_delay)
        .build()
    )

    assert len(check_reports.document_authenticity_checks) == 1
    assert check_reports.document_authenticity_checks[0] == authenticity_check_mock

    assert len(check_reports.document_face_match_checks) == 1
    assert check_reports.document_face_match_checks[0] == face_match_check_mock

    assert len(check_reports.document_text_data_checks) == 1
    assert check_reports.document_text_data_checks[0] == text_data_check_mock

    assert len(check_reports.liveness_checks) == 1
    assert check_reports.liveness_checks[0] == liveness_check_mock

    assert len(check_reports.id_document_comparison_checks) == 1
    assert check_reports.id_document_comparison_checks[0] == comparison_check_mock

    assert len(check_reports.supplementary_document_text_data_checks) == 1
    assert (
        check_reports.supplementary_document_text_data_checks[0]
        == supplementary_text_data_check_mock
    )

    assert check_reports.async_report_delay == 12


def test_json_should_have_correct_properties():
    authenticity_check_mock = Mock(spec=SandboxDocumentAuthenticityCheck)
    face_match_check_mock = Mock(spec=SandboxDocumentFaceMatchCheck)
    text_data_check_mock = Mock(spec=SandboxDocumentTextDataCheck)
    liveness_check_mock = Mock(spec=SandboxLivenessCheck)
    comparison_check_mock = Mock(spec=SandboxIdDocumentComparisonCheck)
    supplementary_text_data_check_mock = Mock(
        spec=SandboxSupplementaryDocumentTextDataCheck
    )
    async_report_delay = 12

    check_reports = (
        SandboxCheckReportsBuilder()
        .with_document_authenticity_check(authenticity_check_mock)
        .with_document_face_match_check(face_match_check_mock)
        .with_document_text_data_check(text_data_check_mock)
        .with_liveness_check(liveness_check_mock)
        .with_id_document_comparison_check(comparison_check_mock)
        .with_supplementary_document_text_data_check(supplementary_text_data_check_mock)
        .with_async_report_delay(async_report_delay)
        .build()
    )

    json = check_reports.to_json()

    assert json.get("ID_DOCUMENT_AUTHENTICITY")[0] == authenticity_check_mock
    assert json.get("ID_DOCUMENT_FACE_MATCH")[0] == face_match_check_mock
    assert json.get("ID_DOCUMENT_TEXT_DATA_CHECK")[0] == text_data_check_mock
    assert json.get("ID_DOCUMENT_COMPARISON")[0] == comparison_check_mock
    assert (
        json.get("SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK")[0]
        == supplementary_text_data_check_mock
    )
    assert json.get("LIVENESS")[0] == liveness_check_mock
    assert json.get("async_report_delay") == async_report_delay


def test_json_defaults_to_empty_array_for_checks():

    check_reports = SandboxCheckReports()

    json = check_reports.to_json()

    assert json.get("ID_DOCUMENT_AUTHENTICITY") == []
    assert json.get("ID_DOCUMENT_FACE_MATCH") == []
    assert json.get("ID_DOCUMENT_TEXT_DATA_CHECK") == []
    assert json.get("ID_DOCUMENT_COMPARISON") == []
    assert json.get("SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK") == []
    assert json.get("LIVENESS") == []


def test_async_report_delay_not_included_when_not_specified():
    authenticity_check_mock = Mock(spec=SandboxDocumentAuthenticityCheck)

    check_reports = (
        SandboxCheckReportsBuilder()
        .with_document_authenticity_check(authenticity_check_mock)
        .build()
    )

    assert check_reports.async_report_delay is None
