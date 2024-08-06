
from langchain.vectorstores import FAISS
from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import TextLoader
#import { TextLoader } from "langchain/document_loaders/fs/text"
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain import LLMChain
import os
from webscrappingnotebook import get_txt

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

# Set the default value for the google_api_key environment variable
os.environ.setdefault("google_api_key", "AIzaSyDs51FtbuJrLx7wvVgZsX_K1UGnq8AL3ok")
# Now you can use the os.environ dictionary to access the value
llm = GooglePalm(google_api_key=os.environ["google_api_key"], temperature=0.1)
#llm = GooglePalm(google_api_key=os.environ["AIzaSyDs51FtbuJrLx7wvVgZsX_K1UGnq8AL3ok"], temperature=0.1)
# # Initialize instructor embeddings using the Hugging Face model
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vectordb_file_path = "faiss_index"

def create_vector_db():
    # Load data from FAQ sheet
    file_path = "recursive_txt.txt"

    if os.path.exists(file_path):
        # The file exists, so use the TextLoader directly
        print('file found!')
        loader = TextLoader(file_path)
    else:
        # The file doesn't exist, so call a function to handle this case
        print('file not found, calling get_txt function')
        txt_file = get_txt()
        loader = TextLoader(txt_file)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    all_splits = text_splitter.split_documents(data)
    # Create a FAISS instance for vector database from 'data'
    vectordb = FAISS.from_documents(documents=all_splits,
                                    embedding=instructor_embeddings)

    # Save vector database locally
    vectordb.save_local(vectordb_file_path)


def get_qa_chain():
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)

    # Create a retriever for querying the vector database
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """You are an artificial intelligence assistant working for Univeristy of Texas at Arlington. You are asked to answer questions about the university. The assistant gives helpful, detailed, and polite answers to the user's questions. If you do not know the answer to a question simply respond with I don't know instead of guessing.

    {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["question"])

    chain = LLMChain(prompt=PROMPT, llm=llm, verbose=True)

    return chain
