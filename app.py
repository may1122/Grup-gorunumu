import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Nöbet Sayısı Görünümü")

uploaded_file = st.file_uploader(
    "Excel yükle",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    st.write("Sütunlar:", df.columns)

    # ALT GRUP SEÇ
    gruplar = df["Grup"].unique()

    secilen_grup = st.selectbox(
        "Alt grup seç",
        gruplar
    )

    # SÜRE SEÇ
    sure = st.radio(
        "Süre seç",
        ["3 ay", "6 ay", "9 ay"],
        horizontal=True
    )

    # GRUP FİLTRE
    df_grup = df[df["Grup"] == secilen_grup]

    st.subheader(f"{secilen_grup} - {sure}")

    # Grafik
    fig, ax = plt.subplots()

    ax.bar(
        df_grup["Eczane"],
        df_grup[sure]
    )

    ax.set_ylabel("Nöbet sayısı")
    ax.set_xlabel("Eczane")

    plt.xticks(rotation=45)

    st.pyplot(fig)
