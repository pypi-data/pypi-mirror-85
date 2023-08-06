import pandas as _pd


def bars_to_pandas(bars_json, group_by="column"):
    """ convert bars payload to pandas dataframe """
    dfs = newbars = {}

    for dt, values in bars_json.items():
        for ticker, ohlc in values.items():
            ohlc['ts'] = dt
            if ticker not in newbars:
                newbars[ticker] = []
            newbars[ticker].append(ohlc)

    for ticker, bars in newbars.items():
        dfs[ticker] = _pd.DataFrame(bars)
        dfs[ticker].set_index("ts", inplace=True)
        dfs[ticker].index = _pd.to_datetime(dfs[ticker].index)
        for col in dfs[ticker].columns:
            dfs[ticker][col] = _pd.to_numeric(dfs[ticker][col])

    df = _pd.concat(dfs.values(), axis=1, keys=dfs.keys())
    df.sort_index(level=0, axis=1, inplace=True)

    if group_by == 'column':
        df.columns = df.columns.swaplevel(0, 1)
        df.sort_index(level=0, axis=1, inplace=True)
