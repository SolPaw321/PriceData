from attrs import define, field
from pricedata.utils.dev_types.dev_types import _normalize, CandleKind, ColumnType, ColumnTypeEnum


@define(slots=True, kw_only=True)
class DropColumnsSpec:
    """
    Attr for dropping columns specyfications.
    """
    cols: str | list[str] | ColumnType | list[ColumnType] = field(converter=_normalize)

    def __attrs_post_init__(self):
        if isinstance(self.cols, str | ColumnType):
            self.cols = [self.cols]

        if isinstance(self.cols, list):
            self.cols = [
                ColumnType[col] if isinstance(col, str) else col
                for col in self.cols
            ]


@define(slots=True, kw_only=True)
class OHLCSpec:
    """
    Attr for OHLC column specification.
    """
    feature_kinds: str | list[str] | ColumnType | list[ColumnType] = field(converter=_normalize, default="ohlc4")
    candle_kinds: str | list[str] | CandleKind | list[CandleKind] = field(converter=_normalize, default="standard")

    def __attrs_post_init__(self):
        if isinstance(self.feature_kinds, str | ColumnType):
            self.feature_kinds = [self.feature_kinds]

        self.feature_kinds = [
            ColumnType[fk] if isinstance(fk, str) else fk
            for fk in self.feature_kinds
        ]
        self.feature_kinds = list(dict.fromkeys(self.feature_kinds))

        if isinstance(self.candle_kinds, str | CandleKind):
            self.candle_kinds = [self.candle_kinds]

        self.candle_kinds = [
            CandleKind[ck] if isinstance(ck, str) else ck
            for ck in self.candle_kinds
        ]
        self.candle_kinds = list(dict.fromkeys(self.candle_kinds))


@define(slots=True, kw_only=True)
class ReturnSpec:
    """
    Attr for return column specification.
    """
    feature_kinds: str | list[str] | ColumnType | list[ColumnType] = field(converter=_normalize, default='return')
    sources: str | list[str] | ColumnType | list[ColumnType] = field(converter=_normalize, default='close')

    def __attrs_post_init__(self):
        if not self.feature_kinds:
            self.feature_kinds = ['return']

        if isinstance(self.feature_kinds, str | ColumnType):
            self.feature_kinds = [self.feature_kinds]

        self.feature_kinds = [
            ColumnType[fk] if isinstance(fk, str) else fk
            for fk in self.feature_kinds
        ]

        if not self.sources:
            self.sources = [ColumnTypeEnum.CLOSE]

        if isinstance(self.sources, str | ColumnType):
            self.sources = [self.sources]

        self.sources = [
            ColumnType[s] if (
                        isinstance(s, str) and ColumnType[s] not in (ColumnTypeEnum.VOLUME, ColumnTypeEnum.SYMBOL))
            else s
            for s in self.sources
        ]
