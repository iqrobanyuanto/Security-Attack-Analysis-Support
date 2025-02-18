from agents.poa_task import chatManager, graph_rag_agent, poa_agent_1, task_master, user, poa_agent_2
import dotenv
from db.neo4j_db import db_conn
from utils.common import log_Info

def main():

    db_conn()
    log_Info("DB Connected")

    dotenv.load_dotenv()
    poa_agent_1.reset()
    chatManager.reset()
    task_master.reset()
    # ragproxyagent.reset()
    graph_rag_agent.reset()
    user.reset()
    poa_agent_2.reset()


    user_input = input("Please enter your question: ")
    inputPrompt = user_input
    # chat_results = ragproxyagent.initiate_chat(chatManager, message=ragproxyagent.message_generator, problem=inputPrompt)
    chat_results = user.initiate_chat(chatManager, message=inputPrompt)
    print(chat_results)

if __name__ == "__main__":
    main()
