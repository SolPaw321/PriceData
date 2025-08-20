import pandas as pd
import numpy as np
from pricedata.utils.dev_types.spec.spec import OHLCSpec, ReturnSpec
from pricedata.utils.dev_types.dev_types import ColumnTypeEnum, ColumnTypeSetEnum, CandleKindEnum


handler = {
    CandleKindEnum.STANDARD: {
        ColumnTypeEnum.OHLC4: (ColumnTypeEnum.OHLC4.value, ColumnTypeSetEnum.OHLC.value),
        ColumnTypeEnum.HLC3: (ColumnTypeEnum.HLC3.value, ColumnTypeSetEnum.HLC.value),
        ColumnTypeEnum.HL2: (ColumnTypeEnum.HL2.value, ColumnTypeSetEnum.HL.value),
        ColumnTypeEnum.HLCC4: (ColumnTypeEnum.HLCC4.value, ColumnTypeSetEnum.HLCC.value)
    },
    CandleKindEnum.HA: {
        ColumnTypeEnum.OHLC4: (ColumnTypeEnum.OHLC4_HA.value, ColumnTypeSetEnum.OHLC_HA.value),
        ColumnTypeEnum.HLC3: (ColumnTypeEnum.HLC3_HA.value, ColumnTypeSetEnum.HLC_HA.value),
        ColumnTypeEnum.HL2: (ColumnTypeEnum.HL2_HA.value, ColumnTypeSetEnum.HL_HA.value),
        ColumnTypeEnum.HLCC4: (ColumnTypeEnum.HLCC4_HA.value, ColumnTypeSetEnum.HLCC_HA.value)
    }
}


def add_ohlc4(df: pd.DataFrame, *, spec: OHLCSpec):
    """
    Add OHLC4 column.

    Args:
        df (pd.DataFrame): data from which OHLC4 column is created
        spec (OHLCSpec): specification
    """
    for candle_kind in spec.candle_kinds:
        OHLC4, OHLC = handler[candle_kind][ColumnTypeEnum.OHLC4]

        df[OHLC4] = df[OHLC].sum(axis=1) / len(OHLC)


def add_hlc3(df: pd.DataFrame, *, spec: OHLCSpec):
    """
    Add HLC3 column.

    Args:
        df (pd.DataFrame): data from which HLC3 column is created
        spec (OHLCSpec): specification
    """
    for candle_kind in spec.candle_kinds:
        HLC3, HLC = handler[candle_kind][ColumnTypeEnum.HLC3]

        df[HLC3] = df[HLC].sum(axis=1) / len(HLC)


def add_hlcc4(df: pd.DataFrame, *, spec: OHLCSpec):
    """
    Add HLCC4 column.

    Args:
        df (pd.DataFrame): data from which HLCC4 column is created
        spec (OHLCSpec): specification
    """
    for candle_kind in spec.candle_kinds:
        HLCC4, HLCC = handler[candle_kind][ColumnTypeEnum.HLCC4]

        df[HLCC4] = df[HLCC].sum(axis=1) / len(HLCC)


def add_hl2(df: pd.DataFrame, *, spec: OHLCSpec):
    """
    Add HL2 column.

    Args:
        df (pd.DataFrame): data from which HL2 column is created
        spec (OHLCSpec): specification
    """
    for candle_kind in spec.candle_kinds:
        HL2, HL = handler[candle_kind][ColumnTypeEnum.HL2]

        df[HL2] = df[HL].sum(axis=1) / len(HL)


def add_return(df: pd.DataFrame, *, spec: ReturnSpec):
    """
    Add classical return column.

    Args:
        df (pd.DataFrame): data from which return column is created
        spec (OHLCSpec): specification
    """
    for src in spec.sources:
        ret_col_name = ColumnTypeEnum.RETURN_ + src
        series = df[src]
        df[ret_col_name] = series.pct_change().fillna(0.0)


def add_log_return(df: pd.DataFrame, *, spec: ReturnSpec):
    """
    Add logarithmic return column.

    Args:
        df (pd.DataFrame): data from which logarithmic return column is created
        spec (OHLCSpec): specification
    """
    for src in spec.sources:
        ret_col_name = ColumnTypeEnum.LOG_RETURN_ + src
        series = df[src]
        df[ret_col_name] = np.log(series / series.shift(1)).fillna(0.0)

