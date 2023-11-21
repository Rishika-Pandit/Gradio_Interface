from pymongo import MongoClient
import json
import ast
import os
import openai
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import gradio as gr

uri = "mongodb+srv://rishika:rishika@test-ai.dnigqvt.mongodb.net/"

def textToMql(cursor,query):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages = [
    {
        "role": "system",
        "content": f"You are a helpful assistant. The following is the document for reference from the given collection by the user {cursor}. Generate a MongoDB query to: {query} and give the filter in JSON format in one line. If there is a projection, provide it in JSON format in the next line (if any specified by the user, else 'Null').In the subsequent line, provide the sorting condition (if any specified by the user) in a single new line. If a sorting condition is given, its contents should be given in a single new line. In the subsequent line, provide the limit (if any specified by the user, else 0). For example:\n\nQ: 'Names of top 'n'(n is a number) restaurants based on filter, projection, sort condition given by user'\n\nA: {{\"column_name\": \"value\"}}\n{{\"projection_name\": 1}}\n[(\"sort_name\", -1)]\n n (value of n, i.e., limit). Note: Don't forget to add '\' in the provided JSON output if there is an apostrophe('). Also, make sure to give the JSON output in double quotes.\nA:"
    }
],
    max_tokens=500,   
    )
    return response.choices[0].message.content

def query_mongodb(query, OpenAI_Key):
    openai.api_key =  OpenAI_Key
    client = MongoClient(uri)
    db = client.sample_restaurants
    coll = db.restaurnats
    cursor = coll.find_one()
    #json string data
    output =textToMql(cursor, query)
    print(output)
    j_filter, j_projection, j_list, limit_str = output.split("\n")

    # Convert limit to integer
    limit = int(limit_str)
    if j_list != "Null":
        j_sort = ast.literal_eval(j_list)
    else: 
        j_sort = None
    # Convert filter to JSON object
    json_object_1 = json.loads(j_filter)
    if j_projection != "Null":
        json_object_2 = json.loads(j_projection)
    else:
        json_object_2 = None

    if json_object_2 != None:
        if j_sort != None:
            cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort)
            if limit>0:
                cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort).limit(limit)
            else: 
                cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort) 
        else:
            if limit>0:
                cursor_ans = coll.find(json_object_1, json_object_2).limit(limit)
            else: 
                cursor_ans = coll.find(json_object_1, json_object_2)
    else:
        cursor_ans = coll.find(json_object_1)

    for doc in cursor_ans:
        return str(doc)
    
demo = gr.Interface(fn=query_mongodb, inputs=["text","text"], outputs="text")

demo.launch()