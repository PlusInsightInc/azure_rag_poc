import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    model_provider="azure_openai",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model=os.getenv("AZURE_OPENAI_EMBEDDINGS_MODEL_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)