from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()


GROQ_API_KEY=os.environ.get('GROQ_API_KEY')


os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()


docsearch = FAISS.load_local(
    folder_path="faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True  
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":2})

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])


question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)