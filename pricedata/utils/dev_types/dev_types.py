from enum import StrEnum, Enum
import re
Enums = Enum | StrEnum


class CandleKindEnum(StrEnum):
    """
    StrEnum for handling candle kinds.
    """
    STANDARD = "standard"
    HA = "ha"


class ColumnTypeEnum(StrEnum):
    """
    StrEnum for handling every column name.
    """
    VOLUME = "volume"
    SYMBOL = "symbol"
    RETURN = "return"
    RETURN_ = "return-"
    LOG_RETURN = "log-return"
    LOG_RETURN_ = "log-return-"

    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"

    OPEN_HA = "open-ha"
    HIGH_HA = "high-ha"
    LOW_HA = "low-ha"
    CLOSE_HA = "close-ha"

    OHLC4 = "ohlc4"
    OHLC4_HA = "ohlc4-ha"

    HLC3 = "hlc3"
    HLC3_HA = "hlc3-ha"

    HLCC4 = "hlcc4"
    HLCC4_HA = "hlcc4-ha"

    HL2 = "hl2"
    HL2_HA = "hl2-ha"


class ColumnTypeSetEnum(Enum):
    """
    Enum for handling every set of specific columns names.
    """
    OTHERS = ["volume", "symbol"]

    OHLC = ["open", "high", "low", "close"]
    OHLC_HA = ["open-ha", "high-ha", "low-ha", "close-ha"]

    HLC = ["high", "low", "close"]
    HLC_HA = ["high-ha", "low-ha", "close-ha"]

    HLCC = ["high", "low", "close", "close"]
    HLCC_HA = ["high-ha", "low-ha", "close-ha", "close-ha"]

    HL = ["high", "low"]
    HL_HA = ["high-ha", "low-ha"]

    OC_HA = ["open-ha", "close-ha"]


def _normalize(s: str | list[str]) -> str | list[str]:
    """
    Normalize the input text.

    Normalization process:
    -> replace every special character (including `_`) with `-`
    -> strip the `-` off text
    -> lower the text

    Args:
        s (str | list[str]): text or list of texts to normalize
    Return:
        Normalized text. The type is the same as `s` input parameter.
    """
    if isinstance(s, str):
        return re.sub(r"(?:\W|_)+", "-", s).strip("-").lower()

    if any(isinstance(s_, list) for s_ in s):
        flattened_s = []
        for s_element in s:
            if isinstance(s_element, list):
                flattened_s.extend(s_element)
            else:
                flattened_s.append(s_element)
        s = flattened_s
    return [re.sub(r"(?:\W|_)+", "-", x).strip("-").lower() for x in s]


class Registry:
    """
    Class using for register allowed input types aliases.
    """
    _map: dict[str, Enums] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._map = {}

    @classmethod
    def register(cls, value: Enums, *aliases: str):
        """
        Assign real value to aliases.

        Args:
            value (Enums): real value
            aliases (str): aliases
        """
        for a in aliases:
            cls._map[_normalize(a)] = value

    @classmethod
    def __class_getitem__(cls, key: str) -> Enums:
        if key in cls.registered_keys():
            return cls._map[_normalize(key)]
        raise KeyError(f"The {key} is not registered. Please use one of: {cls.registered_keys()}")

    @classmethod
    def registered_keys(cls):
        """
        Return all registered aliases.

        Return:
             All registered aliases
        """
        return tuple(cls._map.keys())


class CandleKind(Registry):
    value = None  # without this IDE underlining e.g.: CandleKind["std"].value


class ColumnType(Registry):
    value = None


class ColumnTypeSet(Registry):
    value = None

