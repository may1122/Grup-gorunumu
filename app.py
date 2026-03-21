import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Nöbet Analiz Paneli")

# ================== EXCEL YÜKLE ==================
uploaded_file = st.file_uploader("Excel dosyasını yükle", type=["xlsx"])

if uploaded_file is None:
    st.info("Lütfen bir Excel dosyası yükleyin.")
    st.stop()

# ================== VERİ OKUMA ==================
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"Dosya okunamadı: {e}")
    st.stop()

# ================== KOLON KONTROL ==================
gerekli_kolonlar = ["TARIH", "GRUP", "ECZANE"]

eksik = [col for col in gerekli_kolonlar if col not in df.columns]
if eksik:
    st.error(f"Eksik kolonlar: {eksik}")
    st.stop()

# ================== TARİH İŞLEME ==================
df["TARIH"] = pd.to_datetime(df["TARIH"], errors="coerce")
df = df.dropna(subset=["TARIH"])

if df.empty:
    st.error("Geçerli tarih içeren veri yok.")
    st.stop()

df["GUN_IDX"] = df["TARIH"].dt.weekday
df["GUN_TIPI"] = df["GUN_IDX"].apply(lambda x: "Hafta İçi" if x < 5 else "Hafta Sonu")

# ================== GRUP SEÇ ==================
gruplar = sorted(df["GRUP"].dropna().unique())

if not gruplar:
    st.error("Grup bulunamadı.")
    st.stop()

secilen_grup = st.selectbox("Grup seç", gruplar)

df = df[df["GRUP"] == secilen_grup]

if df.empty:
    st.warning("Bu grupta veri yok.")
    st.stop()

# ================== PERİYOT ==================
secim = st.radio("Periyot (Ay)", [3, 6, 9], horizontal=True)

max_tarih = df["TARIH"].max()
min_tarih = max_tarih - pd.DateOffset(months=secim)

filtre_df = df[df["TARIH"] >= min_tarih]

if filtre_df.empty:
    st.warning("Seçilen tarih aralığında veri yok.")
    st.stop()

# ================== PIVOT ==================
pivot = (
    filtre_df
    .groupby(["ECZANE", "GUN_TIPI"])
    .size()
    .reset_index(name="NOBET_SAYISI")
)

if pivot.empty:
    st.warning("Pivot oluşturulamadı.")
    st.stop()

pivot_table = pivot.pivot_table(
    index="ECZANE",
    columns="GUN_TIPI",
    values="NOBET_SAYISI",
    fill_value=0
)

pivot_table["TOPLAM"] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(by="TOPLAM", ascending=False)

# ================== TABLO ==================
st.subheader(f"📋 {secilen_grup} - Son {secim} Ay")

st.dataframe(pivot_table, use_container_width=True)

# ================== DENGE ==================
ortalama = pivot_table["TOPLAM"].mean()
tolerans = 1

pivot_table["DURUM"] = pivot_table["TOPLAM"].apply(
    lambda x: "🟡 Dengeli"
    if abs(x - ortalama) <= tolerans
    else "🔴 Fazla"
    if x > ortalama
    else "🟢 Az"
)

st.subheader("⚖️ Denge Analizi")
st.dataframe(pivot_table, use_container_width=True)

# ================== GRAFİK ==================
fig = px.bar(
    pivot,
    x="ECZANE",
    y="NOBET_SAYISI",
    color="GUN_TIPI",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)
