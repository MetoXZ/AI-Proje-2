# Yapay Zeka / Makine Öğrenmesi Proje Konu Alternatifleri

> Bu doküman, dönem projesi kapsamında değerlendirilebilecek proje konularını teknik açıdan incelemek amacıyla hazırlanmıştır. Her proje başlığı altında kullanılabilecek yöntemler, teknolojiler, veri setleri ve projeyi akademik olarak daha güçlü hale getirebilecek geliştirme fikirleri ele alınmıştır.

---

# 1. Bilgisayarlı Görü (Computer Vision)

Bilgisayarlı görü projeleri; görüntü veya video verileri üzerinden nesne, hareket, işaret, yüz veya durum analizi yapılmasını amaçlayan çalışmalardır. Bu tür projelerde genellikle CNN tabanlı derin öğrenme modelleri kullanılmaktadır.

---

## 1.1 Trafik İşareti Tanıma Sistemi

### Proje Konusu
Derin öğrenme tabanlı trafik işareti tanıma ve sınıflandırma sistemi geliştirilmesi.

### Teknik Yaklaşım

- GTSRB (German Traffic Sign Recognition Benchmark) veri seti kullanılabilir.
- CNN tabanlı bir sınıflandırma modeli geliştirilebilir.
- OpenCV kullanılarak görüntü ön işleme uygulanabilir.
- Veri artırma (Data Augmentation) teknikleri ile model dayanıklılığı artırılabilir.

### Kullanılabilecek Teknolojiler

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Matplotlib

### Projeyi Güçlendirebilecek Noktalar

- Hazır model yerine özgün CNN mimarisi tasarlanması
- Gerçek zamanlı kamera desteği eklenmesi
- Farklı hava koşullarının simüle edilmesi
- Görüntü gürültüsüne karşı model dayanıklılığı analizi
- Transfer Learning ile performans karşılaştırması

### Yapılabilecek Analizler

- Accuracy / Loss grafikleri
- Confusion Matrix
- Epoch karşılaştırmaları
- Batch size performans analizleri
- Veri artırma öncesi-sonrası başarı karşılaştırmaları

---

## 1.2 Yüz İfadesi ve Duygu Analizi Sistemi

### Proje Konusu
Kamera görüntüsünden insan yüz ifadelerini analiz ederek duygu durumunun tespit edilmesi.

### Teknik Yaklaşım

- Yüz tespiti için OpenCV veya Mediapipe kullanılabilir.
- CNN tabanlı sınıflandırma modeli geliştirilebilir.
- Duygular; mutlu, üzgün, kızgın, şaşkın gibi sınıflara ayrılabilir.

### Kullanılabilecek Teknolojiler

- TensorFlow
- OpenCV
- Mediapipe
- Keras

### Projeyi Güçlendirebilecek Noktalar

- Gerçek zamanlı analiz
- Video akışı üzerinden duygu takibi
- Birden fazla yüzü aynı anda analiz etme
- Yüz landmark verilerinin kullanılması

### Yapılabilecek Analizler

- Accuracy karşılaştırmaları
- Gerçek zamanlı FPS ölçümleri
- Model gecikme süresi analizi
- Veri seti boyutu etkisi

---

# 2. Doğal Dil İşleme (Natural Language Processing - NLP)

NLP projeleri; insan dilinin bilgisayar tarafından analiz edilmesi ve yorumlanmasını hedefleyen çalışmalardır.

---

## 2.1 Duygu Analizi (Sentiment Analysis)

### Proje Konusu
Film, ürün veya kullanıcı yorumlarının olumlu ya da olumsuz olarak sınıflandırılması.

### Teknik Yaklaşım

- IMDB veya Türkçe yorum veri setleri kullanılabilir.
- Metin ön işleme adımları uygulanabilir:
  - Stop-word temizleme
  - Tokenization
  - Lemmatization
- LSTM veya RNN tabanlı modeller geliştirilebilir.

### Kullanılabilecek Teknolojiler

- TensorFlow
- NLTK
- Scikit-learn
- Pandas

### Projeyi Güçlendirebilecek Noktalar

- Türkçe veri seti kullanımı
- Word2Vec ve GloVe embedding karşılaştırması
- Transformer tabanlı modeller ile kıyaslama
- Hibrit embedding yapıları

### Yapılabilecek Analizler

- Embedding boyutu karşılaştırmaları
- Dropout oranı etkisi
- Confusion Matrix
- Accuracy / Loss grafikleri
- Precision / Recall / F1-Score analizleri

---

## 2.2 Spam Mesaj Tespit Sistemi

### Proje Konusu
E-posta veya mesaj içeriklerinin spam olup olmadığını tespit eden sistem geliştirilmesi.

### Teknik Yaklaşım

- TF-IDF veya Word Embedding yöntemleri kullanılabilir.
- Naive Bayes, Logistic Regression veya LSTM modelleri karşılaştırılabilir.

### Kullanılabilecek Teknolojiler

- Scikit-learn
- TensorFlow
- Pandas
- NLTK

### Projeyi Güçlendirebilecek Noktalar

- Çoklu model karşılaştırması
- Türkçe mesaj veri seti desteği
- Gerçek zamanlı mesaj analizi
- Yanlış pozitif oranlarının optimize edilmesi

### Yapılabilecek Analizler

- Precision / Recall analizleri
- Accuracy karşılaştırmaları
- Kelime önem dereceleri
- Hata oranı analizleri

