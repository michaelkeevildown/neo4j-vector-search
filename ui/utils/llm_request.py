import json

from openai import OpenAI

from src.utils.env_variables import load_env_variables

env_vars = load_env_variables()

client = OpenAI(api_key=env_vars['OPENAI_API_KEY'])


def call_openai(messages):
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "json_object"}
    )

    llm_response = json.loads(response.choices[0].message.content)
    if 'documents' in llm_response:
        response = [doc['title'] for doc in llm_response['documents']]
    elif 'response' in llm_response:
        response = llm_response['response']

    return response
