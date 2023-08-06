from yoti_python_sdk.utils import YotiSerializable

from .check.sandbox_document_authenticity_check import (  # noqa: F401
    SandboxDocumentAuthenticityCheck,
)
from .check.sandbox_document_face_match_check import (  # noqa: F401
    SandboxDocumentFaceMatchCheck,
)
from .check.sandbox_document_text_data_check import (  # noqa: F401
    SandboxDocumentTextDataCheck,
)
from .check.sandbox_liveness_check import SandboxLivenessCheck  # noqa: F401


class SandboxCheckReports(YotiSerializable):
    def __init__(
        self,
        document_authenticity_check=None,
        document_face_match_check=None,
        document_text_data_check=None,
        liveness_checks=None,
        async_report_delay=None,
        id_document_comparison_checks=None,
        supplementary_document_text_data_checks=None,
    ):
        if document_authenticity_check is None:
            document_authenticity_check = []

        if document_text_data_check is None:
            document_text_data_check = []

        if document_face_match_check is None:
            document_face_match_check = []

        if liveness_checks is None:
            liveness_checks = []

        if id_document_comparison_checks is None:
            id_document_comparison_checks = []

        if supplementary_document_text_data_checks is None:
            supplementary_document_text_data_checks = []

        self.__document_authenticity_check = document_authenticity_check
        self.__document_face_match_check = document_face_match_check
        self.__document_text_data_check = document_text_data_check
        self.__liveness_checks = liveness_checks
        self.__async_report_delay = async_report_delay
        self.__id_document_comparison_checks = id_document_comparison_checks
        self.__supplementary_document_text_data_checks = (
            supplementary_document_text_data_checks
        )

    @property
    def document_authenticity_checks(self):
        return self.__document_authenticity_check

    @property
    def document_face_match_checks(self):
        return self.__document_face_match_check

    @property
    def document_text_data_checks(self):
        return self.__document_text_data_check

    @property
    def liveness_checks(self):
        return self.__liveness_checks

    @property
    def async_report_delay(self):
        return self.__async_report_delay

    @property
    def id_document_comparison_checks(self):
        return self.__id_document_comparison_checks

    @property
    def supplementary_document_text_data_checks(self):
        return self.__supplementary_document_text_data_checks

    def to_json(self):
        return {
            "ID_DOCUMENT_AUTHENTICITY": self.__document_authenticity_check,
            "ID_DOCUMENT_TEXT_DATA_CHECK": self.__document_text_data_check,
            "ID_DOCUMENT_FACE_MATCH": self.__document_face_match_check,
            "LIVENESS": self.__liveness_checks,
            "ID_DOCUMENT_COMPARISON": self.__id_document_comparison_checks,
            "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK": self.__supplementary_document_text_data_checks,
            "async_report_delay": self.__async_report_delay,
        }


class SandboxCheckReportsBuilder(object):
    def __init__(self):
        self.__document_authenticity_checks = []
        self.__document_face_match_checks = []
        self.__document_text_data_checks = []
        self.__liveness_checks = []
        self.__async_report_delay = None
        self.__id_document_comparison_check = []
        self.__supplementary_document_text_data_checks = []

    def with_document_authenticity_check(self, document_authenticity_check):
        """
        Add a document authenticity check expectation

        :param document_authenticity_check: the document authenticity check
        :type document_authenticity_check: SandboxDocumentAuthenticityCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__document_authenticity_checks.append(document_authenticity_check)
        return self

    def with_document_face_match_check(self, document_face_match_check):
        """
        Add a document face match check expectation

        :param document_face_match_check: the document face match check
        :type document_face_match_check: SandboxDocumentFaceMatchCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__document_face_match_checks.append(document_face_match_check)
        return self

    def with_document_text_data_check(self, document_text_data_check):
        """
        Add a document text data check expectation

        :param document_text_data_check: the document text data check
        :type document_text_data_check: SandboxDocumentTextDataCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__document_text_data_checks.append(document_text_data_check)
        return self

    def with_liveness_check(self, liveness_check):
        """
        Adds a liveness check to the list of checks

        :param liveness_check: the liveness check
        :type liveness_check: SandboxLivenessCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__liveness_checks.append(liveness_check)
        return self

    def with_async_report_delay(self, async_report_delay):
        """
        The Async report delay is a timer (in seconds)
        which simulates a delay between the Doc Scan
        iFrame user journey and the result of the report,
        set by your expectation.
        By using this facility you can effectively handle
        pending states, or results that are not returned
        instantly (such as manual checks).

        :param async_report_delay: delay in seconds
        :type async_report_delay: int
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__async_report_delay = async_report_delay
        return self

    def with_id_document_comparison_check(self, id_document_comparison_check):
        """
        Add an ID document comparison check expectation

        :param id_document_comparison_check: the ID document comparison check
        :type id_document_comparison_check: SandboxIdDocumentComparisonCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__id_document_comparison_check.append(id_document_comparison_check)
        return self

    def with_supplementary_document_text_data_check(
        self, supplementary_document_text_data_check
    ):
        """
        Add a supplementary document text data check expectation

        :param supplementary_document_text_data_check: the document text data check
        :type supplementary_document_text_data_check: SandboxSupplementaryDocumentTextDataCheck
        :return: the builder
        :rtype: SandboxCheckReportsBuilder
        """
        self.__supplementary_document_text_data_checks.append(
            supplementary_document_text_data_check
        )
        return self

    def build(self):
        return SandboxCheckReports(
            self.__document_authenticity_checks,
            self.__document_face_match_checks,
            self.__document_text_data_checks,
            self.__liveness_checks,
            self.__async_report_delay,
            self.__id_document_comparison_check,
            self.__supplementary_document_text_data_checks,
        )
