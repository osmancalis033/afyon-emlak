import streamlit as st
import json
from pathlib import Path

# ── Sayfa Ayarları ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AfyonEmlak | Güvenilir Gayrimenkul Danışmanlığı",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Veri Yükleme ─────────────────────────────────────────────────────────────
def load_listings() -> list:
    path = Path("data/listings.json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []

def load_advisor() -> dict:
    path = Path("data/advisor.json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

listings = load_listings()
advisor  = load_advisor()

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Genel sıfırlama */
*, *::before, *::after { box-sizing: border-box; }

:root {
  --cream:      #F5F0E8;
  --warm:       #EDE4D2;
  --stone:      #C4A97D;
  --terra:      #B5622A;
  --dark:       #1E1610;
  --charcoal:   #2E2318;
  --text:       #3A2E22;
  --muted:      #8A7A6A;
  --marble:     #F8F5F0;
}

/* Streamlit varsayılanlarını temizle */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: var(--charcoal); }

body { font-family: 'DM Sans', sans-serif; background: var(--marble); }

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #1E1610 0%, #3A2518 50%, #2E1A10 100%);
  padding: 5rem 4rem 4rem;
  position: relative; overflow: hidden;
}
.hero::before {
  content: '🏰';
  position: absolute; right: 6rem; top: 50%;
  transform: translateY(-50%); font-size: 14rem; opacity: .06;
  pointer-events: none;
}
.hero-badge {
  display: inline-block;
  background: rgba(196,169,125,.15); border: 1px solid rgba(196,169,125,.3);
  color: var(--stone); padding: .4rem 1rem; border-radius: 2px;
  font-size: .78rem; letter-spacing: .1em; text-transform: uppercase;
  font-weight: 600; margin-bottom: 1.5rem;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 900;
  color: #fff; line-height: 1.1; margin-bottom: 1rem;
}
.hero-title em { color: var(--terra); font-style: italic; }
.hero-sub { font-size: 1.05rem; color: rgba(255,255,255,.6); line-height: 1.7; max-width: 520px; margin-bottom: 2rem; }
.hero-stats { display: flex; gap: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,.1); }
.stat-num  { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #fff; }
.stat-num span { color: var(--terra); }
.stat-lbl  { font-size: .75rem; color: rgba(255,255,255,.45); letter-spacing: .06em; text-transform: uppercase; }

/* ── SECTION LABELS ── */
.sec-label {
  font-size: .75rem; color: var(--terra); letter-spacing: .12em;
  text-transform: uppercase; font-weight: 600; margin-bottom: .5rem;
}
.sec-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 700;
  color: var(--dark); line-height: 1.15; margin-bottom: .5rem;
}
.sec-sub { font-size: .95rem; color: var(--muted); line-height: 1.7; }

/* ── İLAN KARTI ── */
.ilan-card {
  background: white; border-radius: 6px; overflow: hidden;
  border: 1px solid rgba(196,169,125,.2);
  transition: transform .25s, box-shadow .25s;
  height: 100%;
}
.ilan-card:hover { transform: translateY(-5px); box-shadow: 0 16px 40px rgba(30,22,16,.1); }

