"""
backtest.py modul dogrulama scripti.

Sentetik BTC verisi ile run_backtest ve run_backtest_fast fonksiyonlarinin
dogrulugunu, look-ahead bias'sizligini ve performansini test eder.
"""
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np

from src.ga.chromosome import StrategyParams
from src.strategy.signals import generate_signals, generate_signals_fast
from src.strategy.backtest import run_backtest, run_backtest_fast


# =====================================================================
# SENTETIK BTC VERISI
# =====================================================================

np.random.seed(42)
n = 500
dates = pd.date_range("2022-01-01", periods=n, freq="D")
# Gercekci BTC-benzeri fiyat hareketi
returns = np.random.randn(n) * 0.03  # gunluk %3 volatilite
close = 25000.0 * np.exp(np.cumsum(returns))
high = close * (1 + np.abs(np.random.randn(n) * 0.01))
low = close * (1 - np.abs(np.random.randn(n) * 0.01))
open_ = close * (1 + np.random.randn(n) * 0.005)
volume = np.random.randint(1_000_000, 50_000_000, size=n).astype(float)

df = pd.DataFrame({
    "Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume
}, index=dates)

# GA parametreleri
params = StrategyParams(
    rsi_period=14, rsi_oversold=30.0, rsi_overbought=70.0,
    macd_fast=12, macd_slow=26, macd_signal=9,
    bb_period=20, bb_std=2.0,
    sma_short=10, sma_long=50,
    stop_loss=0.05, take_profit=0.10,
    weight_rsi=0.3, weight_macd=0.3, weight_bb=0.2, weight_sma=0.2,
)

# Sinyal uret
df_sig = generate_signals(df, params)

print("=" * 60)
print("BACKTEST MODUL DOGRULAMA TESTLERI")
print("=" * 60)


# =====================================================================
# TEST 1: Cikti anahtarlari ve tipleri
# =====================================================================

print("\nTEST 1: Cikti yapisini dogrula")
print("-" * 40)

result = run_backtest(df_sig)

expected_keys = [
    "total_return", "sharpe_ratio", "max_drawdown",
    "win_rate", "total_trades", "equity_curve", "buy_and_hold"
]
for key in expected_keys:
    assert key in result, f"HATA: '{key}' anahtari eksik!"
    print(f"  [OK] {key}: {type(result[key]).__name__}", end="")
    if key not in ("equity_curve", "buy_and_hold"):
        print(f" = {result[key]}")
    else:
        print(f" (len={len(result[key])})")

assert isinstance(result["equity_curve"], pd.Series), "equity_curve pd.Series olmali!"
assert isinstance(result["buy_and_hold"], pd.Series), "buy_and_hold pd.Series olmali!"
assert len(result["equity_curve"]) == len(df_sig), "equity_curve uzunlugu uyumsuz!"
print("  [OK] Tum cikti kontroleri gecti.")


# =====================================================================
# TEST 2: Sinyal degerleri ve mantik
# =====================================================================

print("\nTEST 2: Mantiksal tutarlilik kontrolleri")
print("-" * 40)

# Equity curve baslangic sermayesiyle baslamali
assert abs(result["equity_curve"].iloc[0] - 10000.0) < 1.0, \
    f"HATA: Equity baslangicci 10000 olmali, bulundu: {result['equity_curve'].iloc[0]}"
print("  [OK] Equity curve $10,000 ile basliyor.")

# Max drawdown negatif olmali (veya sifir)
assert result["max_drawdown"] <= 0.0, \
    f"HATA: Max drawdown negatif olmali, bulundu: {result['max_drawdown']}"
print(f"  [OK] Max drawdown: {result['max_drawdown']:.2f}%")

# Win rate 0-100 arasinda olmali
assert 0.0 <= result["win_rate"] <= 100.0, \
    f"HATA: Win rate 0-100 arasinda olmali, bulundu: {result['win_rate']}"
print(f"  [OK] Win rate: {result['win_rate']:.2f}% ({result['total_trades']} islem)")

# Sharpe ratio makul aralikta olmali
assert -10.0 < result["sharpe_ratio"] < 10.0, \
    f"HATA: Sharpe ratio asiri deger: {result['sharpe_ratio']}"
print(f"  [OK] Sharpe ratio: {result['sharpe_ratio']:.4f}")

print(f"  [OK] Total return: {result['total_return']:.2f}%")


# =====================================================================
# TEST 3: Look-ahead bias kontrolu
# =====================================================================

print("\nTEST 3: Look-ahead bias (veri sizintisi) kontrolu")
print("-" * 40)

# Veriyi yariya kes ve backtest yap
half = n // 2
df_half = df_sig.iloc[:half].copy()
result_half = run_backtest(df_half)

# Tam veri ile yarinin equity curve'u birebir ayni olmali
full_eq = result["equity_curve"].values[:half]
half_eq = result_half["equity_curve"].values

# Kucuk floating-point farklarini tolere et
max_diff = np.max(np.abs(full_eq - half_eq))
assert max_diff < 1e-6, \
    f"HATA: Look-ahead bias tespit edildi! Maks fark: {max_diff:.10f}"
print(f"  [OK] Equity farki (tam vs yari): {max_diff:.2e} (< 1e-6)")
print("  [OK] Gelecek veriye bagimllik yok.")


# =====================================================================
# TEST 4: run_backtest vs run_backtest_fast tutarliligi
# =====================================================================

print("\nTEST 4: DataFrame vs numpy arayuz tutarliligi")
print("-" * 40)

signals_np = df_sig["Composite_Signal"].values.astype(np.float64)
result_fast = run_backtest_fast(close, signals_np)

