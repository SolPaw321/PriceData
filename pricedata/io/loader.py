from dataclasses import dataclass
from pathlib import Path
import time

import pandas as pd

try:
    from tvDatafeed import TvDatafeed, Interval
except ModuleNotFoundError as e:
    # even if TvDatafeed is not installed, you can still ise reading data from a csv file
    TvDatafeed = object


    @dataclass(slots=True)
    class Interval:
        in_1_min = "1"
        in_3_min = "3"
        in_5_min = "5"
        in_15_min = "15"
        in_30_min = "30"
        in_45_min = "45"
        in_1_hour = "60"
        in_2_hour = "120"
        in_3_hour = "180"
        in_4_hour = "240"
        in_daily = "1D"
        in_weekly = "1W"
        in_monthly = "1M"


@dataclass(slots=True)
class DataConfig:
    """
    Data configuration settings.
    """
    symbol: str
    interval: str
    n_bars: int
    base_dir: Path
    index_name: str = "Date"


@dataclass(slots=True)
class ClientConfig:
    """
    Client configuration settings.
    """
    user_name: str | None = None
    password: str | None = None


@dataclass(slots=True)
class DataLoader:
    """
    The data loader class.
    """
    client: TvDatafeed | None = None

    @staticmethod
    def _csv_path(cfg: DataConfig) -> Path:
        """
        Crate a path for saving data into csv file.

        Args:
            cfg (DataConfig): data configuration settings

        Return:
            Path: the path to csv file

        """
        sym = cfg.symbol.replace(":", "_")
        return (cfg.base_dir / sym / f"{cfg.interval}_{cfg.n_bars}.csv").resolve()

    def load_or_fetch(self, cfg: DataConfig, client_cfg: ClientConfig) -> pd.DataFrame:
        """
        Load data from given path or fetch data from TradingView via TvDatafeed.

        Args:
            cfg (DataConfig): data configuration setting
            client_cfg (ClientConfig): client configuration settings

        Return:
            pd.DataFrame: OHLCV standard japanese candlestick price data.

        """
        p = self._csv_path(cfg)
        if p.exists():
            df = pd.read_csv(p, parse_dates=[cfg.index_name])
            df = df.set_index(cfg.index_name)
            df.index.name = cfg.index_name
            return self._normalize_df(df)

        # if a given path does not exist, then fetch data from trading view and save into a given path
        df = self._fetch_from_tv(cfg, client_cfg)
        p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(p, index=True, index_label=cfg.index_name)
        return df

    def save(self, df: pd.DataFrame, cfg: DataConfig) -> None:
        p = self._csv_path(cfg)
        p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(p, index=True, index_label=cfg.index_name)

    def _fetch_from_tv(self, cfg: DataConfig, client_cfg: ClientConfig) -> pd.DataFrame:
        """
        Download price data from TradingView via tvDatafeed in standard OHLCV japanese candlestick format.

        Args:
            cfg (DataConfig): config dataclass

        Return:
            pd.DataFrame: the OHLCV price data
        """
        if self.client is None:
            try:
                self.client: TvDatafeed | object = TvDatafeed(
                    username=client_cfg.user_name,
                    password=client_cfg.password
                )
            except Exception as expectation:
                raise RuntimeError(
                    "Failed to create TvDatafeed client. "
                    "Try to use TradingView account:"
                    "client = Client(user_name=..., password=...)"
                    "DataLoader(client=client)"
                ) from expectation

        exchange, ticker = self._split_symbol(cfg.symbol)
        tv_interval = self._map_interval(cfg.interval)

        attempts = 4
        delay = 1.0
        last_err: Exception | None = None
        for i in range(attempts):
            try:
                df = self.client.get_hist(
                    symbol=ticker,
                    exchange=exchange,
                    interval=tv_interval,
                    n_bars=cfg.n_bars,
                    fut_contract=None,
                    extended_session=False,
                )
                if df is None or len(df) == 0:
                    raise RuntimeError("TradingView returned empty data. Please try again.")
                df = self._normalize_df(df, index_name=cfg.index_name)
                return df
            except Exception as expectation:
                last_err = expectation
                time.sleep(delay)
                delay *= 2

        raise RuntimeError(
            f"Failed to retrieve data from TradingView for {cfg.symbol} @ {cfg.interval} "
            f"after {attempts} attempts. Last error: {last_err}"
        )

    @staticmethod
    def _split_symbol(symbol: str) -> tuple[str, str]:
        """
        Split a symbol into exchange and ticker.

        Args:
            symbol (str): symbol in format EXCHANGE:TICKER

        Return:
            Tuple of exchange and ticker name.

        """
        if ":" not in symbol:
            raise ValueError(
                f"Symbol '{symbol}' do not contain ':'. Use 'EXCHANGE:TICKER' format, eg. 'BINANCE:BTCUSDT'."
            )
        exchange, ticker = symbol.split(":", 1)
        if not exchange or not ticker:
            raise ValueError(f"Incorrect symbol '{symbol}'. Use 'EXCHANGE:TICKER' format, eg. 'BINANCE:BTCUSDT'.")
        return exchange, ticker

    @staticmethod
    def _map_interval(interval_str: str):
        """
        Map str interval into TvDatafeed.Interval.

        """
        s = interval_str.strip().lower()
        mapping = {
            "1m": Interval.in_1_minute,
            "3m": Interval.in_3_minute,
            "5m": Interval.in_5_minute,
            "15m": Interval.in_15_minute,
            "30m": Interval.in_30_minute,
            "45m": Interval.in_45_minute,
            "1h": Interval.in_1_hour,
            "2h": Interval.in_2_hour,
            "3h": Interval.in_3_hour,
            "4h": Interval.in_4_hour,
            "1d": Interval.in_daily,
            "1w": Interval.in_weekly,
            "1mth": Interval.in_monthly,
            "1mon": Interval.in_monthly,
            "1mo": Interval.in_monthly,
            "1m_": Interval.in_monthly,
            "1M": Interval.in_monthly,
        }
        if s in mapping:
            return mapping[s]
        alias = {"d": "1d", "w": "1w", "m": "1m"}
        if s in alias and alias[s] in mapping:
            return mapping[alias[s]]
        raise ValueError(f"Unsupported interval: '{interval_str}'")

    @staticmethod
    def _normalize_df(df: pd.DataFrame, *, index_name: str = "Date") -> pd.DataFrame:
        """
        Normalize data read from file or downloaded from TradingView.

        Normalization contains:
        -> index of type pd.dDatatimeIndex
        -> columns names in lowercase
        -> remove duplicated indexes
        -> sort indexes

        Args:
            df (pd.DataFrame): read or downloaded data
            index_name (str): preferred index name. Default is "Date"

        Return:
            Normalized data.
        """
        df_copy = df.copy()

        # make sure that index is of type pf.DatatimeIndex
        if not isinstance(df_copy.index, pd.DatetimeIndex):
            # try to find a column that can be a date index, otherwise try to convert index into pd.DatatimeIndex
            for dt_col in df_copy.columns:
                if str(dt_col).lower() in ("datetime", "date", "time"):
                    df_copy[dt_col] = pd.to_datetime(df_copy[dt_col], errors="coerce", utc=True)
                    df_copy = df_copy.set_index(dt_col)
                    break
            else:
                df_copy.index = pd.to_datetime(df_copy.index, errors="coerce", utc=True)

        # force UTC and index name
        if df_copy.index.tz is None:
            df_copy.index = df_copy.index.tz_localize("UTC")
        else:
            df_copy.index = df_copy.index.tz_convert("UTC")
        df_copy.index.name = index_name

        # normalize columns names
        df_copy.columns = [str(c).lower() for c in df_copy.columns]

        # remove duplicated index and sort index
        df_copy = df_copy[~df_copy.index.duplicated(keep="last")].sort_index()

        return df_copy
