from yoti_python_sdk.utils import YotiSerializable
from yoti_python_sandbox.doc_scan.task.sandbox_text_extraction_reason import (  # noqa: F401
    SandboxTextDataExtractionReason,
)

VALUE_PROGRESS = "PROGRESS"
VALUE_SHOULD_TRY_AGAIN = "SHOULD_TRY_AGAIN"
VALUE_MUST_TRY_AGAIN = "MUST_TRY_AGAIN"


class SandboxTextDataExtractionRecommendation(YotiSerializable):
    def __init__(self, value, reason):
        self.__value = value
        self.__reason = reason

    def to_json(self):
        obj = {
            "value": self.__value,
        }
        if self.__reason is not None:
            obj["reason"] = self.__reason
        return obj


class SandboxTextDataExtractionRecommendationBuilder(object):
    def __init__(self):
        self.__value = None
        self.__reason = None

    def for_progress(self):
        """
        :rtype: SandboxTextDataExtractionRecommendationBuilder
        """
        self.__value = VALUE_PROGRESS
        return self

    def for_should_try_again(self):
        """
        :rtype: SandboxTextDataExtractionRecommendationBuilder
        """
        self.__value = VALUE_SHOULD_TRY_AGAIN
        return self

    def for_must_try_again(self):
        """
        :rtype: SandboxTextDataExtractionRecommendationBuilder
        """
        self.__value = VALUE_MUST_TRY_AGAIN
        return self

    def with_reason(self, reason):
        """
        :param SandboxTextDataExtractionReason reason: the reason
        :rtype: SandboxTextDataExtractionRecommendationBuilder
        """
        self.__reason = reason
        return self

    def build(self):
        return SandboxTextDataExtractionRecommendation(self.__value, self.__reason)