# 4 ana metrik ayni olmali
for key in ["total_return", "sharpe_ratio", "max_drawdown", "win_rate", "total_trades"]:
    val_full = result[key]
    val_fast = result_fast[key]
    if isinstance(val_full, float):
        assert abs(val_full - val_fast) < 0.01, \
            f"HATA: {key} uyumsuz: {val_full} vs {val_fast}"
    else:
        assert val_full == val_fast, \
            f"HATA: {key} uyumsuz: {val_full} vs {val_fast}"
    print(f"  [OK] {key:20s}: full={val_full}, fast={val_fast}")

# Equity curve ayni olmali
eq_full = result["equity_curve"].values
eq_fast = result_fast["equity_curve"]
max_eq_diff = np.max(np.abs(eq_full - eq_fast))
assert max_eq_diff < 1e-6, f"HATA: Equity curve farki: {max_eq_diff}"
print(f"  [OK] Equity curve max fark: {max_eq_diff:.2e}")


# =====================================================================
# TEST 5: Komisyon etkisi
# =====================================================================

print("\nTEST 5: Komisyon ve slippage etkisi")
print("-" * 40)

result_no_cost = run_backtest(df_sig, commission_rate=0.0, slippage_rate=0.0)
result_with_cost = run_backtest(df_sig, commission_rate=0.001, slippage_rate=0.0005)

# Maliyetli getiri, maliyetsizden dusuk olmali (islem yapildiysa)
if result_with_cost["total_trades"] > 0:
    assert result_with_cost["total_return"] <= result_no_cost["total_return"], \
        "HATA: Maliyet dahil getiri maliyetsizden buyuk olamaz!"
    cost_impact = result_no_cost["total_return"] - result_with_cost["total_return"]
    print(f"  [OK] Maliyetsiz getiri:   {result_no_cost['total_return']:.2f}%")
    print(f"  [OK] Maliyetli getiri:    {result_with_cost['total_return']:.2f}%")
    print(f"  [OK] Maliyet etkisi:      {cost_impact:.2f} puan")
else:
    print("  [UYARI] Hic islem yapilmadi, maliyet etkisi test edilemiyor.")


# =====================================================================
# TEST 6: Kenar durumlari (edge cases)
# =====================================================================

print("\nTEST 6: Kenar durumlari")
print("-" * 40)

# 6a: Tamamen notr sinyal (hic islem yok)
df_neutral = df.copy()
df_neutral["Composite_Signal"] = 0
result_neutral = run_backtest(df_neutral)
assert result_neutral["total_return"] == 0.0, "HATA: Sinyalsiz getiri 0 olmali!"
assert result_neutral["total_trades"] == 0, "HATA: Sinyalsiz islem 0 olmali!"
print("  [OK] Tamamen notr: return=0%, trades=0")

# 6b: Tamamen AL sinyali (hep pozisyonda)
df_all_buy = df.copy()
df_all_buy["Composite_Signal"] = 1
result_all_buy = run_backtest(df_all_buy)
assert result_all_buy["total_trades"] >= 0, "HATA: Negatif islem sayisi!"
print(f"  [OK] Tamamen AL: return={result_all_buy['total_return']:.2f}%, "
      f"trades={result_all_buy['total_trades']}")

# 6c: Alternatif AL/SAT sinyali (cok fazla islem)
df_alternate = df.copy()
alternating = np.tile([1, -1], n // 2 + 1)[:n]
df_alternate["Composite_Signal"] = alternating
result_alt = run_backtest(df_alternate)
print(f"  [OK] Alternatif: return={result_alt['total_return']:.2f}%, "
      f"trades={result_alt['total_trades']} (yuksek maliyet beklenir)")


# =====================================================================
# TEST 7: Performans (hiz) testi
# =====================================================================

print("\nTEST 7: Performans testi")
print("-" * 40)

iterations = 2000

# run_backtest_fast zamanlama
start = time.perf_counter()
for _ in range(iterations):
    _ = run_backtest_fast(close, signals_np)
elapsed_fast = time.perf_counter() - start

print(f"  run_backtest_fast: {iterations} cagri --> {elapsed_fast:.2f}s "
      f"(ortalama {elapsed_fast/iterations*1000:.3f}ms/cagri)")

# run_backtest zamanlama
start = time.perf_counter()
for _ in range(iterations):
    _ = run_backtest(df_sig)
elapsed_full = time.perf_counter() - start

print(f"  run_backtest:      {iterations} cagri --> {elapsed_full:.2f}s "
      f"(ortalama {elapsed_full/iterations*1000:.3f}ms/cagri)")

print(f"  Hiz kazanimi (fast): {elapsed_full/elapsed_fast:.1f}x")


# =====================================================================
# TEST 8: Uçtan uca entegrasyon (signals + backtest)
# =====================================================================

print("\nTEST 8: Uctan uca entegrasyon (signals --> backtest)")
print("-" * 40)

# signals_fast + backtest_fast = tam GA fitness pipeline
start = time.perf_counter()
for _ in range(iterations):
    sigs = generate_signals_fast(close, params)
    _ = run_backtest_fast(close, sigs)
elapsed_pipeline = time.perf_counter() - start

print(f"  Tam pipeline (sinyal+backtest): {iterations} cagri --> {elapsed_pipeline:.2f}s "
      f"(ortalama {elapsed_pipeline/iterations*1000:.3f}ms/cagri)")

# GA icin tahmin: 100 pop * 50 nesil = 5000 fitness cagri
est_ga = 5000 * (elapsed_pipeline / iterations)
print(f"  Tahmini GA suresi (100pop x 50gen): {est_ga:.1f}s ({est_ga/60:.1f}dk)")


# =====================================================================
# SONUC
# =====================================================================

print("\n" + "=" * 60)
print("[BASARILI] Tum dogrulama testleri gecti!")
print("=" * 60)
