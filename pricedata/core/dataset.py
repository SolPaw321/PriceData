from pricedata.io.loader import DataLoader, DataConfig, ClientConfig
from pricedata.transforms.candles import to_heikin_ashi
from pricedata.transforms.features import *
from pricedata.utils.dev_types.spec.spec import OHLCSpec, DropColumnsSpec, ReturnSpec
from pricedata.utils.dev_types.dev_types import ColumnTypeEnum


class Data:
    """
    The main object to operate on the price data.
    """
    def __init__(self, data_cfg: DataConfig, client_cfg: ClientConfig, loader: DataLoader):
        """
        Setting initialize parameters.

        Args:
            data_cfg (DataConfig): contextual parameters
            client_cfg (ClientConfig): client username and password
            loader (DataLoader): price data loader object
        """
        self._data_cfg = data_cfg
        self._client_cfg = client_cfg
        self._loader = loader
        self._df: pd.DataFrame | None = None

        self.feature_handler = {
            ColumnTypeEnum.OHLC4: add_ohlc4,
            ColumnTypeEnum.HLC3: add_hlc3,
            ColumnTypeEnum.HLCC4: add_hlcc4,
            ColumnTypeEnum.HL2: add_hl2,
            ColumnTypeEnum.RETURN: add_return,
            ColumnTypeEnum.LOG_RETURN: add_log_return,
        }

    def load(self) -> "Data":
        """
        Download and save data fom TradingView via tvDatafeed or load from file.

        Specify the save and read path in DataConfig.

        Return:
            Self
        """
        self._df = self._loader.load_or_fetch(self._data_cfg, self._client_cfg)
        return self

    @property
    def df(self) -> pd.DataFrame:
        """
        Get price data as DataFrame.

        Return:
            The price data
        """
        if self._df is None:
            raise RuntimeError("Call Data.load() first")
        return self._df

    def with_candles(self, *, kind: str = "standard", append: bool = False) -> "Data":
        """
        Transform candles to a specified kind.

        Currently, supported kinds:
        {supported_kinds}

        Args:
            kind (str): specified kind
            append (bool): if true, append new columns: ha_open, ha_high, ha_low, ha_close. Otherwise, rewrite open,
                        high, low, close. Default is true.
        Return:
            Data object.
        """
        if kind.lower() in ("heikin_ashi", "heiken ashi", "ha"):
            self._df = to_heikin_ashi(self.df, append)
        elif kind.lower() == "standard":
            pass
        else:
            raise ValueError(f"Unknown candle type: {kind}")
        return self

    def with_features(self, spec: OHLCSpec | ReturnSpec = None) -> "Data":
        """
        Allows you to add columns such as:
        OHLC4, HLC3, return, logarithmic return

        
        """
        for feature_kind in spec.feature_kinds:
            handler_ = self.feature_handler[feature_kind]
            if handler_:
                handler_(self._df, spec=spec)

        return self

    def with_states(self) -> "Data":
        return self

    def drop_columns(self, spec: DropColumnsSpec):
        self._df = self._df.drop(columns=spec.cols)

    def save(self) -> None:
        self._loader.save(self.df, self._data_cfg)