.ilan-top {
  height: 180px; display: flex; align-items: center; justify-content: center;
  font-size: 4rem; position: relative;
}
.tag {
  position: absolute; top: .8rem; left: .8rem;
  font-size: .7rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; padding: .3rem .7rem; border-radius: 2px;
  color: white;
}
.tag-satilik { background: var(--terra); }
.tag-kiralik  { background: #3A6B45; }
.tag-ticari   { background: #2A4A6B; }

.ilan-body { padding: 1.2rem; }
.ilan-addr { font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; margin-bottom: .3rem; }
.ilan-name { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 600; color: var(--dark); margin-bottom: .7rem; line-height: 1.3; }
.ilan-feats { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: .8rem; }
.feat { font-size: .8rem; color: var(--muted); }
.ilan-footer { display: flex; justify-content: space-between; align-items: flex-end; padding-top: .8rem; border-top: 1px solid var(--warm); }
.ilan-price { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: var(--terra); }
.ilan-m2    { font-size: .72rem; color: var(--muted); }

/* ── DANIŞMAN ── */
.advisor-box {
  background: linear-gradient(135deg, var(--warm) 0%, var(--cream) 100%);
  border: 1px solid rgba(196,169,125,.3); border-radius: 8px;
  padding: 2.5rem; height: 100%;
}
.advisor-quote {
  font-family: 'Playfair Display', serif; font-size: 1.15rem;
  font-style: italic; color: var(--dark); line-height: 1.65; margin-bottom: 1.5rem;
  border-left: 3px solid var(--terra); padding-left: 1rem;
}
.advisor-name  { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; color: var(--dark); }
.advisor-title { font-size: .82rem; color: var(--muted); margin-bottom: 1.5rem; }
.contact-row   { display: flex; align-items: center; gap: .7rem; font-size: .9rem; color: var(--text); margin-bottom: .6rem; }

/* ── BÖLGE KARTI ── */
.bolge-card {
  border-radius: 6px; overflow: hidden; position: relative; cursor: pointer;
  transition: transform .25s; height: 160px;
  display: flex; align-items: flex-end;
  padding: 1rem 1.2rem;
  color: white;
}
.bolge-card:hover { transform: translateY(-3px); }
.bolge-name  { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; }
.bolge-count { font-size: .78rem; opacity: .8; }

/* ── CTA BANNER ── */
.cta-box {
  background: var(--terra); border-radius: 8px;
  padding: 3rem; text-align: center;
}
.cta-box h2 { font-family: 'Playfair Display', serif; font-size: 2rem; color: white; margin-bottom: .5rem; }
.cta-box p  { color: rgba(255,255,255,.8); margin-bottom: 1.5rem; font-size: 1rem; }

/* ── GENEL ── */
.divider { height: 1px; background: rgba(196,169,125,.2); margin: 1rem 0; }
a { color: var(--terra); }
</style>
""", unsafe_allow_html=True)

# ── Yardımcı Fonksiyonlar ─────────────────────────────────────────────────────
ILCE_EMOJI = {
    "Merkez":    ("🏰", "linear-gradient(135deg,#8B6F5E,#3A2E22)"),
    "Sandıklı":  ("♨️", "linear-gradient(135deg,#6B8A7A,#3A5A4A)"),
    "İscehisar": ("🪨", "linear-gradient(135deg,#7A6A9A,#4A3A7A)"),
    "Dinar":     ("🌾", "linear-gradient(135deg,#9A845A,#6A5430)"),
    "Emirdağ":   ("🏭", "linear-gradient(135deg,#6A8A9A,#3A5A6A)"),
    "Bolvadin":  ("🌿", "linear-gradient(135deg,#7A9A7A,#4A6A4A)"),
}
TUR_EMOJI = {
    "Daire": "🏢", "Müstakil Ev": "🏡", "Villa": "🏖️",
    "Arsa": "🌳", "Dükkan": "🏪", "Ofis": "💼",
}

def fmt_fiyat(fiyat: int, tip: str) -> str:
    if tip == "Kiralık":
        return f"₺{fiyat:,.0f}/ay".replace(",", ".")
    m = fiyat / 1_000_000
    return f"₺{m:.2f}M".replace(".", ",")

def tag_class(tip: str) -> str:
    return {"Satılık": "tag-satilik", "Kiralık": "tag-kiralik"}.get(tip, "tag-ticari")

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">◆ Afyonkarahisar · Güvenilir Gayrimenkul Danışmanlığı</div>
  <h1 class="hero-title">Afyon'da<br/><em>Hayalinizdeki</em><br/>Mülkü Bulun</h1>
  <p class="hero-sub">
    Afyonkarahisar'ın merkezinden termal bölgelerine, konuttan ticari gayrimenkule —
    {advisor.get('deneyim_yil',15)} yıllık deneyimle doğru mülkü bulmanızda yanınızdayız.
  </p>
  <div class="hero-stats">
    <div>
      <div class="stat-num">{advisor.get('satis_adet',500)}<span>+</span></div>
      <div class="stat-lbl">Tamamlanan Satış</div>
    </div>
    <div>
      <div class="stat-num">{advisor.get('deneyim_yil',15)}<span> yıl</span></div>
      <div class="stat-lbl">Sektör Deneyimi</div>
    </div>
    <div>
      <div class="stat-num">{advisor.get('memnuniyet',98)}<span>%</span></div>
      <div class="stat-lbl">Müşteri Memnuniyeti</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ARAMA / FİLTRE
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    st.markdown("""
    <div style='padding:0 2rem'>
      <div class="sec-label">🔍 Mülk Arayın</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        filtre_tip  = st.selectbox("İlan Tipi", ["Tümü", "Satılık", "Kiralık"])
    with col2:
        filtre_tur  = st.selectbox("Mülk Türü", ["Tümü", "Daire", "Müstakil Ev", "Arsa", "Dükkan", "Ofis"])
    with col3:
        ilceler = ["Tümü"] + sorted({l["ilce"] for l in listings})
        filtre_ilce = st.selectbox("İlçe", ilceler)
    with col4:
        fiyat_opts = {
            "Tüm Fiyatlar":    (0, 999_999_999),
            "0 – 1M":          (0, 1_000_000),
            "1M – 3M":         (1_000_000, 3_000_000),
            "3M – 5M":         (3_000_000, 5_000_000),
            "5M+":             (5_000_000, 999_999_999),
        }
        filtre_fiyat = st.selectbox("Fiyat Aralığı", list(fiyat_opts.keys()))

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# Filtre uygula
def filtrele(lst):
    fmin, fmax = fiyat_opts[filtre_fiyat]
    return [
        l for l in lst
        if l.get("aktif", True)
        and (filtre_tip  == "Tümü" or l["tip"]  == filtre_tip)
        and (filtre_tur  == "Tümü" or l["tur"]  == filtre_tur)
        and (filtre_ilce == "Tümü" or l["ilce"] == filtre_ilce)
        and (fmin <= l["fiyat"] <= fmax)
    ]

gosterilen = filtrele(listings)

# ══════════════════════════════════════════════════════════════════════════════
# İLANLAR
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    pad = "padding:0 2rem"
    st.markdown(f"""
    <div style='{pad}'>
      <div class="sec-label">Öne Çıkan İlanlar</div>
      <div class="sec-title">Seçili Mülkler</div>
      <div class="sec-sub">{len(gosterilen)} ilan listeleniyor</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    if not gosterilen:
        st.info("Bu filtrelere uygun ilan bulunamadı.")
    else:
        cols = st.columns(3)
        for i, ilan in enumerate(gosterilen):
            emoji   = TUR_EMOJI.get(ilan["tur"], "🏠")
            bg_idx  = (i % 6) + 1
            renk    = ["#D4B896","#8FA89A","#A8A0C4","#C4A87A","#8AA8B8","#B8A88A"][i % 6]
            renk2   = ["#C4927A","#6A8A7A","#7A6AA8","#A8845A","#5A7A96","#9A8060"][i % 6]

            oda_txt = f"🛏️ {ilan['oda']}" if ilan["oda"] != "-" else ""
            ban_txt = f"🚿 {ilan['banyo']} Banyo" if ilan["banyo"] else ""
            m2_txt  = f"📐 {ilan['metrekare']} m²"
            feats   = " &nbsp;·&nbsp; ".join(filter(None, [oda_txt, ban_txt, m2_txt]))

            tag_c   = tag_class(ilan["tip"])
            fiyat_s = fmt_fiyat(ilan["fiyat"], ilan["tip"])
            m2_birim = f"~₺{ilan['fiyat']//ilan['metrekare']:,}/m²".replace(",",".") if ilan["metrekare"] else ""

            with cols[i % 3]:
                st.markdown(f"""
                <div class="ilan-card">
                  <div class="ilan-top" style="background:linear-gradient(135deg,{renk},{renk2})">
                    {emoji}
                    <span class="tag {tag_c}">{ilan['tip']}</span>
                  </div>
                  <div class="ilan-body">
                    <div class="ilan-addr">📍 {ilan['ilce']}, {ilan['mahalle']}</div>
                    <div class="ilan-name">{ilan['baslik']}</div>
                    <div class="ilan-feats"><span class="feat">{feats}</span></div>
                    <div class="ilan-footer">
                      <div>
                        <div class="ilan-price">{fiyat_s}</div>
                        <div class="ilan-m2">{m2_birim}</div>
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("📋 Detay & Açıklama"):
                    st.write(ilan.get("aciklama", ""))
                    if ilan.get("ozellikler"):
                        st.write("**Özellikler:** " + " · ".join(ilan["ozellikler"]))

# ══════════════════════════════════════════════════════════════════════════════
# BÖLGELER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='padding:0 2rem'>
  <div class="sec-label">Lokasyona Göre</div>
  <div class="sec-title">Afyon'un İlçeleri</div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

bolge_sayilari = {l["ilce"]: 0 for l in listings}
for l in listings:
    if l.get("aktif"):
        bolge_sayilari[l["ilce"]] = bolge_sayilari.get(l["ilce"], 0) + 1

bolge_cols = st.columns(len(ILCE_EMOJI))
for col, (ilce, (emoji, grad)) in zip(bolge_cols, ILCE_EMOJI.items()):
    sayi = bolge_sayilari.get(ilce, 0)
    with col:
        st.markdown(f"""
        <div class="bolge-card" style="background:{grad};">
          <div>
            <div style="font-size:2rem;margin-bottom:.3rem">{emoji}</div>
            <div class="bolge-name">{ilce}</div>
            <div class="bolge-count">{sayi} İlan</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DANIŞMAN
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='padding:0 2rem'>
  <div class="sec-label">Danışmanınız</div>
  <div class="sec-title">Hakkımda</div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])
with c1:
    st.markdown(f"""
    <div class="advisor-box">
      <div class="advisor-quote">{advisor.get('slogan','')}</div>
      <div class="advisor-name">{advisor.get('ad_soyad','')}</div>
      <div class="advisor-title">{advisor.get('unvan','')} · {advisor.get('deneyim_yil','')} Yıl Deneyim</div>
      <div class="contact-row">📞 {advisor.get('telefon','')}</div>
      <div class="contact-row">📧 {advisor.get('email','')}</div>
      <div class="contact-row">📍 {advisor.get('adres','')}</div>
      <div class="contact-row">💬 WhatsApp: +{advisor.get('whatsapp','')}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="cta-box">
      <h2>Ücretsiz Danışın</h2>
      <p>Mülk sorularınız için size özel, tarafsız bir değerlendirme sunalım.</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button(
        "📞 Hemen Ara",
        f"tel:{advisor.get('telefon','').replace(' ','')}",
        use_container_width=True,
    )
    st.link_button(
        "💬 WhatsApp ile Ulaş",
        f"https://wa.me/{advisor.get('whatsapp','')}",
        use_container_width=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:#1E1610;color:rgba(255,255,255,.5);padding:2rem 4rem;text-align:center;font-size:.85rem;">
  © 2025 AfyonEmlak — {advisor.get('ad_soyad','')} · Tüm hakları saklıdır.<br/>
  <span style="color:#C4A97D">Afyonkarahisar'ın Güvenilir Gayrimenkul Danışmanı</span>
</div>
""", unsafe_allow_html=True)
