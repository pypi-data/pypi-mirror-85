from deprecated import deprecated
from yoti_python_sdk.utils import YotiSerializable


class SandboxTaskResults(YotiSerializable):
    def __init__(
        self,
        id_document_text_extraction_tasks=None,
        supplementary_document_text_extraction_tasks=None,
    ):
        if id_document_text_extraction_tasks is None:
            id_document_text_extraction_tasks = []

        if supplementary_document_text_extraction_tasks is None:
            supplementary_document_text_extraction_tasks = []

        self.__id_document_text_extraction_tasks = id_document_text_extraction_tasks
        self.__supplementary_document_text_extraction_tasks = (
            supplementary_document_text_extraction_tasks
        )

    @property
    @deprecated
    def text_extraction_task(self):
        return self.__id_document_text_extraction_tasks

    def to_json(self):
        return {
            "ID_DOCUMENT_TEXT_DATA_EXTRACTION": self.__id_document_text_extraction_tasks,
            "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION": self.__supplementary_document_text_extraction_tasks,
        }


class SandboxTaskResultsBuilder(object):
    def __init__(self):
        self.__id_document_text_extraction_tasks = []
        self.__supplementary_document_text_extraction_tasks = []

    def with_text_extraction_task(self, id_document_text_extraction_task):
        self.__id_document_text_extraction_tasks.append(
            id_document_text_extraction_task
        )
        return self

    def with_supplementary_document_text_extraction_task(
        self, supplementary_document_text_extraction_task
    ):
        self.__supplementary_document_text_extraction_tasks.append(
            supplementary_document_text_extraction_task
        )
        return self

    def build(self):
        return SandboxTaskResults(
            self.__id_document_text_extraction_tasks,
            self.__supplementary_document_text_extraction_tasks,
        )
