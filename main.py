from agents import assistant, ragproxyagent
import dotenv

def main():
    dotenv.load_dotenv()
    assistant.reset()

    user_input = input("Please enter your question: ")
    qa_problem = user_input
    chat_results = ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem=qa_problem)
    print(chat_results)

if __name__ == "__main__":
    main()