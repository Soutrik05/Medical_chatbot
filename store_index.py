from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os


load_dotenv()



extracted_data=load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


docsearch = FAISS.from_documents(
    documents=text_chunks,
    embedding=embeddings
)

docsearch.save_local("faiss_index")