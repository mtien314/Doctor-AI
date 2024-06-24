import streamlit as st
from streamlit_navigation_bar import st_navbar
from search import search_drugs
from booking_page import appoiment
from chat import display
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader

st.set_page_config(layout="wide")

@st.cache_resource
def load_data3():
    loader = CSVLoader(file_path="PHÒNG KHÁM CHUYÊN GIA- BỆNH VIỆN CHỢ RẪY.csv",encoding="utf8")
    data = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    chunks = splitter.split_documents(data)
    
    embeddings = HuggingFaceEmbeddings()
   
    vector_index = Chroma.from_documents(chunks,embeddings)
    print("Loading data success..")

    return vector_index, chunks

vector_index,chunks = load_data3()



page = st_navbar(["Home", "Chat 🧑‍⚕️", "Search 🔎", "Appoiment 📆"])

if page =="Search 🔎":
    search_drugs()

if page == "Appoiment 📆":
    appoiment()

if page =="Chat 🧑‍⚕️":
    display(vector_index, chunks)

if page =="Home":
    st.header("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
    st.image("chatbot.jpg",output_format="auto")
    st.write("Mô Tả: Đưa sức khỏe của bạn vào tay của công nghệ với Doctor AI - chatbot y tế tiên tiến nhất, hỗ trợ bạn từ việc chẩn đoán ban đầu đến quản lý bệnh mãn tính.")
    st.header("Doctor AI là gì?")
    st.write("Doctor AI là một chatbot y tế thông minh, được thiết kế để cung cấp cho bạn các lời khuyên y tế chính xác và kịp thời. Với sự hỗ trợ của công nghệ AI tiên tiến, Doctor AI có khả năng chẩn đoán các triệu chứng ban đầu, cung cấp thông tin về các bệnh lý và giúp quản lý các bệnh mãn tính.")
    st.image("chatbot2.py")
    st.header("Những Tính Năng Nổi Bật của Doctor AI")
    st.write("+ Chẩn Đoán Ban Đầu: Phân tích các triệu chứng và đưa ra các dự đoán về bệnh lý có thể mắc phải.")
    st.write("+ Thông Tin Y Khoa Đầy Đủ: Cung cấp thông tin chi tiết về các bệnh lý, thuốc và phương pháp điều trị.")
    st.header("Doctor AI Hoạt Động Như Thế Nào?")
    st.write("Doctor AI sử dụng công nghệ AI tiên tiến để phân tích dữ liệu y tế từ người dùng. Bạn chỉ cần nhập các triệu chứng hoặc câu hỏi của mình, Doctor AI sẽ phân tích và cung cấp câu trả lời chính xác nhất.")
