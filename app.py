import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Nöbet Analiz",
    layout="wide"
)

st.title("📊 Nöbet Sayısı Görünümü")

uploaded_file = st.file_uploader(
    "Excel dosyası yükle",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    col1, col2 = st.columns(2)

    with col1:
        gruplar = df["Grup"].unique()

        secilen_grup = st.selectbox(
            "Alt grup seç",
            gruplar
        )

    with col2:

        sure = st.radio(
            "Süre",
            ["3 ay", "6 ay", "9 ay"],
            horizontal=True
        )

    df_grup = df[df["Grup"] == secilen_grup]

    st.markdown("---")

    st.subheader(
        f"{secilen_grup} grubu - {sure}"
    )

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        df_grup["Eczane"],
        df_grup[sure]
    )

    ax.set_ylabel("Nöbet sayısı")

    plt.xticks(rotation=45)

    st.pyplot(fig, use_container_width=True)
