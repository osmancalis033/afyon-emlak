import streamlit as st
import json
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Admin Paneli | AfyonEmlak",
    page_icon="⚙️",
    layout="wide",
)

# ── Şifre Koruması ────────────────────────────────────────────────────────────
ADMIN_SIFRE = "afyon2025"   # ← Buradan değiştirin

def check_login():
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.markdown("""
        <div style='max-width:400px;margin:4rem auto;text-align:center'>
          <h1 style='font-family:serif;color:#1E1610'>🔒 Admin Girişi</h1>
          <p style='color:#8A7A6A'>AfyonEmlak Yönetim Paneli</p>
        </div>
        """, unsafe_allow_html=True)
        _, mid, _ = st.columns([1,2,1])
        with mid:
            sifre = st.text_input("Şifre", type="password", placeholder="Admin şifrenizi girin")
            if st.button("Giriş Yap", use_container_width=True, type="primary"):
                if sifre == ADMIN_SIFRE:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Hatalı şifre!")
        st.stop()

check_login()

# ── Veri Yükleme / Kaydetme ───────────────────────────────────────────────────
LISTINGS_PATH = Path("data/listings.json")
ADVISOR_PATH  = Path("data/advisor.json")

def load_listings():
    if LISTINGS_PATH.exists():
        return json.loads(LISTINGS_PATH.read_text(encoding="utf-8"))
    return []

def save_listings(data):
    LISTINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_advisor():
    if ADVISOR_PATH.exists():
        return json.loads(ADVISOR_PATH.read_text(encoding="utf-8"))
    return {}

def save_advisor(data):
    ADVISOR_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Başlık ────────────────────────────────────────────────────────────────────
col_title, col_logout = st.columns([5,1])
with col_title:
    st.markdown("# ⚙️ Admin Paneli")
    st.markdown("İlanları ve danışman bilgilerini buradan yönetebilirsiniz.")
