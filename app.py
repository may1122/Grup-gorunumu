import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Nöbet Analiz Paneli")

# ================== EXCEL YÜKLE ==================
uploaded_file = st.file_uploader("Excel dosyasını yükle", type=["xlsx"])

if uploaded_file:

    @st.cache_data
    def load_data(file):
        return pd.read_excel(file)

    df = load_data(uploaded_file)

    # ================== KOLON KONTROL ==================
    gerekli = ["TARIH", "GRUP", "ECZANE"]
    if not all(col in df.columns for col in gerekli):
        st.error("Excel formatı hatalı!")
        st.stop()

    # ================== TARİH ==================
    df["TARIH"] = pd.to_datetime(df["TARIH"])
    df["GUN_IDX"] = df["TARIH"].dt.weekday
    df["GUN_TIPI"] = df["GUN_IDX"].apply(lambda x: "Hafta İçi" if x < 5 else "Hafta Sonu")

    # ================== GRUP SEÇ ==================
    grup_list = sorted(df["GRUP"].dropna().unique())
    secilen_grup = st.selectbox("Grup seç", grup_list)

    df = df[df["GRUP"] == secilen_grup]

    # ================== 3-6-9 AY ==================
    col1, col2, col3 = st.columns(3)

    if "secim" not in st.session_state:
        st.session_state.secim = 3

    if col1.button("3 AY"):
        st.session_state.secim = 3
    if col2.button("6 AY"):
        st.session_state.secim = 6
    if col3.button("9 AY"):
        st.session_state.secim = 9

    secim = st.session_state.secim

    max_tarih = df["TARIH"].max()
    min_tarih = max_tarih - pd.DateOffset(months=secim)

    filtre_df = df[df["TARIH"] >= min_tarih]

    # ================== ECZANE BAZLI PIVOT ==================
    pivot = (
        filtre_df
        .groupby(["ECZANE", "GUN_TIPI"])
        .size()
        .reset_index(name="NOBET_SAYISI")
    )

    pivot_table = pivot.pivot(
        index="ECZANE",
        columns="GUN_TIPI",
        values="NOBET_SAYISI"
    ).fillna(0)

    pivot_table["TOPLAM"] = pivot_table.sum(axis=1)

    pivot_table = pivot_table.sort_values(by="TOPLAM", ascending=False)

    st.subheader(f"📋 {secilen_grup} - Son {secim} Ay Eczane Bazlı Nöbet Dağılımı")
    st.dataframe(pivot_table, use_container_width=True)

    # ================== DENGE ANALİZİ ==================
    ortalama = pivot_table["TOPLAM"].mean()

    pivot_table["DURUM"] = pivot_table["TOPLAM"].apply(
        lambda x: "🔴 Fazla" if x > ortalama else "🟢 Az" if x < ortalama else "🟡 Dengeli"
    )

    st.subheader("⚖️ Denge Analizi")
    st.dataframe(pivot_table, use_container_width=True)

    # ================== GRAFİK ==================
    fig = px.bar(
        pivot,
        x="ECZANE",
        y="NOBET_SAYISI",
        color="GUN_TIPI",
        barmode="group",
        title=f"{secilen_grup} - Hafta İçi / Hafta Sonu Dağılımı"
    )

    st.plotly_chart(fig, use_container_width=True)
