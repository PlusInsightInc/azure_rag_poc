import streamlit as st
import os
from azure_rag_poc.rag_engine import load_documents, setup_vectorstore, get_rag_chain

st.set_page_config(page_title="Azure RAG Demo", page_icon="🤖")

st.title("Azure RAG Demo with LangChain 🦜🔗")

if "chain" not in st.session_state:
    with st.spinner("Initializing RAG Engine..."):
        # Check if index exists or just load documents every time for this demo
        # For a real app, you'd want to separate ingestion from query
        docs = load_documents()
        vector_store = setup_vectorstore(docs)
        st.session_state.chain = get_rag_chain(vector_store)
    st.success("RAG Engine Initialized!")

query = st.text_input("Ask a question about your documents:")

if query:
    with st.spinner("Thinking..."):
        response = st.session_state.chain.invoke({"query": query})
        st.markdown("### Answer")
        st.write(response["result"])
        
        with st.expander("Source Documents"):
            for i, doc in enumerate(response["source_documents"]):
                st.markdown(f"**Source {i+1}:** {doc.metadata['source']}")
                st.text(doc.page_content[:200] + "...")
