import streamlit as st
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain


def display(vector_index, chunks): 
    st.secrets["GOOGLE_API_KEY"]
   
    genai.configure(api_key=GOOGLE_API_KEY)
    llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY)

    if "messages" not in st.session_state.keys(): # Initialize the chat message history
        st.session_state.messages = [
            {"role": "assistant", "content": "Xin chào ! Tôi có thể giúp gì cho bạn 🧑‍⚕️ ?."}
        ]
    
    if "question_count" not in st.session_state:  # Initialize the question count
        st.session_state.question_count = 0

    if question := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.question_count += 1 
        
    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])  
    
    if st.session_state.messages[-1]["role"] != "assistant":    
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                
                if  st.session_state.question_count <=5  :
                    prompt_template = """
                    Giao tiếp như 1 người bạn.
                    Bạn là 1 bác sĩ online.
                    Tư vấn bệnh cho bệnh nhân.
                    Kê đơn thuốc kháng sinh cho bệnh nhân và đưa ra lời khuyên.
                    Đề xuất đi khám bác sĩ hoặc đi bệnh viện nếu bệnh nặng.
                    Đề xuất danh sách các bác sĩ liên quan đến bệnh có trong dữ liệu.
                    Nếu câu hỏi không liên quan đến y tế, bệnh hãy trả lời:
                    "Xin lỗi, tôi chỉ là 1 chuyên gia tư vấn sức khỏe online."
                    Context:\n {context}?\n
                    Question: \n {question}\n
                    Answer:
                    """
                    context = vector_index.similarity_search(question, k=3) 
                    prompt = PromptTemplate(template = prompt_template, input_variables = ["", "question"])
                    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",google_api_key = GOOGLE_API_KEY, temperature=0.3)
                    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
                    response = chain({"input_documents": chunks, "question": question}, return_only_outputs=True)
                    st.write(response["output_text"])
                    message = {"role": "assistant", "content": response["output_text"]}
                    st.session_state.messages.append(message) # Add response to message history

                else:
                   
                    st.write("Bạn vui lòng thanh toán để được tư vấn tiếp.")
                   
                    st.write("Link thanh toán: https://buy.stripe.com/test_fZecPd1H73zz7jqfYZ")
                    st.write("Lưu ý: từ câu hỏi thứ 5, phí 50k/câu. Từ câu thứ 10, phí 100k/ câu")
                    st.write("Bạn có muốn tiếp tục nữa không ?")
                    col_1,col_2 = st.columns(2)
                    k = 0
                    with col_1:
                        y = st.button("Yes")
                        if y==True:
                            k = 1

                            
                    with col_2:
                        n = st.button("No")
                        if n==True:
                            k = 2
                    if k==1:
                        st.write("Thật tuyệt !!....")
                        st.session_state.question_count = 0
                        st.empty() 
                    if k==2:
                        st.write("Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi !!")
                           
                    


