from yoti_python_sandbox.doc_scan.check.sandbox_check_report import SandboxCheckReport
from yoti_python_sandbox.doc_scan.check.sandbox_check_result import SandboxCheckResult
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_check import (
    SandboxDocumentCheckBuilder,
)


class SandboxSupplementaryDocumentTextDataCheckResult(SandboxCheckResult):
    def __init__(self, report, document_fields=None):
        SandboxCheckResult.__init__(self, report)
        self.__document_fields = document_fields

    @property
    def document_fields(self):
        return self.__document_fields

    def to_json(self):
        json = SandboxCheckResult.to_json(self)

        if self.document_fields is not None:
            json["document_fields"] = self.document_fields

        return json


class SandboxSupplementaryDocumentTextDataCheck(SandboxDocumentCheck):
    @staticmethod
    def builder():
        return SandboxSupplementaryDocumentTextDataCheckBuilder()


class SandboxSupplementaryDocumentTextDataCheckBuilder(SandboxDocumentCheckBuilder):
    def __init__(self):
        SandboxDocumentCheckBuilder.__init__(self)
        self.__document_fields = None

    def with_document_field(self, key, value):
        """
        :type key: str
        :type value: str or dict
        :rtype: SandboxSupplementaryDocumentTextDataCheckBuilder
        """
        self.__document_fields = self.__document_fields or {}
        self.__document_fields[key] = value
        return self

    def with_document_fields(self, document_fields):
        """
        :type document_fields: dict
        :rtype: SandboxSupplementaryDocumentTextDataCheckBuilder
        """
        self.__document_fields = document_fields
        return self

    def build(self):
        report = SandboxCheckReport(self.recommendation, self.breakdown)
        result = SandboxSupplementaryDocumentTextDataCheckResult(
            report, self.__document_fields
        )
        return SandboxSupplementaryDocumentTextDataCheck(result, self.document_filter)
