import numpy as np
import streamlit as st 
from streamlit_navigation_bar import st_navbar
import pandas as pd
from time import sleep
import bcrypt
from record import update_user,update_account,connect_sql,update_historylogs,update_appoinment2,cancel_appointment
from check import connect
from chat import display
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from booking_page import appointment
from search import search_drugs
import sqlite3
import datetime

st.set_page_config(page_title="Use", page_icon="👨‍🔬",layout="wide")

page2 = st_navbar(['Home','Chat','Search','Appointment','Profile','Logout'])

result = connect(table = 'user')
df = pd.DataFrame(result, columns =['ID','Email','Password','Use'])

n = len(df['ID'])   
name = ''
age = ''
phone = ''
id = ''
email = ''

if n!=0:
    passw = df['Password'][n-1]
    email = df['Email'][n-1]
    id = df['ID'][n-1]

if n == 0 or passw == '0':
    placeholder = st.empty()
     
    with placeholder.form("Change password"):
        st.markdown("### Update information")
        name = st.text_input(r"$\textsf{\normalsize Name}$:red[$\textsf{\normalsize *}$]", type ="default")
        age = st.text_input(r"$\textsf{\normalsize Age}$:red[$\textsf{\normalsize *}$]",type="default")
        phone = st.text_input(r"$\textsf{\normalsize Phone}$:red[$\textsf{\normalsize *}$]",type="default")
        gender = st.radio("Gender",("Male", "Female", "Prefer Not To Say"))
        new_pass = st.text_input(r"$\textsf{\normalsize Enter password}$:red[$\textsf{\normalsize *}$]", type = "password")
        password = st.text_input(r"$\textsf{\normalsize Enter password again}$:red[$\textsf{\normalsize *}$]", type = "password")
        submit = st.form_submit_button("submit")

        hash_passw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    if submit:

        if new_pass != password or name =="" or age =="" or password =="":
            st.warning("Please check new_pass and pass again")
        else:
            st.success("Change password success")
            sleep(0.5)
            update_user(hash_passw)
      
            update_account(id, name, age, email, phone)
            placeholder.empty()



@st.cache_resource
def load_data3():
    loader = CSVLoader(file_path="D:/Users/User/Downloads/PHÒNG KHÁM CHUYÊN GIA- BỆNH VIỆN CHỢ RẪY.csv",encoding="utf8")
    data = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    chunks = splitter.split_documents(data)
    
    embeddings = HuggingFaceEmbeddings()
   
    vector_index = Chroma.from_documents(chunks,embeddings)
    print("Loading data success..")

    return vector_index, chunks

vector_index,chunks = load_data3()

