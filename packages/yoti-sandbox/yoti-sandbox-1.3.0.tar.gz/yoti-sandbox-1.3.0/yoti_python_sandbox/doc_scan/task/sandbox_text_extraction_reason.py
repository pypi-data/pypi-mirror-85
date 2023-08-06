from yoti_python_sdk.utils import YotiSerializable

VALUE_QUALITY = "QUALITY"
VALUE_USER_ERROR = "USER_ERROR"


class SandboxTextDataExtractionReason(YotiSerializable):
    def __init__(self, value, detail):
        self.__value = value
        self.__detail = detail

    def to_json(self):
        obj = {
            "value": self.__value,
        }
        if self.__detail is not None:
            obj["detail"] = self.__detail
        return obj


class SandboxTextDataExtractionReasonBuilder(object):
    def __init__(self):
        self.__value = None
        self.__detail = None

    def for_quality(self):
        """
        :rtype: SandboxTextDataExtractionReasonBuilder
        """
        self.__value = VALUE_QUALITY
        return self

    def for_user_error(self):
        """
        :rtype: SandboxTextDataExtractionReasonBuilder
        """
        self.__value = VALUE_USER_ERROR
        return self

    def with_detail(self, detail):
        """
        :param str detail: the reason detail
        :rtype: SandboxTextDataExtractionReasonBuilder
        """
        self.__detail = detail
        return self

    def build(self):
        return SandboxTextDataExtractionReason(self.__value, self.__detail)
