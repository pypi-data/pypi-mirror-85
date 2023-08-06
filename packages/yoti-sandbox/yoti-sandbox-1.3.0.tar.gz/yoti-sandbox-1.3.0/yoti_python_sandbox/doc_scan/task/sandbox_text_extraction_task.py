import base64

from yoti_python_sdk.utils import YotiSerializable
from yoti_python_sandbox.doc_scan.document_filter import (  # noqa: F401
    SandboxDocumentFilter,
)
from yoti_python_sandbox.doc_scan.task.sandbox_text_extraction_recommendation import (  # noqa: F401
    SandboxTextDataExtractionRecommendation,
)


class SandboxDocumentIdPhoto(YotiSerializable):
    def __init__(self, content_type, data):
        """
        :param str content_type: the content type
        :param bytes data: the image data
        """
        self.__content_type = content_type
        self.__data = data

    def to_json(self):
        return {
            "content_type": self.__content_type,
            "data": base64.b64encode(self.__data).decode("utf-8"),
        }


class SandboxDocumentTextDataExtractionTaskResult(YotiSerializable):
    def __init__(
        self,
        document_fields=None,
        document_id_photo=None,
        detected_country=None,
        recommendation=None,
    ):
        self.__document_fields = document_fields
        self.__document_id_photo = document_id_photo
        self.__detected_country = detected_country
        self.__recommendation = recommendation

    @property
    def document_fields(self):
        return self.__document_fields

    @property
    def document_id_photo(self):
        return self.__document_id_photo

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

        if self.document_id_photo is not None:
            json["document_id_photo"] = self.document_id_photo

        if self.detected_country is not None:
            json["detected_country"] = self.detected_country

        if self.recommendation is not None:
            json["recommendation"] = self.recommendation

        return json


class SandboxDocumentTextDataExtractionTask(YotiSerializable):
    def __init__(self, result, document_filter):
        self.__result = result
        self.__document_filter = document_filter

    @property
    def result(self):
        """
        :rtype: SandboxDocumentTextDataExtractionTaskResult
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


class SandboxDocumentTextDataExtractionTaskBuilder(object):
    def __init__(self):
        self.__document_fields = None
        self.__document_filter = None
        self.__document_id_photo = None
        self.__detected_country = None
        self.__recommendation = None

    def with_document_field(self, key, value):
        """
        :type key: str
        :type value: str or dict
        :rtype: SandboxDocumentTextDataExtractionTaskBuilder
        """
        self.__document_fields = self.__document_fields or {}
        self.__document_fields[key] = value
        return self

    def with_document_fields(self, document_fields):
        """
        :type document_fields: dict
        :rtype: SandboxDocumentTextDataExtractionTaskBuilder
        """
        self.__document_fields = document_fields
        return self

    def with_document_id_photo(self, content_type, data):
        """
        :param str content_type: the content type
        :param bytes data: the image data
        """
        self.__document_id_photo = SandboxDocumentIdPhoto(content_type, data)
        return self

    def with_document_filter(self, document_filter):
        """
        :type document_filter: SandboxDocumentFilter
        :rtype: SandboxDocumentTextDataExtractionTaskBuilder
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
        :rtype: SandboxDocumentTextDataExtractionTaskBuilder
        """
        self.__recommendation = recommendation
        return self

    def build(self):
        result = SandboxDocumentTextDataExtractionTaskResult(
            self.__document_fields,
            self.__document_id_photo,
            self.__detected_country,
            self.__recommendation,
        )
        return SandboxDocumentTextDataExtractionTask(result, self.__document_filter)
