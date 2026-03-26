import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# ── 1. SAYFA VE TEMA AYARLARI ────────────────────────────────────────────────
st.set_page_config(
    page_title="AfyonEmlak | Profesyonel Bölge Portalı",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. VERİ YÖNETİMİ ─────────────────────────────────────────────────────────
def load_all_data():
    listings = []
    advisor = {}
    
    lp = Path("data/listings.json")
    ap = Path("data/advisor.json")
    
    if lp.exists():
        listings = json.loads(lp.read_text(encoding="utf-8"))
    if ap.exists():
        advisor = json.loads(ap.read_text(encoding="utf-8"))
    return listings, advisor

listings, advisor = load_all_data()

# ── 3. ÖZEL CSS TASARIMI ─────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { font-family: 'Playfair Display', serif; color: #1E1610; font-size: 3rem; margin-bottom: 0; }
    .sub-title { color: #8A7A6A; font-size: 1.1rem; margin-top: 0; margin-bottom: 2rem; }
    
    /* İlan Kartı Stili */
    .listing-card {
        background: white; border-radius: 15px; padding: 0;
        border: 1px solid #eee; transition: all 0.3s ease;
    }
    .listing-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    
    /* Etiketler */
    .badge {
        padding: 4px 10px; border-radius: 4px; font-size: 0.7rem; 
        font-weight: bold; text-transform: uppercase; color: white;
    }
    .badge-new { background-color: #28a745; }
    .badge-hot { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# ── 4. SIDEBAR (YAN MENÜ) ────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=80)
    st.title("Yönetim & Filtre")
    
    st.markdown("### 🔍 Arama Kriterleri")
    f_tip = st.radio("İşlem Türü", ["Tümü", "Satılık", "Kiralık"], horizontal=True)
    f_tur = st.multiselect("Mülk Tipi", ["Daire", "Arsa", "Dükkan", "Müstakil Ev", "Ofis"], default=["Daire", "Arsa"])
    
    st.markdown("### 💰 Fiyat Aralığı (TL)")
    f_min, f_max = st.slider("Bütçe", 0, 10_000_000, (0, 10_000_000), step=100_000)
    
    st.divider()
    st.markdown(f"**Bölge Danışmanı:** {advisor.get('ad_soyad', 'Osman')}")
    st.info(f"📍 {advisor.get('adres', 'Denizli Şubesi')}")
    
    if st.button("🔄 Filtreleri Sıfırla"):
        st.query_params.clear()
        st.rerun()

# ── 5. ANA PANEL VE İSTATİSTİKLER ──────────────────────────────────────────
current_ilce = st.query_params.get("ilce", "Tümü")

# Başlık Bölümü
col_t1, col_t2 = st.columns([2, 1])
with col_t1:
    st.markdown(f"<h1 class='main-title'>Afyonkarahisar {current_ilce if current_ilce != 'Tümü' else ''} Portföyü</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Profesyonel gayrimenkul çözümleri ve güncel piyasa verileri.</p>", unsafe_allow_html=True)

# İstatistik Özeti
s1, s2, s3, s4 = st.columns(4)
s1.metric("Toplam İlan", len(listings))
s2.metric("Aktif Portföy", sum(1 for l in listings if l.get('aktif')))
s3.metric("Ortalama m²", f"{int(sum(l['metrekare'] for l in listings)/len(listings))} m²" if listings else 0)
s4.metric("Memnuniyet", f"%{advisor.get('memnuniyet', 98)}")

st.divider()

# ── 6. İLÇE NAVİGASYONU (GÖRSEL MENÜ) ────────────────────────────────────────
st.write("### 🌍 Bölgeleri İncele")
ilceler = {
    "Merkez": "🏰", "Sandıklı": "♨️", "İscehisar": "🪨", 
    "Dinar": "🌾", "Emirdağ": "🏭", "Bolvadin": "🌿"
}
i_cols = st.columns(len(ilceler))

for i, (name, icon) in enumerate(ilceler.items()):
    with i_cols[i]:
        if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.query_params["ilce"] = name
            st.rerun()

# ── 7. İLAN LİSTELEME MANTIĞI ────────────────────────────────────────────────
# Filtrelerin Uygulanması
filtered = [l for l in listings if l.get("aktif", True)]

if current_ilce != "Tümü":
    filtered = [l for l in filtered if l["ilce"] == current_ilce]
if f_tip != "Tümü":
    filtered = [l for l in filtered if l["tip"] == f_tip]
if f_tur:
    filtered = [l for l in filtered if l["tur"] in f_tur]
filtered = [l for l in filtered if f_min <= l["fiyat"] <= f_max]

# İlan Kartlarının Basılması
if not filtered:
    st.warning("Aradığınız kriterlere uygun sonuç bulunamadı. Lütfen filtreleri genişletin.")
else:
    st.write(f"🔍 **{len(filtered)} sonuç listeleniyor**")
    
    rows = [filtered[i:i+3] for i in range(0, len(filtered), 3)]
    for row in rows:
        cols = st.columns(3)
        for idx, ilan in enumerate(row):
            with cols[idx]:
                # Etiket Belirleme (Örn: 5M altı fırsat, yeni tarihli ise yeni)
                is_new = "2025" in ilan.get("tarih", "") # Basit bir kontrol
                
                # Görsel ve Kart İçeriği
                img_url = f"https://source.unsplash.com/featured/600x400?architecture,house&sig={ilan['id']}"
                st.image(img_url, use_container_width=True)
                
                # Başlık ve Etiketler
                tags_html = ""
                if is_new: tags_html += '<span class="badge badge-new">YENİ</span> '
                if ilan["fiyat"] < 3000000: tags_html += '<span class="badge badge-hot">FIRSAT</span>'
                
                st.markdown(f"### {ilan['baslik']} {tags_html}", unsafe_allow_html=True)
                st.markdown(f"#### ₺{ilan['fiyat']:,}".replace(",", "."))
                
                st.write(f"📍 **{ilan['ilce']}** - {ilan['mahalle']}")
                st.caption(f"📏 {ilan['metrekare']}m² | 🚪 {ilan['oda']} | 🗓️ {ilan['tarih']}")
                
                with st.expander("📝 Detaylar ve Konum"):
                    st.write(ilan["aciklama"])
                    st.write("**Donanım:** " + " · ".join(ilan["ozellikler"]))
                    st.link_button("📍 Haritada Gör", f"https://www.google.com/maps/search/Afyon+{ilan['ilce']}+{ilan['mahalle']}")
                    st.link_button("📞 Danışmanı Ara", f"tel:{advisor.get('telefon')}")

# ── 8. FOOTER ────────────────────────────────────────────────────────────────
st.divider()
f_c1, f_c2 = st.columns([3, 1])
with f_c1:
    st.write(f"© 2026 AfyonEmlak Portalı. Tüm hakları saklıdır. {advisor.get('ad_soyad')} Gayrimenkul Danışmanlığı.")
with f_c2:
    st.write(f"**Lisans:** SPL Düzey 3 Adayı")