if page2 == 'Home':
            
    if passw !='0' and passw !="":
        st.header("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
        st.image("D:/Users/User/Downloads/chatbot.jpg",output_format="auto")
        st.write("Mô Tả: Đưa sức khỏe của bạn vào tay của công nghệ với Doctor AI - chatbot y tế tiên tiến nhất, hỗ trợ bạn từ việc chẩn đoán ban đầu đến quản lý bệnh mãn tính.")
        st.header("Doctor AI là gì?")
        st.write("Doctor AI là một chatbot y tế thông minh, được thiết kế để cung cấp cho bạn các lời khuyên y tế chính xác và kịp thời. Với sự hỗ trợ của công nghệ AI tiên tiến, Doctor AI có khả năng chẩn đoán các triệu chứng ban đầu, cung cấp thông tin về các bệnh lý và giúp quản lý các bệnh mãn tính.")
        st.image("D:/Users/User/Downloads/chatbot2.py")
        st.header("Những Tính Năng Nổi Bật của Doctor AI")
        st.write("+ Chẩn Đoán Ban Đầu: Phân tích các triệu chứng và đưa ra các dự đoán về bệnh lý có thể mắc phải.")
        st.write("+ Thông Tin Y Khoa Đầy Đủ: Cung cấp thông tin chi tiết về các bệnh lý, thuốc và phương pháp điều trị.")
        st.header("Doctor AI Hoạt Động Như Thế Nào?")
        st.write("Doctor AI sử dụng công nghệ AI tiên tiến để phân tích dữ liệu y tế từ người dùng. Bạn chỉ cần nhập các triệu chứng hoặc câu hỏi của mình, Doctor AI sẽ phân tích và cung cấp câu trả lời chính xác nhất.")
        st.header("Contact")
        st.write("Bác sĩ online")
        st.write("Email: lapduanviet@gmail.com")
        st.write("Phone: 0918755356")

elif page2 == "Chat":
    if passw !='0' and passw !="":
        display(vector_index, chunks)
    else:
        st.warning("Please update your information")

elif page2 =="Logout":
    st.session_state.clear()
    st.switch_page("main.py")

elif page2 =="Profile":
    st.title("Thông tin cá nhân")
    
    if passw !='0' and passw !="":
        conn = connect_sql()
        cursor = conn.cursor()
        account = cursor.execute("SELECT * FROM account")
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns = ['ID','Name','Age','Email','Phone'])
        n = len(df['ID'])

        Name = ''
        Age = ''
        Email = ''
        Phone = ''
        ID = ''
        if n!=0:
            ID = df['ID'][n-1]
            Age = df['Age'][n-1]
            Email = df['Email'][n-1]
            Phone = df['Phone'][n-1]
            Name = df['Name'][n-1]

        if passw !='0' and passw !="":
        
            col1, col2 = st.columns(2)

            with col1:
                img = "D:/Users/User/Downloads/Unknown_person.jpg"
                st.image(img, width= 250)
            with col2: 
                st.write(f"📝Tên: {Name}")
                st.write(f"📜Tuổi: {Age}")
                st.write(f"📧 Email: {Email}")
                st.write(f"📞 SDT: {Phone}")
 
        col1,col2 = st.columns(2)
        with col1:
            st.header("Lịch hẹn sắp tới 📥")
            conn = sqlite3.connect("chroma.db")
            cursor = conn.cursor()

            ##connect history_logs 
            data = cursor.execute("SELECT * FROM history_logs")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns = ['ID','Email'])
            n = len(df['ID'])
            PatientID = df['ID'][n-1]
                
            #connect appointment
            data = cursor.execute("SELECT * FROM appointment")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns= ['ID', 'DoctorID','PatientID','DATE','Description'])
            loc = df.loc[df['PatientID']==PatientID,['ID','DoctorID','DATE','Description']]
            doctorID = loc['DoctorID']
            n_appoinment = len(doctorID)
            #connect doctor
            data = cursor.execute("SELECT * FROM doctor")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=['ID','Name','Speciality'])
            n = len(doctorID)
            if n_appoinment ==0:
                st.warning("Bạn hiện tại không có lịch hẹn nào")
            else:
                if n==1:
                    doctorID = int(doctorID)
                    loc2 = df.loc[df['ID']==doctorID,['ID','Name','Speciality']]
                
                if n>1:
                    for id in doctorID:
                        loc2 = df.loc[df['ID']==int(id),['ID','Name','Speciality']]

                loc['DoctorName'] = [name for name in loc2['Name']]

                #sap xep lai thu tu cac cot
                new_order = ['ID', 'DoctorID', 'DoctorName','DATE','Description']
                loc_reindex = loc.reindex(columns=new_order)
                loc_reindex = loc_reindex.drop(columns=['DoctorID'])
                st.dataframe(loc_reindex,width=600, height=100)

        with col2:
            st.header("Thay đổi lịch hẹn 📝")
            if 'my_option' not in st.session_state:
                st.session_state.my_option = ""
               
            st.session_state.my_option = st.selectbox(
                        "Options:", 
                        ("Thay đổi lịch hẹn", "Hủy hẹn"), 
                        index=["Thay đổi lịch hẹn", "Hủy hẹn"].index(st.session_state.my_option) if st.session_state.my_option else 0,
                        key='selectbox')
            
            # Hiển thị giá trị của `selectbox` được lưu trữ trong `session_state`
           
            if st.session_state.my_option == "Thay đổi lịch hẹn":
                option_day = st.date_input("Chọn ngày")
                option = st.selectbox("Chọn thời gian:", ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"])
                submit = st.button("Submit")
               
                if submit:

                    #chuyen doi ngay
                    time = option_day.strftime('%A, %B %d, %Y')
                    day = datetime.datetime.strptime(time, '%A, %B %d, %Y').date()

                    #chuyen doi gio
                    time_object = datetime.datetime.strptime(option, '%I:%M %p').time()
                    combine = datetime.datetime.combine(day, time_object)

                    #connect table appointment
                    data = cursor.execute("SELECT * FROM appointment")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns = ['ID','DoctorID','PatientID','DATE','Description'])
                    loc = df.loc[df['PatientID']==PatientID,['DATE']]
                    #lay datetime trong table
                    date = loc['DATE'][0]
                    result = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                   
                    if result == combine:
                        st.warning("Thời gian thay đổi giống với thời gian cũ. Hãy chọn lại !!")
                    else:
                        st.success("Thay đổi lịch hẹn thành công")
                        update_appoinment2(PatientID,combine)

            if st.session_state.my_option == "Hủy hẹn":
                submit = st.button("Submit")
                if submit:
                    st.success("Hủy hẹn thành công")
                    data = cursor.execute("SELECT * FROM appointment")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result, columns = ['ID','DoctorID','PatientID','DATE','Description'])
                    loc = df.loc[df['PatientID']==PatientID,['DATE']]

                    #lay datetime trong table
                    date = loc['DATE'][0]
                    cancel_appointment(PatientID, date)
            
    else:
        st.warning("Please update information")
    
elif page2 =="Appointment":
    conn = connect_sql()
    cursor = conn.cursor()
    data = cursor.execute('SELECT * FROM history_logs')
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns = ['ID','Email'])
    n = len(df['ID'])
    PatientID = df['ID'][n-1]

    appointment(PatientID)

elif page2 =="Search":
    search_drugs()

st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
