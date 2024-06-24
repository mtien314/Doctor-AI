import streamlit as st
import pandas as pd

# Page setup
#st.set_page_config(page_title="Doctor AI Search Engine", page_icon=":health_worker:", layout="wide")


def find_drug(df, text_search):
    # Filter the dataframe using masks
    if text_search:
        m1 = df["Name"].str.contains(text_search, case=False)
        m2 = df["Brand"].str.contains(text_search, case=False)
        df_search = df[m1 | m2]
        return df_search
    return pd.DataFrame()


def search_drugs():
    st.markdown("<h1 style='text-align: center; color: black;'>Công Cụ Tìm Kiếm Thuốc</h1>", unsafe_allow_html=True)

    # Connect to the drug dataset
    path = "drug_data2.csv"
    df = pd.read_csv(path, dtype=str).fillna("")

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("Nhập tên thuốc, thương hiệu thuốc hoặc tên bệnh", value= None)

    # Show the cards
    N_cards_per_row = 3
    if text_search:
        df_search = find_drug(df, text_search)

        if df_search.empty:
            st.markdown(
                "<h1 style='text-align: center; color: black; font-size: 20px;'>Không tìm thấy sản phẩm phù hợp.</h1>",
                unsafe_allow_html=True)

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")

        # draw the card
            with cols[n_row%N_cards_per_row]:
                name = row['Name'].strip()
                brand = row['Brand'].strip()
                img_link = row['Image Link'].strip()
                drug_link = row['Link'].strip()

                st.image(img_link, use_column_width=True)
                st.write(f"[{name}]({drug_link})")

                if row['Price'] != "['None']":
                    f = "'"
                    price = row['Price'][1:-1].replace(f, '').strip()
                    st.markdown(f"Giá: {price}")
