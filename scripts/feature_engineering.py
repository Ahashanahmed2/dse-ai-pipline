import ta

def generate_indicators(df):
    df = df.copy()
    
    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    
    # MACD
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_width'] = bb.bollinger_wband()

    # OBV
    df['obv'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()

    # ATR
    df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()

    # Doji & Engulfing
    df['doji'] = ((abs(df['open'] - df['close']) / (df['high'] - df['low'])).fillna(0) < 0.1).astype(int)
    df['engulfing'] = (
        (df['close'] > df['open'].shift(1)) &
        (df['open'] < df['close'].shift(1))
    ).astype(int)

    # VWAP
    df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()

    return df