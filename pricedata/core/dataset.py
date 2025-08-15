import pandas as pd
from ..io.loader import DataLoader, DataConfig, ClientConfig


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
            raise RuntimeError("Call .load() first")
        return self._df

    def with_candles(self) -> "Data":
        return self

    def with_features(self) -> "Data":
        return self

    def with_states(self) -> "Data":
        return self

    def save(self) -> None:
        self._loader.save(self.df, self._cfg)
