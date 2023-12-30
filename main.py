import streamlit as st
import pandas as pd
from modules.cyk import is_accepted, get_table_element


def display_results(text_accepted, text, data):
    if text_accepted:
        st.success("Kalimat diterima:")
        st.write(text)
    else:
        st.error("Kalimat tidak diterima.")

    if data is not None:
        st.write("Tabel Parsing:")
        st.table(data)


def main():
    st.title("Parsing Kalimat Bahasa Indonesia")
    st.divider()

    st.subheader("Kelompok D5")
    st.caption(
        "Tun Pasek Sarwiko Dipranoto (2208561023), Komang Gede Bagus Devit Aditiya (2208561073), Putu Ananda Darma Wiguna (2208561099), I Komang Dwiprayoga (2208561117)"
    )
    st.caption("")
    st.divider()

    input_text = st.text_input("Input kalimat adjektiva")
    text = input_text.lower().split(" ")

    text_accepted = is_accepted(text)
    result = get_table_element(input_text)

    data = pd.DataFrame(result)
    data = data.style.highlight_null(props="color: transparent;")

    if st.button("Periksa") and text:
        display_results(text_accepted, text, data)
    elif not text:
        st.warning("Masukkan kalimat untuk diperiksa.")


if __name__ == "__main__":
    main()
