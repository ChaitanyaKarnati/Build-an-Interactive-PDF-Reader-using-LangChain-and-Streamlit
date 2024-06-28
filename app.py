
# Task 1: Import the Libraries
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader, PdfWriter
from tempfile import NamedTemporaryFile
import base64
from htmlTemplates import expander_css, css, bot_template, user_template
st.set_page_config(layout="wide", page_title="Interactive Reader", page_icon=":books:")

# Task 4: Process the Input PDF
def process_file(doc):

    model_name = "thenlper/gte-small"
    model_kwargs = {'device': 'mps'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)  
    
    pdfsearch = Chroma.from_documents(doc, embeddings)

    chain = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.3), 
        retriever=pdfsearch.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True)
    return chain


# Task 6: Method for Handling User Input
def handle_userinput(query):

    response = st.session_state.conversation({"question": query, 'chat_history':st.session_state.chat_history}, return_only_outputs=True)
    st.session_state.chat_history += [(query, response['answer'])]

    st.session_state.N = list(response['source_documents'][0])[1][1]['page']
    
    
    for i, message in enumerate(st.session_state.chat_history): 
         st.session_state.expander1.write(user_template.replace("{{MSG}}", message[0]), unsafe_allow_html=True)
         st.session_state.expander1.write(bot_template.replace("{{MSG}}", message[1]), unsafe_allow_html=True)


def main():
    pass
    
    # Task 3: Create Web-page Layout
    load_dotenv()
    
    
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "N" not in st.session_state:
        st.session_state.N = 0
   
    st.session_state.col1, st.session_state.col2 = st.columns([1, 1])
    st.session_state.col1.header("Interactive Reader :books:")
    user_question = st.session_state.col1.text_input("Ask a question on the contents of the uploaded PDF:")
    st.session_state.expander1 = st.session_state.col1.expander('Your Chat', expanded=True)
    st.session_state.col1.markdown(expander_css, unsafe_allow_html=True) 

    # Task 5: Load and Process the PDF 
    st.session_state.col1.subheader("Your documents")
    st.session_state.pdf_doc = st.session_state.col1.file_uploader("Upload your PDF here and click on 'Process'")

    if st.session_state.col1.button("Process", key='a'):
        with st.spinner("Processing"):
            if st.session_state.pdf_doc is not None:
                with NamedTemporaryFile(suffix="pdf") as temp:
                    temp.write(st.session_state.pdf_doc.getvalue())
                    temp.seek(0)
                    loader = PyPDFLoader(temp.name)
                    pdf = loader.load()
                    st.session_state.conversation = process_file(pdf)
                    st.session_state.col1.markdown("Done processing. You may now ask a question.")


    
    # Task 7: Handle Query and Display Pages
    if user_question:
        handle_userinput(user_question)
        with NamedTemporaryFile(suffix="pdf") as temp:
            temp.write(st.session_state.pdf_doc.getvalue())
            temp.seek(0)
            reader = PdfReader(temp.name)
            
            pdf_writer = PdfWriter()
            start = max(st.session_state.N-2, 0)
            end = min(st.session_state.N+2, len(reader.pages)-1) 
            while start <= end:
                pdf_writer.add_page(reader.pages[start])
                start+=1
            with NamedTemporaryFile(suffix="pdf") as temp2:
                pdf_writer.write(temp2.name)
                with open(temp2.name, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

                    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}#page={3}"\
                        width="100%" height="900" type="application/pdf frameborder="0"></iframe>'
                
                    st.session_state.col2.markdown(pdf_display, unsafe_allow_html=True)
       



if __name__ == '__main__':
    main()

