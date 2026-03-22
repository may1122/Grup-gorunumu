import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("3 / 6 / 9 Ay Grup Karşılaştırma")

st.write("Excel dosyasını yükleyin")

uploaded_file = st.file_uploader(
    "Excel yükle",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.subheader("Veri")
    st.dataframe(df)

    # Grup seçimi
    gruplar = df["Grup"].unique()

    secilen_grup = st.selectbox(
        "Grup seç",
        gruplar
    )

    df_grup = df[df["Grup"] == secilen_grup]

    toplam = df_grup[
        ["3 ay", "6 ay", "9 ay"]
    ].sum()

    st.subheader("Grafik")

    fig, ax = plt.subplots()

    ax.bar(
        ["3 ay", "6 ay", "9 ay"],
        toplam.values
    )

    ax.set_title(
        f"{secilen_grup} grubu"
    )

    st.pyplot(fig)
