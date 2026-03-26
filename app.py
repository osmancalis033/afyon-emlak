import streamlit as st
import json
from pathlib import Path

# ── 1. SAYFA AYARLARI ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AfyonEmlak | Bölge Uzmanı",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded", # Yan menü hep açık
)

# ── 2. VERİ YÜKLEME SİSTEMİ ──────────────────────────────────────────────────
def load_data():
    listings_path = Path("data/listings.json")
    advisor_path = Path("data/advisor.json")
    
    # Varsayılan boş veriler
    listings = []
    advisor = {
        "ad_soyad": "Osman",
        "unvan": "Gayrimenkul Danışmanı",
        "telefon": "+90 5XX XXX XX XX",
        "email": "osman@afyonemlak.com"
    }

    if listings_path.exists():
        listings = json.loads(listings_path.read_text(encoding="utf-8"))
    if advisor_path.exists():
        advisor = json.loads(advisor_path.read_text(encoding="utf-8"))
        
    return listings, advisor

listings, advisor = load_data()

# ── 3. CSS MODERN TASARIM ────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');
    
    .main { background-color: #fcfaf7; }
    
    /* Hero Banner */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center;
        padding: 60px 20px; border-radius: 15px; text-align: center; color: white;
        margin-bottom: 30px;
    }
    
    /* İlçe Kartları */
    .ilce-box {
        background: white; padding: 20px; border-radius: 10px;
        border: 1px solid #eee; text-align: center; transition: 0.3s;
    }
    .ilce-box:hover { border-color: #B5622A; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    
    /* Sidebar Stili */
    [data-testid="stSidebar"] { background-color: #1E1610; color: white; }
    [data-testid="stSidebar"] h3 { color: #C4A97D !important; }
</style>
""", unsafe_allow_html=True)

# ── 4. YAN MENÜ (SIDEBAR) ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {advisor.get('ad_soyad')}")
    st.caption(f"{advisor.get('unvan')}")
    st.divider()
    
    st.markdown("#### 🔍 Hızlı Filtre")
    f_tip = st.selectbox("İlan Tipi", ["Tümü", "Satılık", "Kiralık"])
    f_tur = st.selectbox("Mülk Türü", ["Tümü", "Daire", "Arsa", "Dükkan", "Müstakil Ev"])
    
    st.divider()
    st.markdown("#### 📞 İletişim")
    st.write(f"📱 {advisor.get('telefon')}")
    st.write(f"✉️ {advisor.get('email')}")
    
    if st.button("🆘 Destek Talebi Oluştur", use_container_width=True):
        st.toast("Talebiniz danışmana iletildi!", icon="📩")

# ── 5. ANA SAYFA VE İLÇE NAVİGASYONU ─────────────────────────────────────────
# URL Parametresi Kontrolü
current_ilce = st.query_params.get("ilce", "Tümü")

if current_ilce == "Tümü":
    st.markdown("""
    <div class="hero-section">
        <h1 style='font-family:Playfair Display; font-size: 3rem;'>Afyonkarahisar Gayrimenkul Rehberi</h1>
        <p style='font-size: 1.2rem;'>Bölgenin en güncel ve güvenilir ilanları burada.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"## 📍 {current_ilce} Bölgesindeki İlanlar")
    if st.button("⬅️ Tüm Bölgeleri Gör"):
        st.query_params.clear()
        st.rerun()

# İlçe Kartları (Menü Görevi Görür)
st.subheader("Bölgeleri Keşfedin")
ilceler = ["Merkez", "Sandıklı", "İscehisar", "Dinar", "Emirdağ", "Bolvadin"]
cols = st.columns(6)

for i, ilce in enumerate(ilceler):
    with cols[i]:
        # Kart görünümlü butonlar
        if st.button(f"🏛️\n\n{ilce}", key=f"btn_{ilce}", use_container_width=True):
            st.query_params["ilce"] = ilce
            st.rerun()

st.divider()

# ── 6. İLANLARI LİSTELEME ────────────────────────────────────────────────────
# Filtreleme Mantığı
filtered_listings = [l for l in listings if l.get("aktif", True)]

if current_ilce != "Tümü":
    filtered_listings = [l for l in filtered_listings if l["ilce"] == current_ilce]
if f_tip != "Tümü":
    filtered_listings = [l for l in filtered_listings if l["tip"] == f_tip]
if f_tur != "Tümü":
    filtered_listings = [l for l in filtered_listings if l["tur"] == f_tur]

# İlan Kartları
if not filtered_listings:
    st.warning("Bu kriterlere uygun ilan bulunamadı.")
else:
    st.write(f"**Toplam {len(filtered_listings)} ilan listeleniyor.**")
    grid = st.columns(3)
    
    for idx, ilan in enumerate(filtered_listings):
        with grid[idx % 3]:
            # Görsel Seçimi (Unsplash - Ücretsiz)
            img_query = "apartment" if ilan["tur"] == "Daire" else "modern-house"
            if ilan["tur"] == "Arsa": img_query = "nature-land"
            
            st.image(f"https://source.unsplash.com/featured/600x400?{img_query}&sig={ilan['id']}", 
                     use_container_width=True, caption=f"{ilan['tur']} - {ilan['tip']}")
            
            st.markdown(f"### {ilan['baslik']}")
            st.markdown(f"#### ₺{ilan['fiyat']:,}".replace(",", "."))
            st.write(f"📍 {ilan['ilce']} / {ilan['mahalle']}")
            
            with st.expander("🔍 İlan Detaylarını Gör"):
                st.write(f"📏 **Metrekare:** {ilan['metrekare']} m²")
                st.write(f"🛌 **Oda:** {ilan['oda']}")
                st.write(f"📝 **Açıklama:** {ilan['aciklama']}")
                st.write(f"✅ **Özellikler:** {', '.join(ilan['ozellikler'])}")
                st.link_button("💬 WhatsApp'tan Sor", f"https://wa.me/{advisor.get('whatsapp', '')}")

# ── 7. FOOTER ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>© 2026 AfyonEmlak - {advisor.get('ad_soyad')} Gayrimenkul Danışmanlığı</div>", unsafe_allow_html=True)
