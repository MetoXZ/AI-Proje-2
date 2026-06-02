# Mert Rapor Notlari

Bu notlar Faz 6 rapor yazimi icin Mert'in sorumlu oldugu Problem Tanimi, GA yapisi ve performans iyilestirme bolumlerinde kullanilmak uzere hazirlanmistir.

## Bolum 1: Problem Tanimi

Bitcoin fiyat hareketleri yuksek volatilite, 7/24 islem yapisi, haber akisi ve piyasa duyarliligi gibi etkenler nedeniyle klasik kurallarla tahmin edilmesi zor bir finansal zaman serisi problemidir. Bu projede amac, tek bir sabit al-sat kuralina bagli kalmak yerine RSI, MACD, Bollinger Bands ve SMA gibi teknik indikatorlerin periyot, esik ve agirlik parametrelerini Genetik Algoritma ile optimize ederek daha uyarlanabilir bir trading stratejisi elde etmektir.

Problem onemlidir cunku manuel parametre secimi hem zaman alir hem de belirli bir piyasa donemine asiri uyum saglayabilir. GA, genis ve surekli/ayrik karisik arama uzayinda birden cok parametreyi ayni anda iyilestirebildigi icin bu probleme uygundur. Kromozomdaki 16 gen; indikator periyotlarini, RSI esiklerini, stop-loss/take-profit oranlarini ve indikator agirliklarini temsil eder.

Projenin kapsami; BTC kapanis fiyatlari uzerinden teknik indikator tabanli sinyal uretmek, bu sinyalleri vektorel backtesting ile test etmek ve GA fitness fonksiyonuna Sharpe Ratio, toplam getiri, maksimum drawdown ve islem sayisi gibi metrikleri aktarmaktir. Gercek para ile islem, canli borsa emri veya yatirim tavsiyesi kapsam disidir.

## Bolum 4: GA Yapisi ve Onerilen Yontem

GA bireyi 16 genlik bir kromozom olarak tasarlanmistir. Tam sayi genler RSI/MACD/Bollinger/SMA periyotlarini, float genler esik ve risk oranlarini, son dort gen ise indikator sinyal agirliklarini temsil eder. `src/ga/chromosome.py` bu yapinin sinirlarini, dataclass tabanli `StrategyParams` arayuzunu, decode islemini ve tamir fonksiyonunu icerir.

Fitness hattinda `src/ga/fitness.py` kullanilir. Birey once `StrategyParams` nesnesine cozulur, sonra `generate_signals_fast` ile sinyal dizisi uretilir ve `run_backtest_fast` ile performans metrikleri hesaplanir. Tek amacli fitness, cezalar uygulanmis Sharpe Ratio degerini dondurur. Cok amacli fitness ise Sharpe Ratio ve toplam getiriyi maksimize, mutlak maksimum drawdown riskini minimize edecek sekilde tasarlanmistir.

Operator katmaninda `src/ga/operators.py` turnuva secimi, elitizm, BLX-alpha caprazlama, Gaussian mutasyon ve Uniform mutasyon fonksiyonlarini saglar. Her caprazlama ve mutasyon sonrasi birey otomatik tamir edilir; boylece gen sinirlari, `macd_fast < macd_slow`, `sma_short < sma_long`, `rsi_oversold < rsi_overbought` ve agirlik normalizasyonu korunur.

## Ek 1: Performans Iyilestirme

| Iyilestirme | Uygulama | Beklenen Etki |
|-------------|----------|---------------|
| Vektorel sinyal uretimi | `generate_signals_fast` ile DataFrame overhead'i azaltilir | Fitness cagri suresi duser |
| Vektorel backtesting | `run_backtest_fast` sadece numpy dizileriyle calisir | GA nesilleri daha hizli degerlendirilir |
| Kromozom tamir fonksiyonu | Gecersiz genler ve agirliklar fitness oncesi duzeltilir | Bos/gecersiz denemeler azalir |
| Penalizasyon | Az islem yapan veya gecersiz bireyler dusuk fitness alir | GA daha anlamli stratejilere yonelir |
| Elitizm | En iyi bireylerin yeni nesle aktarimi desteklenir | Iyi cozumlerin kaybolma riski azalir |

Bu iyilestirmeler Faz 4.2 ve Faz 4.3'te eklenen vektorel sinyal/backtest altyapisi ile uyumludur. Mert kapsamina eklenen fitness ve operator modulleri, bu altyapiyi GA cekirdegine baglayarak sonraki engine entegrasyonu icin hazir hale getirir.
