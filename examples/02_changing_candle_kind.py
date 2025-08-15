"""
Example 2: Changing candlestick kinds

There are two equivalent ways to change candelstick types.
"""
from pricedata.io.loader import DataConfig, ClientConfig, DataLoader
from pricedata.core.dataset import Data
from pricedata.utils.pandas.pandas_init import pandas_set_up_func
from pathlib import Path


# set up pandas display range (for visual purposes only)
pandas_set_up_func(is_max_cols=True)

# initialize data configuration
data_config = DataConfig(
    symbol="TVC:NDQ",
    interval='1d',
    n_bars=1000,
    base_dir=Path(__file__).parent.parent / "data"  # to save downloaded data if it does not exist
)

# initialize client configuration
client_config = ClientConfig(
    user_name=None,  # or your username on TradingView, e.g. "User1"
    password=None  # or your password to TradingView, e.g. "12345"
)

# initialize loader
loader = DataLoader()


# -------------------------------------------
# The first way
print("The first way.")
data = Data(data_config, client_config, loader)
data.load().with_candles(kind='ha')

# print the results
print(data.df.head(10))


# -------------------------------------------
# The second way
print("The second way.")
data = Data(data_config, client_config, loader)
data.load()
data.with_candles(kind='ha')

# print the results
print(data.df.head(10))
