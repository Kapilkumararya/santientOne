import os  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_PATH = "vector_db/faiss_index"

def get_embedding_function():
    # Runs locally on CPU/GPU. No API cost.
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def add_to_vector_store(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    
    embeddings = get_embedding_function()
    
    # Check if DB exists to append, otherwise create new
    if os.path.exists(DB_PATH):
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        db.add_texts(chunks)
    else:
        db = FAISS.from_texts(chunks, embeddings)
        
    db.save_local(DB_PATH)
    return len(chunks)

def query_vector_store(query):
    embeddings = get_embedding_function()
    try:
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        # Get top 3 most relevant chunks
        docs = db.similarity_search(query, k=3)
        return "\n\n".join([d.page_content for d in docs])
    except:
        return ""