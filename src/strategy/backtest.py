"""
Vektorel backtest modulu -- GA tabanli BTC trading botu icin.

GA'nin fitness fonksiyonunda her nesilde binlerce kez cagrilmasi icin
optimize edilmistir:
  - Tamamen vektorel islemler (for dongusu / df.apply() YOK)
  - Look-ahead bias (veri sizintisi) YOK -- pozisyon shift(1) ile kaydiriliyor
  - Komisyon + slippage yalnizca islem anlarinda uygulaniyor

Akis:
  Sinyal --> Pozisyon (long-only, ffill) --> shift(1) --> Getiri --> Maliyet
  --> Equity Curve --> Metrikler (Total Return, Sharpe, MaxDD, Win Rate)
"""
import pandas as pd
import numpy as np


# ═══════════════════════════════════════════════════════════════════════════════
# YARDIMCI: NUMPY FFILL (pandas-free, vektorel)
# ═══════════════════════════════════════════════════════════════════════════════


def _ffill_numpy(arr: np.ndarray, fill_value: float = 0.0) -> np.ndarray:
    """
    NaN degerlerini bir onceki gecerli degerle doldurur (forward-fill).
    Pandas kullanmadan tamamen numpy ile O(n) karmasiklik.

    Args:
        arr: NaN icermesi muhtemel 1-D numpy dizisi.
        fill_value: Dizinin basindaki NaN'lar icin dolgu degeri.

    Returns:
        NaN'lar giderilmis dizi.
    """
    mask = np.isnan(arr)
    if not mask.any():
        return arr.copy()

    # NaN olmayan indeksleri isle, NaN olan yerlerde onceki gecerli indeksi tasi
    idx = np.where(~mask, np.arange(len(arr)), 0)
    np.maximum.accumulate(idx, out=idx)
    result = arr[idx]

    # Baslangictaki NaN'lari fill_value ile doldur (ilk gecerli degerden once)
    first_valid = np.argmax(~mask)
    if first_valid > 0:
        result[:first_valid] = fill_value

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# ANA BACKTEST FONKSIYONU (DataFrame arayuzu)
# ═══════════════════════════════════════════════════════════════════════════════


def run_backtest(
    df: pd.DataFrame,
    signal_col: str = "Composite_Signal",
    initial_capital: float = 10_000.0,
    position_size: float = 0.95,
    commission_rate: float = 0.001,
    slippage_rate: float = 0.0005,
) -> dict:
    """
    Long-only vektorel backtest -- sinyal sutunundan performans metrikleri uretir.

    Islem mantigi:
        1 (AL)  -->  pozisyona gir  (position = 1)
       -1 (SAT) -->  pozisyondan cik (position = 0)
        0 (NOTR) --> onceki pozisyonu koru (ffill)

    Kritik: Pozisyon shift(1) ile bir gun sonraya kaydirilir.
    Bu, sinyal gununde islem verilemeyecegini modelleyerek look-ahead bias'i onler.

    Args:
        df: En az 'Close' ve sinyal sutununu iceren DataFrame.
        signal_col: Sinyal sutununun adi (default: 'Composite_Signal').
        initial_capital: Baslangic sermayesi ($). Default: 10,000.
        position_size: Sermayenin kac katiyia pozisyon acilacagi. Default: 0.95.
        commission_rate: Islem basi komisyon orani. Default: 0.001 (%0.1).
        slippage_rate: Islem basi kayma orani. Default: 0.0005 (%0.05).

    Returns:
        Asagidaki anahtarlari iceren dictionary:
            total_return   (float): Toplam getiri yuzdesi (%).
            sharpe_ratio   (float): Yilliklandirilmis Sharpe orani (365 gun, rf=0).
            max_drawdown   (float): Zirveden en buyuk dusus yuzdesi (negatif %).
            win_rate       (float): Karli islemlerin orani (%).
            total_trades   (int)  : Tamamlanan islem sayisi.
            equity_curve   (pd.Series): Gunluk sermaye degeri.
            buy_and_hold   (pd.Series): Karsilastirma icin buy-and-hold equity.

    Raises:
        ValueError: Gerekli sutunlar eksikse.
    """
    # ── Girdi dogrulama ──────────────────────────────────────────
    if "Close" not in df.columns:
        raise ValueError("DataFrame'de 'Close' sutunu bulunamadi.")
    if signal_col not in df.columns:
        raise ValueError(f"DataFrame'de '{signal_col}' sinyal sutunu bulunamadi.")

    close = df["Close"].values.astype(np.float64)
    signals = df[signal_col].values.astype(np.float64)

    # ── Hesapla ──────────────────────────────────────────────────
    result = _backtest_core(
        close=close,
        signals=signals,
        initial_capital=initial_capital,
        position_size=position_size,
        commission_rate=commission_rate,
        slippage_rate=slippage_rate,
    )

    # Equity curve'u pandas Series olarak sar (gorsellesitirme icin)
    result["equity_curve"] = pd.Series(
        result["equity_curve"], index=df.index, name="Equity"
    )
    result["buy_and_hold"] = pd.Series(
        result["buy_and_hold"], index=df.index, name="Buy_and_Hold"
    )

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# HIZLI BACKTEST FONKSIYONU (numpy arayuzu -- GA fitness icin)
# ═══════════════════════════════════════════════════════════════════════════════


