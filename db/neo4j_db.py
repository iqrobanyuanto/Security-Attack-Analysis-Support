from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os

from autogen.agentchat.contrib.graph_rag.neo4j_graph_query_engine import Neo4jGraphQueryEngine

query_engine = Neo4jGraphQueryEngine(
    username="neo4j",  # Change if you reset username
    password="iqrobanyuanto",  # Change if you reset password
    host="neo4j://localhost",  # Change
    port=7687,  # if needed
    llm=OpenAI(model="gpt-4o", temperature=0.0, api_key=os.getenv("OPENAI_API_KEY")),  # Default, no need to specify
    embedding=OpenAIEmbedding(model_name="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")),  # except you want to use a different model
    database="neo4j",  # Change if you want to store the graphh in your custom database
)