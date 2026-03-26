# 🏠 AfyonEmlak — Streamlit Gayrimenkul Websitesi

Afyonkarahisar'a özel, admin panelli gayrimenkul danışmanlık websitesi.

---

## 📁 Proje Yapısı

```
afyon-emlak/
├── app.py                  ← Ana website (ana sayfa)
├── pages/
│   └── 1_Admin.py          ← Şifreli admin paneli
├── data/
│   ├── listings.json       ← İlan veritabanı
│   └── advisor.json        ← Danışman bilgileri
├── .streamlit/
│   └── config.toml         ← Tema ve renk ayarları
├── requirements.txt
└── README.md
```

---

## 🚀 Yerel Kurulum

```bash
# 1. Repoyu klonlayın
git clone https://github.com/KULLANICI_ADINIZ/afyon-emlak.git
cd afyon-emlak

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Uygulamayı başlatın
streamlit run app.py
```

Tarayıcıda otomatik açılır: `http://localhost:8501`

---

## ☁️ Streamlit Cloud'a Deploy (Ücretsiz)

### Adım 1 — GitHub'a yükleyin
```bash
git init
git add .
git commit -m "İlk yükleme"
git remote add origin https://github.com/KULLANICI_ADINIZ/afyon-emlak.git
git push -u origin main
```

### Adım 2 — Streamlit Cloud'da yayınlayın
1. **[share.streamlit.io](https://share.streamlit.io)** adresine gidin
2. GitHub hesabınızla giriş yapın
3. **"New app"** → repo, branch ve `app.py` dosyasını seçin
4. **"Deploy!"** butonuna tıklayın

Birkaç dakika içinde siteniz canlıya alınır! 🎉

---

## 🔐 Admin Paneli

- **URL:** `https://SIZIN-URL.streamlit.app/Admin`
- **Varsayılan Şifre:** `afyon2025`
- **Şifre değiştirmek için:** `pages/1_Admin.py` dosyasının 10. satırını düzenleyin:
  ```python
  ADMIN_SIFRE = "yeni_sifreniz"
  ```

### Admin Panelinde neler yapabilirsiniz?
| Özellik | Açıklama |
|---------|----------|
| 📋 İlan Listesi | Tüm ilanları görün, aktif/pasif yapın, silin |
| ➕ Yeni İlan Ekle | Form ile kolayca ilan girin |
| 👤 Danışman Bilgileri | Ad, telefon, slogan, istatistikleri güncelleyin |

---

## ✏️ Kişiselleştirme

### Danışman bilgilerini güncelle
`data/advisor.json` dosyasını düzenleyin:
```json
{
  "ad_soyad": "Ad Soyad",
  "telefon": "+90 500 000 00 00",
  "whatsapp": "905000000000",
  "email": "info@afyonemlak.com",
  "adres": "Uzun Çarşı Cad. No:12, Afyonkarahisar"
}
```

### İlk ilanları ekle
`data/listings.json` dosyasını düzenleyin ya da Admin Paneli'ni kullanın.

### Renkleri değiştir
`.streamlit/config.toml` dosyasında:
```toml
[theme]
primaryColor = "#B5622A"   ← Ana renk (buton, vurgu)
backgroundColor = "#F8F5F0" ← Sayfa arka planı
```

---

## ⚠️ Önemli Not (Streamlit Cloud)

Streamlit Cloud'da dosyaya yazılan veriler (admin paneli değişiklikleri) **uygulama yeniden başladığında sıfırlanabilir.**

**Kalıcı veri için:**
- İlanları doğrudan `data/listings.json` içinde düzenleyip GitHub'a push edin
- Ya da Google Sheets / Supabase entegrasyonu eklenebilir (isteğe göre)

---

## 📞 Destek

Sorularınız için admin panelindeki iletişim bilgilerini güncelledikten sonra siteniz hazır!
