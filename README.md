# Azure RAG POC

This project is a Proof of Concept for a Retrieval-Augmented Generation (RAG) application using Azure OpenAI and Azure AI Search.

## Setup

1.  **Prerequisites**: Python 3.13+, `uv` installed.
2.  **Install**:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    uv pip install -e .
    ```
3.  **Environment Variables**: Create a `.env` file with the keys listed in `.env.example` (if provided) or based on the code.

## Usage

Run the Streamlit app:
```bash
streamlit run src/azure_rag_poc/app.py
```
