# Genetik Algoritmalar ile Bitcoin Trading Stratejisi Optimizasyonu

Ege Universitesi - Bilgisayar Muhendisligi Bolumu
Yapay Zeka Yontemleri (3+0) - 2025-2026 Bahar Donemi - Proje 2

## Takim

| Uye | Rol |
|-----|-----|
| Mert | Genetik Algoritma Cekirdek Gelistirme |
| Yigit | Veri Toplama, On Isleme & Feature Engineering |
| Mert Kerem | Trading Stratejisi & Backtesting |
| Gorkem Ege | Deneysel Calismalar & Rapor/Dokumantasyon |

## Proje Ozeti

Bu projede Genetik Algoritmalar (GA) kullanilarak Bitcoin (BTC) trading stratejilerinin parametreleri optimize edilmektedir. Sistem, tarihsel BTC fiyat verilerinden teknik indikatorler cikararak, GA ile en uygun trading parametrelerini (RSI/MACD/BB esikleri, stop-loss/take-profit seviyeleri, indikatör agirliklari) bulmaktadir.

## Kurulum

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Proje Yapisi

```
├── config/
│   ├── config.py              # Proje konfigurasyonlari (DataClass)
│   └── config.yaml            # GA ve strateji parametreleri
├── src/
│   ├── data/
│   │   ├── collector.py       # BTC veri toplama (yfinance)
│   │   └── preprocessor.py    # Veri temizleme, train/test ayirimi
│   ├── indicators/
│   │   └── technical.py       # Teknik indikatorler (RSI, MACD, BB, vb.)
│   ├── ga/
│   │   └── chromosome.py      # Kromozom yapisi, gen tanimlari, tamir fonk.
│   ├── strategy/              # Trading sinyalleri ve backtesting
│   └── visualization/         # Grafik ve gorsellesitirme
├── data/
│   ├── raw/                   # Ham BTC verisi
│   └── processed/             # Islenmis veri
├── docs/
│   ├── AIM_2026_ENG.doc       # Proje gereksinimleri
│   ├── Project 2 Report Template - EN.docx
│   ├── Literature_Review.docx # Literatur taramasi (11 kaynak)
│   ├── teknoloji_secim_raporu.md
│   └── Proje_On_Analiz_Raporu.md
├── results/
│   ├── figures/               # Cikti grafikleri
│   ├── tables/                # Sonuc tablolari
│   └── logs/                  # GA calisma loglari
├── notebooks/                 # Jupyter notebook'lar
├── tests/                     # Birim testleri
├── fazlar/                    # Proje faz planlama dokumanlari
├── ROADMAP.md                 # Proje yol haritasi
└── requirements.txt           # Python bagimliliklari
```

## Kullanim

```bash
# 1. Veri toplama
python -m src.data.collector

# 2. GA calistirma (Faz 3-4 sonrasi)
python main.py
```

## Teknolojiler

- **Python 3.10+**
- **DEAP** - Genetik Algoritma
- **pandas-ta** - Teknik indikatorler
- **yfinance** - BTC veri toplama
- **matplotlib / plotly** - Gorsellesitirme
