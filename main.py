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
import os
import sys

st.set_page_config(layout="wide")
os.path.dirname(sys.executable)
@st.cache_resource
def load_data3():
    loader = CSVLoader(file_path="PHÒNG KHÁM CHUYÊN GIA- BỆNH VIỆN CHỢ RẪY.csv",encoding="utf8")
    data = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)

    chunks = splitter.split_documents(data)
    
    embeddings = HuggingFaceEmbeddings(model_name = 'keepitreal/vietnamese-sbert')
   
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
    st.write("Welcome")