---

# 3. Makine Öğrenmesi (Machine Learning)

Makine öğrenmesi projelerinde genellikle sayısal veriler üzerinden tahminleme, sınıflandırma veya karar destek sistemleri geliştirilmektedir.

---

## 3.1 Fiyat Tahminleme Sistemi

### Proje Konusu
Ev, araç veya ürün fiyatlarını geçmiş veriler üzerinden tahmin eden sistem geliştirilmesi.

### Teknik Yaklaşım

- Çok öznitelikli veri setleri kullanılabilir.
- Regresyon tabanlı makine öğrenmesi modelleri geliştirilebilir.
- Hiperparametre optimizasyonu uygulanabilir.

### Kullanılabilecek Teknolojiler

- Scikit-learn
- XGBoost
- Pandas
- NumPy

### Kullanılabilecek Yöntemler

- Linear Regression
- Random Forest
- XGBoost
- Support Vector Regression (SVR)

### Projeyi Güçlendirebilecek Noktalar

- Feature Engineering uygulanması
- GridSearchCV ile optimizasyon
- Ensemble yöntemleri
- Veri temizleme süreçlerinin detaylandırılması

### Yapılabilecek Analizler

- RMSE / MAE karşılaştırmaları
- Feature Importance grafikleri
- Model başarı karşılaştırmaları
- Parametre optimizasyon sonuçları

---

## 3.2 Öğrenci Başarı Tahminleme Sistemi

### Proje Konusu
Öğrencilerin akademik başarı durumlarını tahmin eden sistem geliştirilmesi.

### Teknik Yaklaşım

- Öğrenci geçmiş verileri üzerinden model eğitilebilir.
- Başarıyı etkileyen faktörler analiz edilebilir.

### Kullanılabilecek Yöntemler

- Decision Tree
- Random Forest
- Logistic Regression

### Projeyi Güçlendirebilecek Noktalar

- Veri görselleştirme desteği
- Risk analizi sistemi
- Başarıya etki eden özniteliklerin yorumlanması

### Yapılabilecek Analizler

- Öznitelik önem dereceleri
- Accuracy karşılaştırmaları
- Veri dengesizliği analizleri

---

# 4. Meta-Sezgisel Optimizasyon

Bu projelerde amaç; belirli kısıtlar altında en uygun çözümü bulabilen algoritmalar geliştirmektir.

---

## 4.1 Genetik Algoritma ile Ders Programı Oluşturma

### Proje Konusu
Belirli kısıtlar altında en uygun haftalık ders programının oluşturulması.

### Teknik Yaklaşım

- Genetik Algoritma (GA) kullanılabilir.
- Fitness Function tasarlanabilir.
- Mutation ve Crossover stratejileri uygulanabilir.

### Kullanılabilecek Teknolojiler

- Python
- NumPy
- Matplotlib

### Problem Kısıtları

#### Sert Kısıtlar

- Ders çakışmaları
- Eğitmen uygunluğu
- Sınıf kapasitesi

#### Esnek Kısıtlar

- Tercih edilen saatler
- Gün içi yoğunluk dengesi

### Projeyi Güçlendirebilecek Noktalar

- Çoklu fitness kriterleri
- Dinamik kısıt sistemi
- Farklı seçim yöntemlerinin karşılaştırılması
- Adaptif mutation oranı

### Yapılabilecek Analizler

- Convergence grafikleri
- Nesil bazlı fitness değişimi
- Mutation rate analizleri
- Çözüm süresi karşılaştırmaları

---

## 4.2 Knapsack Problemi Çözümü

### Proje Konusu
Belirli kapasite altında maksimum değeri sağlayacak kombinasyonun bulunması.

### Kullanılabilecek Yöntemler

- Genetic Algorithm
- Simulated Annealing
- Particle Swarm Optimization

### Projeyi Güçlendirebilecek Noktalar

- Farklı optimizasyon algoritmalarının karşılaştırılması
- Çözüm süresi optimizasyonu
- Büyük veri boyutlarında performans testi

### Yapılabilecek Analizler

- Yakınsama grafikleri
- Algoritma başarı karşılaştırmaları
- Süre / performans analizleri

---

# 5. Genel Teknik Yaklaşımlar ve İyileştirme Fikirleri

Projeleri daha kapsamlı hale getirmek amacıyla aşağıdaki yöntemler projelere entegre edilebilir:

- Hiperparametre optimizasyonu
- Veri artırma (Data Augmentation)
- Ensemble yöntemleri
- Transfer Learning
- K-Fold Cross Validation
- Feature Selection
- Gerçek zamanlı analiz desteği
- Modüler pipeline mimarisi
- Otomatik grafik üretimi
- Deney sonuçlarının dinamik kaydı

---

# 6. Kullanılabilecek Genel Teknolojiler

| Teknoloji | Kullanım Alanı |
|---|---|
| Python | Ana geliştirme dili |
| TensorFlow / Keras | Derin öğrenme |
| PyTorch | Alternatif DL framework |
| Scikit-learn | Makine öğrenmesi |
| OpenCV | Görüntü işleme |
| Pandas | Veri analizi |
| NumPy | Matematiksel işlemler |
| Matplotlib | Grafik üretimi |
| Jupyter Notebook | Deneysel analiz |
| Git / GitHub | Versiyon kontrolü |

```