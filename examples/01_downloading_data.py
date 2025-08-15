from pricedata.io.loader import DataConfig, ClientConfig
from pathlib import Path

data_config = DataConfig(
    symbol="TVC:NDQ",
    interval='1d',
    n_bars=1000,
    base_dir=Path(__file__).parent / "data"
)

client_config = ClientConfig(
    user_name=None,  # or your username on TradingView
    password=None  # or your password to TradingView
)

data =