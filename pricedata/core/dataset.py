import pandas as pd
from pricedata.io.loader import DataLoader, DataConfig, ClientConfig
from pricedata.transforms.candles import to_heikin_ashi


class Data:
    def __init__(self, cfg: DataConfig, client_cfg: ClientConfig, loader: DataLoader):
        self._cfg = cfg
        self._client_cfg = client_cfg
        self._loader = loader
        self._df: pd.DataFrame | None = None

    def load(self) -> "Data":
        self._df = self._loader.load_or_fetch(self._cfg, self._client_cfg)
        return self

    @property
    def df(self) -> pd.DataFrame:
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

    def with_features(self) -> "Data":
        return self

    def with_states(self) -> "Data":
        return self

    def save(self) -> None:
        self._loader.save(self.df, self._cfg)
