import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("3 / 6 / 9 Ay Grup Karşılaştırma")

uploaded_file = st.file_uploader(
    "Excel yükle",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # SÜTUN TEMİZLE
    df.columns = df.columns.str.strip()

    st.write("Sütunlar:", df.columns)

    gruplar = df["Grup"].unique()

    secilen_grup = st.selectbox(
        "Grup seç",
        gruplar
    )

    df_grup = df[df["Grup"] == secilen_grup]

    toplam = df_grup[
        ["3 ay", "6 ay", "9 ay"]
    ].sum()

    fig, ax = plt.subplots()

    ax.bar(
        ["3 ay", "6 ay", "9 ay"],
        toplam.values
    )

    st.pyplot(fig)
