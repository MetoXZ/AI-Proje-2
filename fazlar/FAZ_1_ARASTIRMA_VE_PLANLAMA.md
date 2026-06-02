# Faz 1: Arastirma ve Planlama

**Sure:** Gun 1 - Sabah (31 Mayis Cumartesi)
**Tarih:** 31 Mayis 2026
**Durum:** Kismen Tamamlandi (Mert kapsami tamamlandi)
**Sorumlu:** Tum Takim

---

## Hedef

Proje konusunu derinlemesine arastirmak, literatur taramasi yapmak, kullanilacak yontem ve araclari belirlemek, gelistirme ortamini kurmak ve projenin teknik altyapisini planlamak.

---

## Gorevler

### 1.1 Literatur Taramasi
**Sorumlu:** Gorkem Ege & Mert
**Sure:** 2 saat (09:00-11:00)

- [x] Genetik Algoritmalar (GA) hakkinda temel kaynaklarin incelenmesi
  - Holland'in "Adaptation in Natural and Artificial Systems" kitabi
  - Goldberg'in GA uzerine klasik calismalari
  - GA'nin temel kavramlari: populasyon, kromozom, gen, fitness, secim, caprazlama, mutasyon
- [x] GA ile finansal tahmin/trading uzerine akademik makalelerin taranmasi
  - Google Scholar'da "genetic algorithm trading strategy optimization" aramalari
  - "Genetic algorithm Bitcoin prediction" konulu makaleler
  - Hocanin BTC fiyat tahmini makalesi (varsa referans alinmasi)
- [x] Benzer projelerin ve acik kaynak kodlarin incelenmesi
  - GitHub'da "genetic algorithm trading" repolari
  - Kaggle'da ilgili notebook'lar
- [x] En az 10 kaynak belirlenmesi ve ozetlerinin cikarilmasi
- [x] Incelenen kaynaklarin linkleri ve ogrenilen bilgilerin dokumante edilmesi

**Tamamlanma notu (Mert & Gorkem Ege):** Literatur taramasi `docs/Literature_Review.docx` dosyasinda 11 kaynak ve ozetleriyle dokumante edildi.

### 1.2 Teknik Altyapi Arastirmasi
**Sorumlu:** Yigit & Mert Kerem
**Sure:** 1 saat (09:00-10:00, Literatur ile paralel)

- [ ] Python kutuphanelerinin arastirilmasi ve karsilastirilmasi:
  - **DEAP** (Distributed Evolutionary Algorithms in Python) - GA implementasyonu icin
  - **pandas-ta** vs **TA-Lib** - Teknik indikatörler icin
  - **backtrader** vs ozel backtesting - Strateji test icin
  - **yfinance** vs **ccxt** - Veri toplama icin
- [ ] BTC tarihsel veri kaynaklarinin belirlenmesi:
  - Yahoo Finance (yfinance)
  - Binance API
  - CoinGecko API
  - Kaggle BTC veri setleri
- [ ] Veri granularitesinin belirlenmesi (gunluk / saatlik / 4 saatlik)
- [ ] Veri zaman araliginin belirlenmesi (orn: 2018-2025)

### 1.3 Gelistirme Ortaminin Kurulumu
**Sorumlu:** Yigit
**Sure:** 1 saat (10:00-11:00)

- [ ] Python 3.10+ kurulumu ve sanal ortam (venv) olusturma
- [ ] `requirements.txt` dosyasinin hazirlanmasi:
  ```
  numpy>=1.24.0
  pandas>=2.0.0
  deap>=1.4.0
  yfinance>=0.2.0
  matplotlib>=3.7.0
  plotly>=5.15.0
  seaborn>=0.12.0
  scikit-learn>=1.3.0
  ```
- [ ] GitHub reposunun olusturulmasi
  - `.gitignore` dosyasi (Python template)
  - `README.md` dosyasi
  - Proje klasor yapisi
- [ ] Jupyter Notebook ortaminin hazirlanmasi (kesfetme/prototip icin)

### 1.4 Proje Yapisinin Belirlenmesi
**Sorumlu:** Mert & Mert Kerem
**Sure:** 1 saat (11:00-12:00)

