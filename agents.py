import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from autogen import Agent, AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
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

user = UserProxyAgent(
    name="user",
    system_message="You are the users.",
    human_input_mode="ALWAYS",
    code_execution_config={
        "use_docker": False,
    },
)

task_master = AssistantAgent(
    name="Task_Master",
    system_message="your job is to create an understandable, comprhensive and detailed task",
    llm_config={
        "config_list": config["config_list"]
    },
    human_input_mode="NEVER",
)

poa_agent_1 = AssistantAgent(
    name="PoA_Agent_1",
    system_message="You are an expert in cybersecurity, your task is to analyze the PoA based on the given project requirements.",
    llm_config={
        "config_list": config["config_list"]
    },
    human_input_mode="NEVER",
)

poa_agent_2 = AssistantAgent(
    name="PoA_Agent_2",
    system_message="You are an expert in cybersecurity, your task is to analyze the PoA based on the given project requirements.",
    llm_config={
        "config_list": config["config_list"]
    },
    human_input_mode="NEVER",
)

sentence_transformer_ef = SentenceTransformer("all-mpnet-base-v2").encode
client = QdrantClient(url="https://c8edc979-935b-4327-951a-1590a78b6e4a.us-east4-0.gcp.cloud.qdrant.io", api_key=os.getenv("QDRANT_API_KEY"))

ragproxyagent = RetrieveUserProxyAgent(
    name='RAG_Agent',
    human_input_mode="ALWAYS",
    retrieve_config={
        "task": "default",
        "docs_path": [
          #"Ansari et al. - 2022 - STORE Security Threat Oriented Requirements Engineering Methodology.pdf",
          #"PoA Guideline.pdf"
        ],  # change this to your own path, such as https://raw.githubusercontent.com/ag2ai/ag2/main/README.md
        # "chunk_token_size": 10000,
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

def bsaa_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
    """Define a customized speaker selection function.
    A recommended way is to define a transition for each speaker in the groupchat.

    Returns:
        Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
    """
    messages = groupchat.messages

    # We'll start with a transition to the planner
    if len(messages) <= 1:
        return task_master
    
    elif last_speaker is user:
        if "APPROVED" in messages[-2]["content"]:
            return poa_agent_1
        else:
            return task_master
    
    # elif last_speaker is ragproxyagent:
    #     return task_master
    
    elif last_speaker is task_master:
        return user

    elif last_speaker is poa_agent_1:
        return poa_agent_2

    elif last_speaker is poa_agent_2:
        return user

    else:
        return "auto"

poaGroup = GroupChat(
    agents=[user ,ragproxyagent, task_master, poa_agent_1 ,poa_agent_2],
    speaker_selection_method=bsaa_speaker_selection_func,
    messages=[],
    max_round=20,
)

chatManager = GroupChatManager(
    groupchat=poaGroup,
    system_message="You are the chat manager.",
)
