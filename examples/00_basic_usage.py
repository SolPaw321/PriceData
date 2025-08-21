"""
Example 0: Basic usage

In this example, we present the basic usage of PriceData package.

You will learn step-by-step how to:
-> setting data configuration
-> setting client configuration
-> initializing loader
"""

# require imports
from pathlib import Path
from pricedata.io.loader import DataConfig, ClientConfig, DataLoader
from pricedata.core.dataset import Data
from pricedata.utils.pandas.pandas_init import pandas_set_up_func
from pricedata.utils.dev_types.spec.spec import OHLCSpec, DropColumnsSpec, ReturnSpec

# set up pandas display range (for visual purposes only, you can skip this)
pandas_set_up_func(is_max_cols=True)


# ---| PART 1:  LOADING DATA |--- #
# set up data configuration
data_config = DataConfig(
    symbol="TVC:NDQ",  # exchange:ticker
    interval='1d',
    n_bars=1000,
    base_dir=Path(__file__).parent.parent / "data"  # to save downloaded data if it does not exist
)

# set up client configuration
client_config = ClientConfig(
    user_name=None,  # or your username on TradingView, e.g. "User1"
    password=None  # or your password to TradingView, e.g. "12345"
)

# initialize loader
loader = DataLoader()

# load data from csv file or from Trading View via tvDatafeed
# this code will generate `standard` and `heikin ashi` candles
data = Data(data_config, client_config, loader)
data.load().with_candles(  # fluent API
    kind='ha',  # candle type
    append=True  # if the type is not `standard`, you can include columns of different candles (here: heikin ashi)
                 # if the value is True,
                 # or override the `standard` type if the value is False
)

# now print the results
print("Loaded data:")
print(data.df.head(5))

# ---| PART 2:  ADDING FEATURES |--- #

# set up OHLC specification
# this code specifies the ohlc4, hlc3, hl2 and hlcc4 columns on `standard` and `heikin ashi` candles
spec = OHLCSpec(
    feature_kinds=["ohlc4", "hlc-3", "hl2", "hlcc4"],
    candle_kinds=["std", "ha"]
)

# implement your OHLC specification
data.with_features(spec)

# now print the results
print("Data with some features:")
print(data.df.head(5))


# set up Return specification
# this code specifies the classical return column on source `close`
spec = ReturnSpec(
    feature_kinds="r",
    sources="close"
)

# implement your Return specification
data.with_features(spec)

# if you want, you can specify logarithmic return
spec = ReturnSpec(
    feature_kinds="log-return",
    sources="ohlc4"
)

# implement your Return specification
data.with_features(spec)

# now print the results
print("Data with return column:")
print(data.df.head(5))

# ---| PART 3:  DROP UNNECESSARY COLUMNS |--- #

# set up Drop specification
# this code specifies columns (symbol and volume) to be dropped
spec = DropColumnsSpec(
    cols=["symbol", "volume"]
)
data.drop_columns(spec)

# now print the results
print("Data without symbol and volume")
print(data.df.head(5))

#