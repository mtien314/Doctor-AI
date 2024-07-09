import streamlit as st
from streamlit_navigation_bar import st_navbar
from search import search_drugs
import streamlit_google_oauth as oauth
import bcrypt
from time import sleep
from check import check_user, find_accountID
from record import update_user_record,update_historylogs

st.set_page_config(page_title="Home", page_icon="🏚️",layout="wide")
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

redirect_uri = st.secretes["edirect_uri"]
def ggAuth():
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri  = redirect_uri 
    )
     
    if login_info:
        user_id,user_email = login_info
        update_user_record(user_id,user_email)
        update_historylogs(user_id,user_email)
        st.success("login success")
        sleep(0.5)
        st.switch_page("pages/page1.py")
    st.session_state.clear()


page = st_navbar(["Home", "Chat 🧑‍⚕️", "Search 🔎", "Appointment 📆", "Login"])
#swich_page = st.session_state.get("page_index",0)

if page =="Search 🔎":
    search_drugs()

if page == "Appointment 📆":
    st.warning("Please login to appointment")

if page =="Chat 🧑‍⚕️":
    st.warning("Please login to chat")
   

if page =="Home":
    st.header("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
    st.image("chatbot.jpg",output_format="auto")
    st.write("Mô Tả: Đưa sức khỏe của bạn vào tay của công nghệ với Doctor AI - chatbot y tế tiên tiến nhất, hỗ trợ bạn từ việc chẩn đoán ban đầu đến quản lý bệnh mãn tính.")
    st.header("Doctor AI là gì?")
    st.write("Doctor AI là một chatbot y tế thông minh, được thiết kế để cung cấp cho bạn các lời khuyên y tế chính xác và kịp thời. Với sự hỗ trợ của công nghệ AI tiên tiến, Doctor AI có khả năng chẩn đoán các triệu chứng ban đầu, cung cấp thông tin về các bệnh lý và giúp quản lý các bệnh mãn tính.")
    st.header("Những Tính Năng Nổi Bật của Doctor AI")
    st.write("+ Chẩn Đoán Ban Đầu: Phân tích các triệu chứng và đưa ra các dự đoán về bệnh lý có thể mắc phải.")
    st.write("+ Thông Tin Y Khoa Đầy Đủ: Cung cấp thông tin chi tiết về các bệnh lý, thuốc và phương pháp điều trị.")
    st.header("Doctor AI Hoạt Động Như Thế Nào?")
    st.write("Doctor AI sử dụng công nghệ AI tiên tiến để phân tích dữ liệu y tế từ người dùng. Bạn chỉ cần nhập các triệu chứng hoặc câu hỏi của mình, Doctor AI sẽ phân tích và cung cấp câu trả lời chính xác nhất.")
    st.header("Contact")
    st.write("Bác sĩ online")
    st.write("Email: lapduanviet@gmail.com")
    st.write("Phone: 0918755356")
if page =="Login":
    #login by gg
    ggAuth()

    #form login
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type = "password")
        #button submit
        submit = st.form_submit_button("login")
    
    #check status
    if password == "" or email == "":
        st.warning("Please login")
    
    else:
        #check account
        actual_pass = check_user(email)
        print("actual_pass:",actual_pass)

        if actual_pass != 0:
            #encode password
            actual = actual_pass
            if bcrypt.checkpw(password.encode(), actual):
                st.success("Login success")
                user_id = find_accountID(email)
                placeholder = st.empty()
                sleep(0.5)
                st.switch_page("pages/page1.py")
            else:
                st.warning("Password/Email incorrect")
                
        else:
            st.warning("Password/Email incorrect")
            
        
st.sidebar.header("Home")
st.sidebar.write("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