with col_logout:
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    if st.button("🚪 Çıkış", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

st.divider()

# ── Tab Yapısı ────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 İlanlar", "➕ Yeni İlan Ekle", "👤 Danışman Bilgileri"])

# ════════════════════════════════════════════════════════════
# TAB 1 — İlan Listesi
# ════════════════════════════════════════════════════════════
with tab1:
    listings = load_listings()

    if not listings:
        st.info("Henüz ilan yok. 'Yeni İlan Ekle' sekmesinden başlayabilirsiniz.")
    else:
        st.markdown(f"**Toplam {len(listings)} ilan** | Aktif: {sum(1 for l in listings if l.get('aktif'))}")
        st.markdown("")

        for i, ilan in enumerate(listings):
            with st.expander(
                f"{'✅' if ilan.get('aktif') else '⛔'} #{ilan['id']}  {ilan['baslik']}  —  {ilan['ilce']}",
                expanded=False
            ):
                e1, e2, e3, e4 = st.columns([2,1,1,1])
                with e1:
                    st.markdown(f"**{ilan['baslik']}**")
                    st.caption(f"{ilan['ilce']} · {ilan['mahalle']}")
                    st.write(ilan.get("aciklama", ""))
                with e2:
                    st.metric("Fiyat", f"₺{ilan['fiyat']:,.0f}".replace(",","."))
                    st.caption(f"{ilan['tip']} · {ilan['tur']}")
                with e3:
                    st.metric("m²", ilan["metrekare"])
                    st.caption(f"Oda: {ilan['oda']}")
                with e4:
                    # Aktif / Pasif toggle
                    yeni_durum = st.toggle(
                        "Aktif",
                        value=ilan.get("aktif", True),
                        key=f"aktif_{ilan['id']}"
                    )
                    if yeni_durum != ilan.get("aktif", True):
                        listings[i]["aktif"] = yeni_durum
                        save_listings(listings)
                        st.success("Durum güncellendi!")
                        st.rerun()

                    # Silme
                    if st.button("🗑️ Sil", key=f"sil_{ilan['id']}", type="secondary"):
                        listings = [l for l in listings if l["id"] != ilan["id"]]
                        save_listings(listings)
                        st.success(f"İlan #{ilan['id']} silindi.")
                        st.rerun()

# ════════════════════════════════════════════════════════════
# TAB 2 — Yeni İlan Ekle
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### ➕ Yeni İlan Formu")
    listings = load_listings()

    with st.form("yeni_ilan_form", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            baslik  = st.text_input("İlan Başlığı *", placeholder="Kale Manzaralı 3+1 Daire")
            tip     = st.selectbox("İlan Tipi *", ["Satılık", "Kiralık"])
            tur     = st.selectbox("Mülk Türü *", ["Daire", "Müstakil Ev", "Villa", "Arsa", "Dükkan", "Ofis"])
            ilce    = st.selectbox("İlçe *", ["Merkez", "Sandıklı", "İscehisar", "Dinar", "Emirdağ", "Bolvadin", "Diğer"])
            mahalle = st.text_input("Mahalle / Bölge", placeholder="Ordu Mah.")
        with f2:
            fiyat   = st.number_input("Fiyat (₺) *", min_value=0, step=10000, format="%d")
            metrekare = st.number_input("Alan (m²) *", min_value=0, step=5, format="%d")
            oda     = st.selectbox("Oda Sayısı", ["1+0", "1+1", "2+1", "3+1", "4+1", "5+1", "-"])
            banyo   = st.number_input("Banyo Sayısı", min_value=0, max_value=5, step=1)
            aktif   = st.checkbox("Yayında (aktif)", value=True)

        aciklama = st.text_area("Açıklama", placeholder="Mülk hakkında detaylı bilgi...", height=100)
        ozellikler_raw = st.text_input(
            "Özellikler (virgülle ayırın)",
            placeholder="Kale Manzarası, Asansör, Doğalgaz, Otopark"
        )

        submitted = st.form_submit_button("✅ İlanı Kaydet", use_container_width=True, type="primary")

        if submitted:
            if not baslik or fiyat == 0 or metrekare == 0:
                st.error("Lütfen zorunlu alanları doldurun (Başlık, Fiyat, m²).")
            else:
                yeni_id = max((l["id"] for l in listings), default=0) + 1
                ozellikler = [o.strip() for o in ozellikler_raw.split(",") if o.strip()]
                yeni_ilan  = {
                    "id": yeni_id,
                    "baslik": baslik,
                    "tip": tip,
                    "tur": tur,
                    "ilce": ilce,
                    "mahalle": mahalle,
                    "fiyat": int(fiyat),
                    "metrekare": int(metrekare),
                    "oda": oda,
                    "banyo": int(banyo),
                    "aciklama": aciklama,
                    "ozellikler": ozellikler,
                    "tarih": str(date.today()),
                    "aktif": aktif,
                }
                listings.append(yeni_ilan)
                save_listings(listings)
                st.success(f"✅ İlan #{yeni_id} başarıyla kaydedildi!")
                st.balloons()

# ════════════════════════════════════════════════════════════
# TAB 3 — Danışman Bilgileri
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 👤 Danışman Bilgilerini Güncelle")
    adv = load_advisor()

    with st.form("advisor_form"):
        a1, a2 = st.columns(2)
        with a1:
            ad_soyad   = st.text_input("Ad Soyad",    value=adv.get("ad_soyad", ""))
            unvan      = st.text_input("Unvan",        value=adv.get("unvan", "Lisanslı Gayrimenkul Danışmanı"))
            telefon    = st.text_input("Telefon",      value=adv.get("telefon", ""))
            whatsapp   = st.text_input("WhatsApp No (başında + olmadan)", value=adv.get("whatsapp", ""))
        with a2:
            email      = st.text_input("E-posta",      value=adv.get("email", ""))
            adres      = st.text_input("Ofis Adresi",  value=adv.get("adres", ""))
            deneyim    = st.number_input("Deneyim (yıl)", value=adv.get("deneyim_yil", 15), min_value=0)
            satis      = st.number_input("Toplam Satış Adedi", value=adv.get("satis_adet", 500), min_value=0)
            memnuniyet = st.slider("Müşteri Memnuniyeti (%)", 0, 100, adv.get("memnuniyet", 98))

        slogan = st.text_area("Kişisel Slogan / Alıntı", value=adv.get("slogan", ""), height=80)

        if st.form_submit_button("💾 Kaydet", use_container_width=True, type="primary"):
            save_advisor({
                "ad_soyad": ad_soyad,
                "unvan": unvan,
                "telefon": telefon,
                "whatsapp": whatsapp,
                "email": email,
                "adres": adres,
                "deneyim_yil": int(deneyim),
                "satis_adet": int(satis),
                "memnuniyet": memnuniyet,
                "slogan": slogan,
            })
            st.success("✅ Danışman bilgileri güncellendi!")
