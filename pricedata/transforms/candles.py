import pandas as pd
from pricedata.utils.dev_types.dev_types import ColumnTypeEnum, ColumnTypeSetEnum


def to_heikin_ashi(df: pd.DataFrame, append: bool) -> pd.DataFrame:
    """
    Transform given candles to heikin ashi.

    NOTE.:
    The value of the heikin ashi candles depends on the initial candle. The values may vary depending on the number of
    candles loaded.

    Args:
        df (pd.DataFrame): data for which candles are transformed
        append (bool): if true, append new columns: ha_open, ha_high, ha_low, ha_close. Otherwise, rewrite open, high,
                        low, close. Default is true.
    Return:
        Data with transformed candles.

    """
    # check for all required columns
    required = set(ColumnTypeSetEnum.OHLC.value)
    missing = required - set(df.columns)
    if missing:
        print(f"Missing columns for HEIKIN ASHI: {sorted(missing)}. The kind of candles has not been changed.")
        return df

    data_copy = df.copy()

    # calculate ha candles
    data_copy[ColumnTypeEnum.CLOSE_HA] = data_copy[ColumnTypeSetEnum.OHLC.value].sum(axis=1) / 4.0

    data_copy[ColumnTypeEnum.OPEN_HA] = data_copy[ColumnTypeEnum.OPEN]
    data_copy.loc[data_copy.index[1:], ColumnTypeEnum.OPEN_HA] = (
                                            data_copy[ColumnTypeSetEnum.OC_HA.value].sum(axis=1).shift(1) / 2.0).iloc[1:]

    data_copy[ColumnTypeEnum.HIGH_HA] = data_copy[
        [ColumnTypeEnum.HIGH, *ColumnTypeSetEnum.OC_HA.value]].max(axis=1)

    data_copy[ColumnTypeEnum.LOW_HA] = data_copy[
        [ColumnTypeEnum.LOW, *ColumnTypeSetEnum.OC_HA.value]].min(axis=1)

    if not append:
        data_copy[ColumnTypeSetEnum.OHLC.value] = data_copy[ColumnTypeSetEnum.OHLC_HA.value]
    return data_copy
