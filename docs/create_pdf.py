import os
import platform
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def get_system_font():
    """İşletim sistemine göre Arial fontunun yolunu bulur."""
    sys_type = platform.system()
    if sys_type == "Windows":
        font_path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Fonts", "arial.ttf")
        bold_path = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Fonts", "arialbd.ttf")
    elif sys_type == "Darwin":  # macOS
        font_path = "/Library/Fonts/Arial.ttf"
        bold_path = "/Library/Fonts/Arial Bold.ttf"
    else:  # Linux / Ubuntu
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        bold_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
    return font_path, bold_path

def create_project_plan_pdf(filename="Calisma_Surekliligi_Plani.pdf"):
    # 1. Font Kaydetme (Türkçe Karakter Çözümü)
    font_path, bold_path = get_system_font()
    
    # Eğer sistem fontu bulunamazsa varsayılana dön ama büyük ihtimalle bulacaktır
    if os.path.exists(font_path) and os.path.exists(bold_path):
        pdfmetrics.registerFont(TTFont('TurkishArial', font_path))
        pdfmetrics.registerFont(TTFont('TurkishArial-Bold', bold_path))
        main_font = 'TurkishArial'
        bold_font = 'TurkishArial-Bold'
    else:
        print("Sistem fontu bulunamadı, varsayılan fonta dönülüyor (Türkçe karakterler bozulabilir).")
        main_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'

    # PDF Doküman Ayarları
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    story = []
    
    # Stil Tanımlamaları
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=bold_font,
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1A365D'),
        alignment=1,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName=main_font,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName=bold_font,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName=main_font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=8
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName=main_font,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1A202C')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=bold_font,
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    # Doküman İçeriği (Tamamen Türkçe Karakterli)
    story.append(Paragraph("EGE ÜNİVERSİTESİ - BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ", title_style))
    story.append(Paragraph("Yapay Zeka Yöntemleri Dönem Projesi (P2) - Çalışma Sürekliliği Planı", subtitle_style))
    story.append(Spacer(1, 10))
    
    intro_text = (
        "Bu doküman, Yapay Zeka Yöntemleri dersi dönem projesi kapsamında talep edilen "
        "<b>'Finallerden önce en az 5 gün ve Final Haftasında en az 1 gün çalışma'</b> koşulunu "
        "eksiksiz yerine getirmek ve projenin sürekliliğini belgelemek amacıyla hazırlanmıştır. "
        "Plana sadık kalınarak yapılan çalışmalar, proje raporunun sonundaki ilgili tabloya işlenecektir."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("1. Finallerden Önceki 5 Günlük Geliştirme Süreci", h1_style))
    
    days_data = [
        ("1. Gün: Altyapı ve Veri Seti Hazırlığı", 
         "Proje konusunun netleştirilmesi, kaynak araştırması ve Kaggle/UCI gibi platformlardan veri setinin indirilmesi. Veri yükleme, temizleme, eksik verilerin kontrolü, normalizasyon ve veri setinin Train/Test (%80-%20) olarak ayrılması script'inin yazılması. (Raporda Problemin Tanımı ve Ön Çalışma bölümü doldurulur)."),
        ("2. Gün: Baseline (Temel) Modelin Kurulması", 
         "Sistemin temelini oluşturacak ilk yapay zeka model mimarisinin (Örn: Temel bir CNN veya klasik ML sınıflandırıcısı) kodlanması. Modelin ilk eğitiminin başlatılması, temel başarım metriklerinin (Loss, Accuracy) elde edilmesi ve model şemasının rapora eklenmesi."),
        ("3. Gün: Başarım İyileştirme ve Hiperparametre Optimizasyonu", 
         "Projenin basite kaçmaması koşulunu sağlamak adına modelin derinleştirilmesi; Dropout, Batch Normalization eklenmesi. Farklı optimizasyon yöntemlerinin (Adam, SGD) ve hiperparametrelerin (GridSearch/RandomSearch) test edilmesi. Kararsızlık matrisi (Confusion Matrix) ve başarım tablolarının rapora işlenmesi."),
        ("4. Gün: Ek Maddelerin Analizi ve Literatür Kıyaslaması", 
         "Modelin test setindeki tahminlerinin görselleştirilmesi. Raporda yüksek puan getiren Ek 1 (Başarım İyileştirme), Ek 2 (Özgün Değer/Literatüre Katkı) ve Ek 3 (Faydalanılan Kaynaklardan Farklar) bölümlerinin analizi ve detaylıca metne dökülmesi."),
        ("5. Gün: Üretken Yapay Zeka Araştırma Sorusu ve Rapor Birleştirme", 
         "Raporun en önemli adımlarından biri olan GenAI avantajları (10 madde), projede kullanım kanıtları ve riskleri içeren 'Araştırma Sorusu' kısmının yazılması. Sonuç, Kaynakça ve Çalışma Sürekliliği Listesinin ilk 5 gününün doldurularak rapor taslağının (Min 5 - Max 13 sayfa) tamamlanması.")
    ]
    
    for title, desc in days_data:
        story.append(Paragraph(f"<b>{title}</b>", body_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 5))
        
    story.append(Paragraph("2. Final Haftasındaki Zorunlu Çalışma Günü", h1_style))
    final_day_desc = (
        "<b>6. Gün (Final Haftası): Kodların Son Testi, Demo Videosu ve Özdeğerlendirme</b><br/>"
        "Geliştirilen yapay zeka kodunun son kez entegre şekilde çalıştırılması. Hocanın talep ettiği 5-10 dakikalık "
        "proje tanıtım, kod açıklama ve rapor sunum videosunun (Demo Videosu) çekilmesi. Raporun sonundaki "
        "Özdeğerlendirme Tablosunun tahmin edilen puanlarla doldurulması ve projenin nihai teslimi."
    )
    story.append(Paragraph(final_day_desc, body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("3. Rapora Eklenecek Çalışma Sürekliliği Tablo Şablonu", h1_style))
    
    table_data = [
        [Paragraph("<b>Tarih / Dönem</b>", table_header_style), 
         Paragraph("<b>Yapılan Çalışma / İş Paketi</b>", table_header_style), 
         Paragraph("<b>Geliştirilen Kod / Rapor Bölümü</b>", table_header_style), 
         Paragraph("<b>Kanıt (Commit ID / Ekran Görüntüsü)</b>", table_header_style)]
    ]
    
    raw_table_rows = [
        ("Finallerden Önce<br/>(1. Gün)", "Veri seti analizi, eksik verilerin temizlenmesi ve normalizasyon.", "data_preprocessing.py yazıldı. Problemin Tanımı ve Ön Çalışma dolduruldu.", "Git Commit ID: a1b2c3d"),
        ("Finallerden Önce<br/>(2. Gün)", "Baseline model mimarisinin tasarlanması ve ilk eğitim.", "baseline_model.py yazıldı. Önerilen Yöntem şeması eklendi.", "Git Commit ID: e4f5g6h"),
        ("Finallerden Önce<br/>(3. Gün)", "Hiperparametre optimizasyonu, katman ve LR denemeleri.", "optimization.py çalıştırıldı. Başarım metrikleri ve Hata Matrisi eklendi.", "Grafik Ekran Görüntüsü: Fig_3.png"),
        ("Finallerden Önce<br/>(4. Gün)", "Modelin iyileştirilmesi, literatürdeki çalışmalarla kıyaslama.", "Nihai model kaydedildi. Ek 1, Ek 2 ve Ek 3 bölümleri yazıldı.", "Rapor Ek Bölümleri"),
        ("Finallerden Önce<br/>(5. Gün)", "Üretken Yapay Zeka araştırması ve raporun birleştirilmesi.", "Araştırma Sorusu, Sonuç ve Kaynakça kısımları tamamlandı.", "Rapor Taslağı v1.0.pdf"),
        ("FİNAL HAFTASI<br/>(6. Gün)", "Kodların son testi, Demo Videosunun çekilmesi ve teslim.", "Özdeğerlendirme Tablosu dolduruldu. 5-10 dk'lık video kaydedildi.", "Video Linki & Nihai Rapor")
    ]
    
    for row in raw_table_rows:
        table_data.append([
            Paragraph(row[0], table_text_style),
            Paragraph(row[1], table_text_style),
            Paragraph(row[2], table_text_style),
            Paragraph(row[3], table_text_style)
        ])
        
    col_widths = [90, 160, 162, 120]
    project_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5282')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    
    story.append(project_table)
    doc.build(story)
    print(f"Başarılı: '{filename}' Türkçe karakter destekli olarak oluşturuldu.")

if __name__ == "__main__":
    create_project_plan_pdf()