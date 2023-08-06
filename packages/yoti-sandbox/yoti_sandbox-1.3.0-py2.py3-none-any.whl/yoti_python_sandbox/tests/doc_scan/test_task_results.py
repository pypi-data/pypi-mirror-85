from mock import Mock

from yoti_python_sandbox.doc_scan import SandboxTaskResultsBuilder
from yoti_python_sandbox.doc_scan.task_results import SandboxTaskResults
from yoti_python_sandbox.doc_scan.task.sandbox_text_extraction_task import (
    SandboxDocumentTextDataExtractionTask,
)
from yoti_python_sandbox.doc_scan.task.sandbox_supplementary_document_text_extraction_task import (
    SandboxSupplementaryDocumentTextDataExtractionTask,
)


def test_json_should_have_correct_properties():
    text_extraction_task_mock = Mock(spec=SandboxDocumentTextDataExtractionTask)
    supplementary_text_extraction_task_mock = Mock(
        spec=SandboxSupplementaryDocumentTextDataExtractionTask
    )

    task_results = (
        SandboxTaskResultsBuilder()
        .with_text_extraction_task(text_extraction_task_mock)
        .with_supplementary_document_text_extraction_task(
            supplementary_text_extraction_task_mock
        )
        .build()
    )

    json = task_results.to_json()

    assert json.get("ID_DOCUMENT_TEXT_DATA_EXTRACTION")[0] == text_extraction_task_mock
    assert (
        json.get("SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION")[0]
        == supplementary_text_extraction_task_mock
    )


def test_json_defaults_to_empty_array_for_tasks():

    task_results = SandboxTaskResults()

    json = task_results.to_json()

    assert json.get("ID_DOCUMENT_TEXT_DATA_EXTRACTION") == []
    assert json.get("SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION") == []