- [ ] Proje dizin yapisinin tasarlanmasi:
  ```
  btc-ga-trading/
  ├── README.md
  ├── requirements.txt
  ├── config/
  │   └── config.py            # Proje konfigurasyonlari
  ├── data/
  │   ├── raw/                 # Ham veri
  │   └── processed/           # Islenmis veri
  ├── src/
  │   ├── __init__.py
  │   ├── data/
  │   │   ├── __init__.py
  │   │   ├── collector.py     # Veri toplama
  │   │   └── preprocessor.py  # Veri on isleme
  │   ├── indicators/
  │   │   ├── __init__.py
  │   │   └── technical.py     # Teknik indikatörler
  │   ├── ga/
  │   │   ├── __init__.py
  │   │   ├── chromosome.py    # Kromozom yapisi
  │   │   ├── fitness.py       # Fitness fonksiyonu
  │   │   ├── operators.py     # GA operatörleri
  │   │   └── engine.py        # GA motoru
  │   ├── strategy/
  │   │   ├── __init__.py
  │   │   ├── signals.py       # Trading sinyalleri
  │   │   └── backtest.py      # Backtesting
  │   └── visualization/
  │       ├── __init__.py
  │       └── plots.py         # Gorsellesitirme
  ├── notebooks/
  │   └── exploration.ipynb    # Kesfetme notebook'u
  ├── results/
  │   ├── figures/             # Grafikler
  │   └── tables/              # Sonuc tablolari
  ├── reports/
  │   └── report.docx          # Proje raporu
  └── tests/
      └── test_ga.py           # Birim testleri
  ```
- [ ] Modüller arasi arayuzlerin (interface) tanimlanmasi
- [ ] Konfigurasyon dosyasinin sablonunun hazirlanmasi

### 1.5 GA Tasarim Kararlari
**Sorumlu:** Mert
**Sure:** 1 saat (11:00-12:00, Proje yapisi ile paralel)

- [x] Kromozom temsil yapisinin on tasarimi:
  - Hangi parametreler optimize edilecek?
  - Her genin veri tipi ve aralik degerleri
  - Kromozom uzunlugu
- [x] Fitness fonksiyonu icin metrik seceneklerinin belirlenmesi:
  - Toplam kar/zarar
  - Sharpe Orani
  - Maximum Drawdown
  - Win Rate
  - Kar Faktoru (Profit Factor)
- [x] GA operatörlerinin on secimi:
  - Secim: Turnuva, Rulet Tekerlegi, Elitizm
  - Caprazlama: Tek/Cift nokta, Uniform
  - Mutasyon: Gaussian, Uniform, Bit-flip

**Tamamlanma notu (Mert):** 16 genlik kromozom, Sharpe/return/drawdown odakli fitness ve turnuva-elitizm-BLX/Gaussian/Uniform operator kararlari `src/ga/` altinda koda baglandi.

---

## Ciktilar

| Cikti | Aciklama |
|-------|----------|
| Literatur Taramasi Dokumani | En az 10 kaynak ve ozetleri |
| Teknoloji Secim Raporu | Kutuphaneler ve gerekceleri |
| GitHub Reposu | Bos proje iskeleti |
| `requirements.txt` | Bagimliliklarin listesi |
| GA On Tasarim Dokumani | Kromozom, fitness, operatör kararlari |

---

## Basari Kriterleri

- [x] En az 10 ilgili akademik kaynak/makale incelenmis
- [x] Tum kutuphaneler belirlenip gerekceleri yazilmis
- [x] Gelistirme ortami kurulmus ve calisir durumda
- [x] Proje iskeleti GitHub'a yuklenmis
- [x] GA'nin temel tasarim kararlari alinmis ve dokumante edilmis

---

## Notlar

- Hocanin BTC fiyat tahmini makalesi mutlaka incelenecek ve referans verilecek
- Literatur taramasi rapor icin kritik - "Arastirma" bolumunn temelini olusturacak
- Proje basitlikten uzak olmali; sadece hazir yontem uygulayip sonuc gostermek yeterli degil
- GA'nin neden secildigi ve klasik ML yontemlerine gore avantajlari aciklanabilmeli
