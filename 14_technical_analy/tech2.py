
import yfinance as yf
data=yf.download('NVDA',interval='1h',start='2025-01-25',end='2025-07-27',multi_level_index=False)
print(data)

import pandas_ta as ta
super=ta.supertrend(data['High'],data['Low'],data['Close'],10,3)
print(super)


import pandas as pd
import numpy as np

def supertrend(high, low, close, length=7, multiplier=3.0, offset=0, **kwargs):
    """
    Supertrend Indicator - Standalone Implementation
    
    Supertrend is an overlap indicator used to identify trend direction,
    set stop loss, identify support and resistance, and generate buy/sell signals.
    
    Args:
        high (pd.Series): Series of 'high' prices
        low (pd.Series): Series of 'low' prices
        close (pd.Series): Series of 'close' prices
        length (int): Period for ATR calculation. Default: 7
        multiplier (float): Multiplier for upper and lower bands. Default: 3.0
        offset (int): Number of periods to offset the result. Default: 0
        
    Returns:
        pd.DataFrame: Contains SUPERT, SUPERTd, SUPERTl, SUPERTs columns
    """
    
    # Input validation
    if not all(isinstance(x, pd.Series) for x in [high, low, close]):
        raise ValueError("high, low, and close must be pandas Series")
    
    if len(high) != len(low) or len(low) != len(close):
        raise ValueError("high, low, and close must have the same length")
    
    if length <= 0:
        raise ValueError("length must be positive")
        
    if multiplier <= 0:
        raise ValueError("multiplier must be positive")
    
    # Ensure we have enough data
    if len(close) < length:
        raise ValueError(f"Not enough data. Need at least {length} periods")
    
    # Calculate HL2 (typical price)
    hl2 = (high + low) / 2
    
    # Calculate True Range components
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    # True Range is the maximum of the three components
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR using Simple Moving Average
    atr = true_range.rolling(window=length).mean()
    
    # Calculate basic upper and lower bands
    matr = multiplier * atr
    basic_upperband = hl2 + matr
    basic_lowerband = hl2 - matr
    
    # Initialize arrays
    m = len(close)
    final_upperband = np.full(m, np.nan)
    final_lowerband = np.full(m, np.nan)
    direction = np.full(m, 1)  # Start with bullish direction
    supertrend = np.full(m, np.nan)
    
    # Initialize first valid values
    for i in range(length):
        direction[i] = 1  # Start with bullish direction
    
    # Copy basic bands to final bands initially
    final_upperband = basic_upperband.copy().values
    final_lowerband = basic_lowerband.copy().values
    
    # Initialize first valid values
    for i in range(length):
        direction[i] = 1  # Start with bullish direction
    
    # Copy basic bands to final bands initially
    final_upperband = basic_upperband.copy().values
    final_lowerband = basic_lowerband.copy().values
    
    # Calculate final bands and supertrend following original logic
    for i in range(1, m):
        # Direction logic first (matches original)
        if close.iloc[i] > final_upperband[i - 1]:
            direction[i] = 1
        elif close.iloc[i] < final_lowerband[i - 1]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]
            
            # Adjust bands based on direction (matches original logic)
            if direction[i] > 0 and final_lowerband[i] < final_lowerband[i - 1]:
                final_lowerband[i] = final_lowerband[i - 1]
            if direction[i] < 0 and final_upperband[i] > final_upperband[i - 1]:
                final_upperband[i] = final_upperband[i - 1]
        
        # Set supertrend and long/short values
        if direction[i] > 0:
            supertrend[i] = final_lowerband[i]
        else:
            supertrend[i] = final_upperband[i]
    
    # Create long and short arrays (matching original logic)
    long_values = np.full(m, np.nan)
    short_values = np.full(m, np.nan)
    
    for i in range(m):
        if direction[i] > 0:
            long_values[i] = supertrend[i]
        else:
            short_values[i] = supertrend[i]
    
    # Create result DataFrame
    _props = f"_{length}_{multiplier}"
    result_df = pd.DataFrame({
        f"SUPERT{_props}": supertrend,
        f"SUPERTd{_props}": direction,
        f"SUPERTl{_props}": long_values,
        f"SUPERTs{_props}": short_values,
    }, index=close.index)
    
    result_df.name = f"SUPERT{_props}"
    result_df.category = "overlap"
    
    # Apply offset if specified
    if offset != 0:
        result_df = result_df.shift(offset)
    
    # Handle fill options
    if "fillna" in kwargs:
        result_df.fillna(kwargs["fillna"], inplace=True)
    
    if "fill_method" in kwargs:
        result_df.fillna(method=kwargs["fill_method"], inplace=True)
    
    return result_df



super=supertrend(data['High'],data['Low'],data['Close'],10,3)
print(super)

# import mplfinance as mpf
# a=mpf.make_addplot(super['SUPERTl_7_3.0'],color='black')
# b=mpf.make_addplot(super['SUPERTs_7_3.0'],color='blue')

# mpf.plot(data,type='candle',style='yahoo',addplot=[a,b])

#macd
# stochastic osc
# rsi
# adx

#plotly
#tradingview chart


# import pandas as pd
# from lightweight_charts import Chart



# def calculate_sma(df, period: int = 50):
#     return pd.DataFrame({
#         'time': df['Datetime'],
#         f'SMA {period}': df['Close'].rolling(window=period).mean()
#     }).dropna()



# chart = Chart()
# chart.legend(visible=True)

# df = data
# chart.set(df)

# line = chart.create_line('SMA 50')
# sma_data = calculate_sma(df.reset_index(), period=50)
# line.set(sma_data)

# chart.show(block=True)