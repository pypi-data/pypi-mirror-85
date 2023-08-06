from yoti_python_sandbox.doc_scan.check.sandbox_check_report import SandboxCheckReport
from yoti_python_sandbox.doc_scan.check.sandbox_check_result import SandboxCheckResult
from yoti_python_sandbox.doc_scan.check.sandbox_check import SandboxCheck
from yoti_python_sandbox.doc_scan.check.sandbox_check import SandboxCheckBuilder


class SandboxIdDocumentComparisonCheck(SandboxCheck):
    def __init__(self, result, secondary_document_filter):
        SandboxCheck.__init__(self, result)
        self.__secondary_document_filter = secondary_document_filter

    @staticmethod
    def builder():
        return SandboxIdDocumentComparisonCheckBuilder()

    @property
    def secondary_document_filter(self):
        return self.__secondary_document_filter

    def to_json(self):
        parent = SandboxCheck.to_json(self)
        if self.secondary_document_filter is not None:
            parent["secondary_document_filter"] = self.secondary_document_filter
        return parent


class SandboxIdDocumentComparisonCheckBuilder(SandboxCheckBuilder):
    def __init__(self):
        SandboxCheckBuilder.__init__(self)
        self.__secondary_document_filter = None

    def with_secondary_document_filter(self, secondary_document_filter):
        self.__secondary_document_filter = secondary_document_filter
        return self

    def build(self):
        report = SandboxCheckReport(self.recommendation, self.breakdown)
        result = SandboxCheckResult(report)
        return SandboxIdDocumentComparisonCheck(
            result, self.__secondary_document_filter
        )
