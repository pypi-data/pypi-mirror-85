from mock import Mock

from yoti_python_sandbox.doc_scan.task import (
    SandboxTextDataExtractionRecommendationBuilder,
)
from yoti_python_sandbox.doc_scan.task.sandbox_text_extraction_reason import (
    SandboxTextDataExtractionReason,
)


def test_json_should_include_value_progress():
    recommendation = (
        SandboxTextDataExtractionRecommendationBuilder().for_progress().build()
    )

    assert recommendation.to_json().get("value") == "PROGRESS"


def test_json_should_include_value_should_try_again():
    recommendation = (
        SandboxTextDataExtractionRecommendationBuilder().for_should_try_again().build()
    )

    assert recommendation.to_json().get("value") == "SHOULD_TRY_AGAIN"


def test_json_should_include_value_must_try_again():
    recommendation = (
        SandboxTextDataExtractionRecommendationBuilder().for_must_try_again().build()
    )

    assert recommendation.to_json().get("value") == "MUST_TRY_AGAIN"


def test_json_should_not_include_reason_when_not_set():
    recommendation = SandboxTextDataExtractionRecommendationBuilder().build()

    assert recommendation.to_json().get("reason") is None


def test_json_should_include_reason_when_set():
    reason_mock = Mock(spec=SandboxTextDataExtractionReason)

    recommendation = (
        SandboxTextDataExtractionRecommendationBuilder()
        .with_reason(reason_mock)
        .build()
    )

    assert recommendation.to_json().get("reason") == reason_mock
