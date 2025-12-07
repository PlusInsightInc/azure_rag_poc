import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import AzureSearch
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

def load_documents(data_dir="data"):
    """Loads documents from the specified directory."""
    loader = DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

def setup_vectorstore(documents=None, index_name="rag-poc-index"):
    """Sets up the Azure AI Search vector store."""
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_MODEL_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    vector_store_address = os.getenv("AZURE_SEARCHAI_ENDPOINT")
    vector_store_password = os.getenv("AZURE_SEARCHAI_API_KEY")

    vector_store = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    if documents:
        vector_store.add_documents(documents=documents)
    
    return vector_store

def get_rag_chain(vector_store):
    """Creates the RAG chain."""
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0,
    )

    retriever = vector_store.as_retriever(search_type="similarity")

    # Custom prompt
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible. 
    Always say "thanks for asking!" at the end of the answer. 
    
    {context}
    
    Question: {question}
    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain

if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")
    
    print("Setting up vector store...")
    vector_store = setup_vectorstore(docs)
    print("Vector store setup complete.")
    
    print("Creating RAG chain...")
    chain = get_rag_chain(vector_store)
    
    query = "What is Azure AI Search?"
    print(f"Query: {query}")
    result = chain.invoke({"query": query})
    print(f"Answer: {result['result']}")
