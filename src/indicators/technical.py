"""Teknik indikatör hesaplama modulu."""
import pandas as pd
import pandas_ta as ta


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Tum teknik indikatorleri hesaplar ve DataFrame'e ekler."""
    df = df.copy()

    # Trend
    df["SMA_20"] = ta.sma(df["Close"], length=20)
    df["SMA_50"] = ta.sma(df["Close"], length=50)
    df["EMA_12"] = ta.ema(df["Close"], length=12)
    df["EMA_26"] = ta.ema(df["Close"], length=26)
    macd = ta.macd(df["Close"], fast=12, slow=26, signal=9)
    df = pd.concat([df, macd], axis=1)

    # Momentum
    df["RSI_14"] = ta.rsi(df["Close"], length=14)
    stoch = ta.stoch(df["High"], df["Low"], df["Close"])
    df = pd.concat([df, stoch], axis=1)

    # Volatilite
    bbands = ta.bbands(df["Close"], length=20, std=2)
    df = pd.concat([df, bbands], axis=1)
    df["ATR_14"] = ta.atr(df["High"], df["Low"], df["Close"], length=14)

    # Hacim
    df["OBV"] = ta.obv(df["Close"], df["Volume"])

    return df
