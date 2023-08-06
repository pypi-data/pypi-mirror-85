from yoti_python_sdk.utils import YotiSerializable
from yoti_python_sandbox.doc_scan.document_filter import (  # noqa: F401
    SandboxDocumentFilter,
)
from yoti_python_sandbox.doc_scan.task.sandbox_text_extraction_recommendation import (  # noqa: F401
    SandboxTextDataExtractionRecommendation,
)


class SandboxSupplementaryDocumentTextDataExtractionTaskResult(YotiSerializable):
    def __init__(
        self,
        document_fields=None,
        detected_country=None,
        recommendation=None,
    ):
        self.__document_fields = document_fields
        self.__detected_country = detected_country
        self.__recommendation = recommendation

    @property
    def document_fields(self):
        return self.__document_fields

    @property
    def detected_country(self):
        return self.__detected_country

    @property
    def recommendation(self):
        return self.__recommendation

    def to_json(self):
        json = {}

        if self.document_fields is not None:
            json["document_fields"] = self.document_fields

        if self.detected_country is not None:
            json["detected_country"] = self.detected_country

        if self.recommendation is not None:
            json["recommendation"] = self.recommendation

        return json


class SandboxSupplementaryDocumentTextDataExtractionTask(YotiSerializable):
    def __init__(self, result, document_filter):
        self.__result = result
        self.__document_filter = document_filter

    @property
    def result(self):
        """
        :rtype: SandboxSupplementaryDocumentTextDataExtractionTaskResult
        """
        return self.__result

    @property
    def document_filter(self):
        """
        :rtype: SandboxDocumentFilter
        """
        return self.__document_filter

    def to_json(self):
        obj = {
            "result": self.__result,
        }
        if self.__document_filter is not None:
            obj["document_filter"] = self.__document_filter
        return obj


class SandboxSupplementaryDocumentTextDataExtractionTaskBuilder(object):
    def __init__(self):
        self.__document_fields = None
        self.__document_filter = None
        self.__detected_country = None
        self.__recommendation = None

    def with_document_field(self, key, value):
        """
        :type key: str
        :type value: str or dict
        :rtype: SandboxSupplementaryDocumentTextDataExtractionTaskBuilder
        """
        self.__document_fields = self.__document_fields or {}
        self.__document_fields[key] = value
        return self

    def with_document_fields(self, document_fields):
        """
        :type document_fields: dict
        :rtype: SandboxSupplementaryDocumentTextDataExtractionTaskBuilder
        """
        self.__document_fields = document_fields
        return self

    def with_document_filter(self, document_filter):
        """
        :type document_filter: SandboxDocumentFilter
        :rtype: SandboxSupplementaryDocumentTextDataExtractionTaskBuilder
        """
        self.__document_filter = document_filter
        return self

    def with_detected_country(self, detected_country):
        """
        :param str detected_country: the detected country
        """
        self.__detected_country = detected_country
        return self

    def with_recommendation(self, recommendation):
        """
        :type recommendation: SandboxTextDataExtractionRecommendation
        :rtype: SandboxSupplementaryDocumentTextDataExtractionTaskBuilder
        """
        self.__recommendation = recommendation
        return self

    def build(self):
        result = SandboxSupplementaryDocumentTextDataExtractionTaskResult(
            self.__document_fields,
            self.__detected_country,
            self.__recommendation,
        )
        return SandboxSupplementaryDocumentTextDataExtractionTask(
            result, self.__document_filter
        )
