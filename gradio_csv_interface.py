from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits.csv.base import create_csv_agent
import os
import openai
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import gradio as gr

# "C:\\Users\\Dhiraj Pandit\\Desktop\\Programs\\cleaned_car_data.csv"

# def upload_file(file):
#     file_path = os.path.abspath(file)
#     # print(type(file_path))
#     return file_path

def query_csv(query):
    agent = create_csv_agent(
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        path="C:\\Users\\Dhiraj Pandit\\Desktop\\Programs\\cleaned_car_data.csv",
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True
    )
    print("agent created successfully")
    answer = agent.run(query)
    print("query run successfully")

    return answer

# with gr.Blocks() as demo:
#     file_output = gr.File()
#     upload_button = gr.UploadButton("Click to Upload a File", file_types=["file"], file_count="single", type="filepath")
#     upload_button.upload(upload_file, upload_button, file_output)
#     path = upload_file(file_output)
    
demo = gr.Interface(fn=query_csv, inputs="text", outputs="text")

demo.launch(share=True)