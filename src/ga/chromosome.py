"""Kromozom yapisi ve gen tanimlari."""
from dataclasses import dataclass
from deap import base, creator, tools
import random

# Gen sinirlari: (min, max) - int ise int, float ise float
GENE_BOUNDS = [
    (7, 30),        # rsi_period (int)
    (20.0, 40.0),   # rsi_oversold (float)
    (60.0, 80.0),   # rsi_overbought (float)
    (8, 16),        # macd_fast (int)
    (20, 30),       # macd_slow (int)
    (5, 12),        # macd_signal (int)
    (15, 30),       # bb_period (int)
    (1.5, 3.0),     # bb_std (float)
    (5, 20),        # sma_short (int)
    (30, 100),      # sma_long (int)
    (0.01, 0.10),   # stop_loss (float)
    (0.02, 0.20),   # take_profit (float)
    (0.0, 1.0),     # weight_rsi (float)
    (0.0, 1.0),     # weight_macd (float)
    (0.0, 1.0),     # weight_bb (float)
    (0.0, 1.0),     # weight_sma (float)
]

GENE_NAMES = [
    "rsi_period", "rsi_oversold", "rsi_overbought",
    "macd_fast", "macd_slow", "macd_signal",
    "bb_period", "bb_std",
    "sma_short", "sma_long",
    "stop_loss", "take_profit",
    "weight_rsi", "weight_macd", "weight_bb", "weight_sma",
]


@dataclass
class StrategyParams:
    """GA kromozomundan cozulen strateji parametreleri."""
    rsi_period: int
    rsi_oversold: float
    rsi_overbought: float
    macd_fast: int
    macd_slow: int
    macd_signal: int
    bb_period: int
    bb_std: float
    sma_short: int
    sma_long: int
    stop_loss: float
    take_profit: float
    weight_rsi: float
    weight_macd: float
    weight_bb: float
    weight_sma: float


def create_individual():
    """Rastgele bir birey olusturur."""
    individual = []
    for low, high in GENE_BOUNDS:
        if isinstance(low, int) and isinstance(high, int):
            individual.append(random.randint(low, high))
        else:
            individual.append(random.uniform(low, high))
    return individual


def decode_chromosome(individual) -> StrategyParams:
    """Kromozomu StrategyParams dataclass'ina donusturur."""
    values = {}
    for i, name in enumerate(GENE_NAMES):
        low, high = GENE_BOUNDS[i]
        if isinstance(low, int) and isinstance(high, int):
            values[name] = int(round(individual[i]))
        else:
            values[name] = individual[i]
    return StrategyParams(**values)


def repair_individual(individual):
    """Kisitlamalari ihlal eden genleri duzeltir."""
    # macd_fast < macd_slow olmali
    if individual[3] >= individual[4]:
        individual[3], individual[4] = min(individual[3], individual[4]), max(individual[3], individual[4])

    # sma_short < sma_long olmali
    if individual[8] >= individual[9]:
        individual[8], individual[9] = min(individual[8], individual[9]), max(individual[8], individual[9])

    # rsi_oversold < rsi_overbought olmali
    if individual[1] >= individual[2]:
        individual[1], individual[2] = min(individual[1], individual[2]), max(individual[1], individual[2])

    # Gen sinirlarini kontrol et
    for i, (low, high) in enumerate(GENE_BOUNDS):
        individual[i] = max(low, min(high, individual[i]))
        if isinstance(low, int) and isinstance(high, int):
            individual[i] = int(round(individual[i]))

    return individual
