import pandas as pd


def to_heikin_ashi(df: pd.DataFrame, append: bool) -> pd.DataFrame:
    """
    Transform given candles to heikin ashi.

    Args:
        df (pd.DataFrame): data for which candles are transformed
        append (bool): if true, append new columns: ha_open, ha_high, ha_low, ha_close. Otherwise, rewrite open, high,
                        low, close. Default is true.
    Return:
        Data with transformed candles.

    """
    # check for all required columns
    required = {"open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        print(f"Missing columns for HEIKIN ASHI: {sorted(missing)}. The kind of candles has not been changed.")
        return df

    data_copy = df.copy()

    # calculate ha candles
    data_copy["ha_close"] = (data_copy["open"] + data_copy["high"] + data_copy["low"] + data_copy["close"]) / 4.0
    data_copy["ha_open"] = data_copy["open"]
    data_copy.loc[data_copy.index[1:], "ha_open"] = (
        (data_copy["ha_open"].shift(1) + data_copy["ha_close"]
         .shift(1)) / 2.0).iloc[1:]
    data_copy["ha_high"] = data_copy[["high", "ha_open", "ha_close"]].max(axis=1)
    data_copy["ha_low"] = data_copy[["low", "ha_open", "ha_close"]].min(axis=1)

    if not append:
        data_copy[["open", "high", "low", "close"]] = data_copy[["ha_open", "ha_high", "ha_low", "ha_close"]]
    return data_copy