def run_backtest_fast(
    close: np.ndarray,
    signals: np.ndarray,
    initial_capital: float = 10_000.0,
    position_size: float = 0.95,
    commission_rate: float = 0.001,
    slippage_rate: float = 0.0005,
) -> dict:
    """
    Yuksek performansli backtest -- sadece numpy, DataFrame overhead'i yok.

    GA fitness fonksiyonunun her cagrisinda kullanilmak uzere tasarlandi.
    run_backtest() ile ayni mantigi kullanir. equity_curve ve buy_and_hold
    numpy dizisi olarak dondurulur.

    Args:
        close: Kapanis fiyatlarinin numpy dizisi (1-D float64).
        signals: Sinyal dizisi (+1, -1, 0) (1-D).
        initial_capital: Baslangic sermayesi ($).
        position_size: Pozisyon buyuklugu orani.
        commission_rate: Komisyon orani.
        slippage_rate: Kayma orani.

    Returns:
        run_backtest() ile ayni anahtarlari iceren dictionary.
        equity_curve ve buy_and_hold np.ndarray olarak dondurulur.
    """
    return _backtest_core(
        close=np.asarray(close, dtype=np.float64),
        signals=np.asarray(signals, dtype=np.float64),
        initial_capital=initial_capital,
        position_size=position_size,
        commission_rate=commission_rate,
        slippage_rate=slippage_rate,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CEKIRDEK HESAPLAMA MOTORU (tamamen numpy, her iki arayuz tarafindan paylasilir)
# ═══════════════════════════════════════════════════════════════════════════════


def _backtest_core(
    close: np.ndarray,
    signals: np.ndarray,
    initial_capital: float,
    position_size: float,
    commission_rate: float,
    slippage_rate: float,
) -> dict:
    """
    Tum backtest hesaplamasini vektorel olarak gerceklestirir.

    FOR DONGUSU VE DF.APPLY() KULLANILMAZ.
    """
    n = len(close)

    # ──────────────────────────────────────────────────────────────
    # 1. POZISYON HESAPLAMA (Long-only)
    # ──────────────────────────────────────────────────────────────
    #   signal =  1 --> pozisyona gir  (position = 1)
    #   signal = -1 --> pozisyondan cik (position = 0)
    #   signal =  0 --> onceki durumu koru (ffill)

    raw_position = np.where(
        signals == 1, 1.0,
        np.where(signals == -1, 0.0, np.nan)
    )

    # NaN degerleri onceki gecerli pozisyonla doldur (ffill)
    # Baslangicta pozisyon yok (0)
    raw_position = _ffill_numpy(raw_position, fill_value=0.0)

    # ──────────────────────────────────────────────────────────────
    # 2. LOOK-AHEAD BIAS ONLEME -- shift(1)
    # ──────────────────────────────────────────────────────────────
    # Bugunun sinyali yarin uygulanir: bugun karar ver, yarin isle.
    # position[t] = raw_position[t-1]

    position = np.empty(n, dtype=np.float64)
    position[0] = 0.0             # ilk gun: pozisyon yok
    position[1:] = raw_position[:-1]  # shift(1)

    # ──────────────────────────────────────────────────────────────
    # 3. GUNLUK GETIRI
    # ──────────────────────────────────────────────────────────────

    daily_return = np.empty(n, dtype=np.float64)
    daily_return[0] = 0.0
    daily_return[1:] = (close[1:] - close[:-1]) / close[:-1]

    # ──────────────────────────────────────────────────────────────
    # 4. STRATEJI GETIRISI (maliyet oncesi)
    # ──────────────────────────────────────────────────────────────
    # Sermayenin position_size kadari pozisyonda, gerisi nakit (getiri=0)

    strategy_return = position * daily_return * position_size

    # ──────────────────────────────────────────────────────────────
    # 5. ISLEM MALIYETLERI (sadece giris/cikis anlarinda)
    # ──────────────────────────────────────────────────────────────
    # position_change = position.diff()
    #   +1 --> pozisyona giris (ALIS)
    #   -1 --> pozisyondan cikis (SATIS)
    #    0 --> degisiklik yok

    position_change = np.empty(n, dtype=np.float64)
    position_change[0] = position[0]       # ilk gun: 0'dan position[0]'a
    position_change[1:] = position[1:] - position[:-1]

    # Maliyet = |degisim| * (komisyon + kayma) * pozisyon_buyuklugu
    trade_cost_per_bar = (
        np.abs(position_change) * (commission_rate + slippage_rate) * position_size
    )

    # ──────────────────────────────────────────────────────────────
    # 6. NET GETIRI VE EQUITY CURVE
    # ──────────────────────────────────────────────────────────────

    net_return = strategy_return - trade_cost_per_bar
    equity = initial_capital * np.cumprod(1.0 + net_return)

    # ──────────────────────────────────────────────────────────────
    # 7. BUY-AND-HOLD KARSILASTIRMA
    # ──────────────────────────────────────────────────────────────

    bh_return = np.empty(n, dtype=np.float64)
    bh_return[0] = 0.0
    bh_return[1:] = daily_return[1:] * position_size
    buy_and_hold = initial_capital * np.cumprod(1.0 + bh_return)
    # ══════════════════════════════════════════════════════════════
    # 8. PERFORMANS METRIKLERI
    # ══════════════════════════════════════════════════════════════

    # ── 8.1 Total Return (%) ─────────────────────────────────
    final_equity = equity[-1]
    total_return = (
        (final_equity / initial_capital - 1.0) * 100.0
        if np.isfinite(final_equity)
        else 0.0
    )

    # ── 8.2 Sharpe Ratio (yilliklandirilmis, 365 gun, rf=0) ─────
    # NaN ve sifir varyans durumlarina karsi koruma
    finite_returns = net_return[np.isfinite(net_return)]
    if len(finite_returns) > 1:
        mean_ret = np.mean(finite_returns)
        std_ret = np.std(finite_returns, ddof=1)
        sharpe_ratio = (
            (mean_ret / std_ret) * np.sqrt(365.0)
            if std_ret > 1e-12
            else 0.0
        )
    else:
        sharpe_ratio = 0.0

    # ── 8.3 Maximum Drawdown (%) ─────────────────────────────────
    # NaN iceren equity degerlerini koruma
    valid_equity = np.where(np.isfinite(equity), equity, initial_capital)
    peak = np.maximum.accumulate(valid_equity)
    drawdown = np.where(peak > 0, (valid_equity - peak) / peak, 0.0)
    max_drawdown = float(np.min(drawdown)) * 100.0   # negatif %

    # ── 8.4 Win Rate (%) ─────────────────────────────────────────
    # Islem bazli kar/zarar: giris ve cikis fiyatlarini diff() ile tespit et
    #
    # raw_position uzerinde diff():
    #   +1 --> giris (AL)
    #   -1 --> cikis (SAT)
    raw_change = np.empty(n, dtype=np.float64)
    raw_change[0] = raw_position[0]
    raw_change[1:] = raw_position[1:] - raw_position[:-1]

    entry_mask = raw_change == 1.0    # giris noktalari
    exit_mask = raw_change == -1.0    # cikis noktalari

    entry_prices = close[entry_mask]
    exit_prices = close[exit_mask]

    # Sadece tamamlanan islemleri say (son acik pozisyon haric)
    n_trades = min(len(entry_prices), len(exit_prices))

    if n_trades > 0:
        ep = entry_prices[:n_trades]
        xp = exit_prices[:n_trades]
        # Maliyet dahil net kar: cikis*(1-maliyet) - giris*(1+maliyet)
        total_cost = commission_rate + slippage_rate
        net_profit = xp * (1.0 - total_cost) - ep * (1.0 + total_cost)
        win_rate = float(np.sum(net_profit > 0)) / n_trades * 100.0
    else:
        win_rate = 0.0

    # ──────────────────────────────────────────────────────────────

    return {
        "total_return": round(float(total_return), 4),
        "sharpe_ratio": round(float(sharpe_ratio), 4),
        "max_drawdown": round(float(max_drawdown), 4),
        "win_rate": round(float(win_rate), 2),
        "total_trades": int(n_trades),
        "equity_curve": equity,        # np.ndarray (veya pd.Series wraplenir)
        "buy_and_hold": buy_and_hold,  # np.ndarray (veya pd.Series wraplenir)
    }
