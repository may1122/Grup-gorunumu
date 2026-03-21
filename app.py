import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Nöbet Analiz Paneli")

# ================== EXCEL YÜKLE ==================
uploaded_file = st.file_uploader("Excel dosyasını yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Tarih formatı
    df["TARIH"] = pd.to_datetime(df["TARIH"])

    # Hafta içi / hafta sonu
    df["GUN_IDX"] = df["TARIH"].dt.weekday
    df["GUN_TIPI"] = df["GUN_IDX"].apply(lambda x: "Hafta İçi" if x < 5 else "Hafta Sonu")

    # ================== GRUP SEÇ ==================
    grup_list = df["GRUP"].dropna().unique()
    secilen_grup = st.selectbox("Grup seç", grup_list)

    df = df[df["GRUP"] == secilen_grup]

    # ================== 3-6-9 AY BUTON ==================
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

    # ================== TARİH FİLTRE ==================
    max_tarih = df["TARIH"].max()
    min_tarih = max_tarih - pd.DateOffset(months=secim)

    filtre_df = df[df["TARIH"] >= min_tarih]

    # ================== AGGREGATION ==================
    pivot = (
        filtre_df
        .groupby(["GUN_TIPI", "ECZANE"])
        .size()
        .reset_index(name="NOBET_SAYISI")
    )

    # ================== GRAFİK ==================
    fig = px.bar(
        pivot,
        x="GUN_TIPI",
        y="NOBET_SAYISI",
        color="ECZANE",
        barmode="group",
        title=f"{secilen_grup} - Son {secim} Ay Hafta İçi / Hafta Sonu Nöbet Dağılımı"
    )

    st.plotly_chart(fig, use_container_width=True)
