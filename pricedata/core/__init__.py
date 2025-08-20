from pricedata.core.dataset import Data

SUPPORTED_CANDLES = {"standard", "heiken ashi"}

Data.with_candles.__doc__ = Data.with_candles.__doc__.format(
    supported_kinds=", ".join(SUPPORTED_CANDLES)
)
