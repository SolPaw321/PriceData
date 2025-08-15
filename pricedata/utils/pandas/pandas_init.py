from pandas import set_option


def pandas_set_up_func(is_max_rows=True, is_max_cols=True, is_max_colwidth=True, is_expand=True):
    set_option('display.max_rows', None) if is_max_rows else None
    set_option('display.max_columns', None) if is_max_cols else None
    set_option('display.max_colwidth', None) if is_max_colwidth else None
    set_option('display.expand_frame_repr', False) if is_expand else None
