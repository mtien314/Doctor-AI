import streamlit as st
from ast import literal_eval
import pandas as pd

# Page setup
#st.set_page_config(page_title="Doctor AI Search Engine", page_icon=":health_worker:", layout="wide")
#st.title("Công Cụ Tìm Kiếm Thông Tin Về Thuốc, Thương Hiệu ")

def search_drugs():
    st.markdown("<h1 style='text-align: center; color: black;'>Tìm kiếm thuốc</h1>", unsafe_allow_html=True)

    
    path = "drug_data2.csv"
    df = pd.read_csv(path, dtype=str).fillna("")

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("Nhập tên hoặc thương hiệu thuốc cần tìm kiếm", value="")

    # Filter the dataframe using masks
    m1 = df["Name"].str.contains(text_search, case=False)
    m2 = df["Brand"].str.contains(text_search, case=False)

    df_search = df[m1 | m2]
    N_cards_per_row = 3
    if text_search:
        for n_row, row in df_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i==0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
            with cols[n_row%N_cards_per_row]:
                st.image(row['Image Link'].strip(), use_column_width=True)
                st.caption(f"{row['Name'].strip()} - {row['Brand'].strip()} ")
                if row['Price'] != "['None']":
                    f = "'"
                    st.markdown(f"Giá: {row['Price'][1:-1].replace(f, '').strip()}")
                st.markdown(f"Chi tiết: **{row['Link'].strip()}**")
