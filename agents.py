import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

config = {
  "config_list": [
    {
      "api_type": "openai",
      "model": "gpt-4o",
      "api_key": os.getenv("OPENAI_API_KEY")
    }
  ],
}

# Create group chat, and group chat manager

assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    max_consecutive_auto_reply=2,
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config["config_list"]
    },
    human_input_mode="NEVER",
)

sentence_transformer_ef = SentenceTransformer("all-mpnet-base-v2").encode
client = QdrantClient(url="https://c8edc979-935b-4327-951a-1590a78b6e4a.us-east4-0.gcp.cloud.qdrant.io", api_key=os.getenv("QDRANT_API_KEY"))

ragproxyagent = RetrieveUserProxyAgent(
    name='rag_proxy_agent',
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    retrieve_config={
        "task": "default",
        "docs_path": [
          # "Ansari et al. - 2022 - STORE Security Threat Oriented Requirements Engineering Methodology.pdf",
        ],  # change this to your own path, such as https://raw.githubusercontent.com/ag2ai/ag2/main/README.md
        "chunk_token_size": 10000,
        "context_max_tokens": 10000,
        "must_break_at_empty_line": False,
        "model": config["config_list"][0]["model"],
        "db_config": {"client": client},
        "vector_db": "qdrant",  # qdrant database
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection
        "overwrite": True,  # set to True if you want to overwrite an existing collection
        "embedding_function": sentence_transformer_ef,  # If left out fastembed "BAAI/bge-small-en-v1.5" will be used
    },
    code_execution_config=False,
)