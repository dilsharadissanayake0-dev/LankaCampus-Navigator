import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# 1. Documents Load කිරීම
def load_documents(data_path="data/ugc_docs"):
    loader = DirectoryLoader(data_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Total Documents Loaded: {len(documents)}")
    return documents

# 2. Chunks වලට වෙන් කිරීම (Chunking Strategy)
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total Chunks Created: {len(chunks)}")
    return chunks

# 3. Vector Database (ChromaDB) සාදා Save කිරීම
def create_vector_store(chunks, db_path="./chroma_db"):
    # නොමිලේ භාවිත කළ හැකි FastEmbed model එකක්
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print(f"Vector Database created successfully at '{db_path}'!")
    return vectorstore

if __name__ == "__main__":
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)
        create_vector_store(chunks)
    else:
        print("No documents found in data/ugc_docs folder!")