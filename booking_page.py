import streamlit as st
import datetime
import pandas as pd
import numpy as np

def appointment():
    st.markdown("<h1 style='text-align: center; color: black;'>Đặt Lịch Hẹn Bác Sĩ</h1>", unsafe_allow_html=True)

    # Connect to the data
    path = "D:/Users/User/Downloads/PHÒNG KHÁM CHUYÊN GIA- BỆNH VIỆN CHỢ RẪY.xlsx"
    df = pd.read_excel(path, dtype=str).fillna("")
    print(df.head())
    availability = "Monday, Wednesday, Friday"
    time_slot = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]

    df['Availability'] = availability
    df['Time'] = [time_slot] * len(df)

    if "selected_time" not in st.session_state:
        st.session_state["selected_time"] = None


    # Function to select the doctor's time slot
    def select_name(name):
        st.session_state["selected_name"] = name


    def select_time(slot):
        st.session_state["selected_time"] = slot


    def select_day(day):
        st.session_state["selected_day"] = day

    doctor_columns, booking_column = st.columns([4, 3])

    # Doctors' individual information
    with doctor_columns:
        st.header("Thông Tin Bác Sĩ")
        temp_col_1, temp_col_2 = st.columns([2, 3])
        with temp_col_1:
            doctor_name = st.selectbox(r"$\textsf{\normalsize Chọn bác sĩ}$:red[$\textsf{\normalsize *}$]", df['Tên'].to_list())
            select_name(doctor_name)
        doctor_info = df[df['Tên'] == doctor_name]
    
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            print(doctor_info['Ảnh'].values[0])
            if doctor_info['Ảnh'].values[0] != "" :
                st.image(doctor_info['Ảnh'].values[0], width= 250)
            else:
                unknown_doctor = "D:/Users/User/Downloads/Unknown_person.jpg"
                st.image(unknown_doctor, width= 250)
        with col_2:
            st.subheader(doctor_name)
            st.write(f"*{doctor_info['Chức vụ'].values[0]}*")
            st.write(f"*Chuyên Ngành:* {doctor_info['Chuyên ngành'].values[0]}")

        # Inject custom CSS for the buttons
        st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        # Days
        st.write(f"*Ngày Khám Trong Tuần:*")
        col = st.columns([1, 1, 1, 1, 1])
        available_days = doctor_info['Availability'].values[0].split(", ")
        unavailable_days = []

        for idx in range(len(available_days)):
            with col[idx]:
             # st.button(available_days[idx])
                if available_days[idx] in unavailable_days:
                    st.button(available_days[idx], disabled=True)
                else:
                    if st.button(available_days[idx]):
                        select_time(available_days[idx])

         #Available slot
        st.write("*Thời gian khám:*")
        unavailable_slots = []
        available_slots = doctor_info["Time"].values[0]
        N_cards_per_row = 4
        for idx in range(len(available_slots)):
            i = idx % N_cards_per_row
            if i == 0:
                cols = st.columns(N_cards_per_row*2 - 1, gap='small')
            # draw the card
            with cols[idx % N_cards_per_row]:
                if available_slots[idx] in unavailable_slots:
                    st.button(available_slots[idx], disabled=True)
                else:
                    if st.button(available_slots[idx]):
                            select_time(available_slots[idx])

    with booking_column:
        st.header("Thông Tin Lịch Hẹn")
        name = st.text_input(r"$\textsf{\normalsize Họ tên}$:red[$\textsf{\normalsize *}$]", placeholder="Nhập tên của bạn")
        doctor_name = st.session_state["selected_name"]
        date = st.date_input(r"$\textsf{\normalsize Chọn ngày khám}$:red[$\textsf{\normalsize *}$]", min_value=datetime.date.today())

        # Determine available slots by excluding unavailable ones
        doctor_info = df[df['Tên'] == doctor_name]
        unavailable_slots = []

        all_slots = doctor_info["Time"].values[0]
        available_slots = [slot for slot in all_slots if slot not in unavailable_slots]

        # Maintain consistency with unavailable slots and session state
        selected_time = st.selectbox(r"$\textsf{\normalsize Thời gian khám}$:red[$\textsf{\normalsize *}$]", available_slots,\
                                 index=available_slots.index(st.session_state["selected_time"])\
                                     if st.session_state["selected_time"] in available_slots else 0)
        symptoms = st.text_area(r"$\textsf{\normalsize Triệu chứng}$",  placeholder="Nhập triệu chứng của bạn")
        notes = st.text_area(r"$\textsf{\normalsize  Ghi chú}$", placeholder="Ghi chú thêm dành cho bác sĩ")

        # Button to book appointment
        if st.button('Đặt hẹn'):
            if name == "":
                st.error("Bạn phải nhập tên.")
            else:
                st.success(f"Đặt lịch hẹn thành công với {doctor_name}. Thời gian {date.strftime('%A, %B %d, %Y')} vào lúc {selected_time}")
