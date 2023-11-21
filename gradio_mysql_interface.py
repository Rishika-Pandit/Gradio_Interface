
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import os
import openai
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import gradio as gr

# uri = "mysql://sql12658396:d5lPvJy515@sql12.freesqldatabase.com:3306/sql12658396"
# query = "give me top 10 user names, phone number who are cusotmers based on number of orders"

def query_mysql(query,uri):
    db = SQLDatabase.from_uri(uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0,model="gpt-4"))

    agent_executor = create_sql_agent(
        llm=ChatOpenAI(temperature=0, max_tokens=750,model="gpt-3.5-turbo-16k"),
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    answer = agent_executor.run(query)
    return answer

demo = gr.Interface(fn=query_mysql, inputs=["text","text"], outputs="text")

demo.launch()