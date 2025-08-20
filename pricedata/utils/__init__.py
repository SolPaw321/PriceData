from .dev_types.dev_types import *

CandleKind.register(CandleKindEnum.STANDARD,
                    "standard", "std", "jap", "japanese", "japan", "origin", "s")
CandleKind.register(CandleKindEnum.HA,
                    "heikin-ashi", "heiken ashi", "ha", "h-a")


ColumnType.register(ColumnTypeEnum.VOLUME,
                    "volume", "v")
ColumnType.register(ColumnTypeEnum.SYMBOL,
                    "symbol", "s")
ColumnType.register(ColumnTypeEnum.RETURN,
                    "return", "r")
ColumnType.register(ColumnTypeEnum.RETURN_,
                    "return-", "r-")
ColumnType.register(ColumnTypeEnum.LOG_RETURN,
                    "log-return", "log-r", "l-r", "l-return")
ColumnType.register(ColumnTypeEnum.LOG_RETURN_,
                    "log-return-", "log-r-", "l-r-", "l-return-")

ColumnType.register(ColumnTypeEnum.OPEN,
                    "open", "o")
ColumnType.register(ColumnTypeEnum.HIGH,
                    "high", "h")
ColumnType.register(ColumnTypeEnum.LOW,
                    "low", "l")
ColumnType.register(ColumnTypeEnum.CLOSE,
                    "close", "c")
ColumnType.register(ColumnTypeEnum.OPEN_HA,
                    "open-ha", "o-ha", "open-h-a", "o-h-a")
ColumnType.register(ColumnTypeEnum.HIGH_HA,
                    "high-ha", "h-ha", "high-h-a", "h-h-a")
ColumnType.register(ColumnTypeEnum.LOW_HA,
                    "low-ha", "l-ha", "low-h-a", "l-h-a")
ColumnType.register(ColumnTypeEnum.CLOSE_HA,
                    "close-ha", "c-ha", "close-h-a", "c-h-a")
ColumnType.register(ColumnTypeEnum.OHLC4,
                    "ohlc4", "o-h-l-c-4", "ohlc-4")
ColumnType.register(ColumnTypeEnum.OHLC4_HA,
                    "ohlc4-ha", "o-h-l-c-4-ha", "ohlc-4-ha", "ohlc4-h-a", "o-h-l-c-4-h-a", "ohlc-4-h-a")
ColumnType.register(ColumnTypeEnum.HLC3,
                    "hlc3", "h-l-c-3", "hlc-3")
ColumnType.register(ColumnTypeEnum.HLC3_HA,
                    "hlc3-ha", "h-l-c-3-ha", "hlc-3-ha", "hlc3-h-a", "h-l-c-3-h-a", "hlc-3-h-a")
ColumnType.register(ColumnTypeEnum.HLCC4,
                    "hlcc4", "h-l-c-c-4", "hlcc-4")
ColumnType.register(ColumnTypeEnum.HLCC4_HA,
                    "hlcc4-ha", "h-l-c-c-4-ha", "hlcc-4-ha", "h-l-c-c-4-h-a", "h-l-c-c-4-h-a", "hlcc-4-h-a")
ColumnType.register(ColumnTypeEnum.HL2,
                    "hl2", "h-l-2", "hl-2")
ColumnType.register(ColumnTypeEnum.HL2_HA,
                    "hl2-ha", "h-l-2-ha", "hl-2-ha", "hl2-h-a", "h-l-2-h-a", "hl-2-h-a")

ColumnTypeSet.register(ColumnTypeSetEnum.OHLC,
                       "ohlc", "o-h-l-c")
ColumnTypeSet.register(ColumnTypeSetEnum.OHLC_HA,
                       "ohlc-ha", "o-h-l-c-h-a", "ohlc-h-a", "o-h-l-c-ha")
ColumnTypeSet.register(ColumnTypeSetEnum.HLC,
                       "hlc", "h-l-c")
ColumnTypeSet.register(ColumnTypeSetEnum.HLC_HA,
                       "hlc-ha", "h-l-c-h-a", "hlc-h-a", "h-l-c-ha")
ColumnTypeSet.register(ColumnTypeSetEnum.HLCC,
                       "hlcc", "h-l-c-c")
ColumnTypeSet.register(ColumnTypeSetEnum.HLCC_HA,
                       "hlcc-ha", "h-l-c-c-h-a", "hlcc-h-a", "h-l-c-c-ha")
ColumnTypeSet.register(ColumnTypeSetEnum.HL,
                       "hl", "h-l")
ColumnTypeSet.register(ColumnTypeSetEnum.HL_HA,
                       "hl-ha", "h-l-h-a", "hl-h-a", "h-l-ha")
ColumnTypeSet.register(ColumnTypeSetEnum.OC_HA,
                       "oc-ha", "o-c-h-a", "oc-h-a", "o-c-ha")
