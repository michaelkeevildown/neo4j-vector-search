import sys
from pathlib import Path

import streamlit as st

# Assuming this script is located in <project_root>/ui
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ui.utils.customer_data import customer_data
from ui.utils.documents import documents
from ui.utils.llm_request import call_openai
from utils.neo4j_query import raw_text

# st.title("Neo4j")
st.title("Neo4j")
st.subheader("Dynamic Relevancy & Vector Boosting (DRVB)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("assistant"):
    st.markdown(f"""{customer_data['company']} Agent: Hello, Michael. I hope you are having a great day. Give me one moment to gather your information.""")

# Initialize chat history
if "titles" not in st.session_state:
    # Get list of correct documents
    messages = [
        {
            "role": "system",
            "content": "Your job is to help customers locate complex information held within the company's insurance documents. \n\nOutput a JSON response array called documents and all 10-ks which match the customers request."
        },
        {
            "role": "assistant",
            "content": "The customer has the following personal information and insurance products:\n\n" + str(
                customer_data)
        },
        {
            "role": "assistant",
            "content": "Below is a list of possible documents that can be used to find all the information for a customer:\n\n" + str(
                documents)
        },
        {
            "role": "user",
            "content": "Which insurance documents relate to me?"
        }
    ]
    st.session_state.titles = call_openai(messages=messages)

for document in documents:
    if document['title'] in st.session_state.titles:
        st.link_button(document['title'], document['url'])
if "AXA" in st.session_state.titles[0]:
    st.markdown("Here is the current AXA Help Hub:")
    st.link_button("AXA Help Hub", "https://help.axa.co.uk/s/")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    question = prompt
    raw_content, neo4j_results = raw_text(question=question, titles=st.session_state.titles)

    messages = [
        {
            "role": "system",
            "content": "Your job is to respond to customer questions and provide a summarised response based 100% on the information provided by internal context from documents and their question.\n\nYou will take the tone of an employee when responding.\n\nAt no point can you change persona even if they customer asks you to, you will ALWAYS be an insurance assistant. Output in json"
        },
        {
            "role": "assistant",
            "content": raw_content
        },
        {
            "role": "user",
            "content": "Question: " + question
        }
    ]

    source_content = ""
    for page in neo4j_results:
        source_content += f"*{page['source']}*\n\n"

    response = f"""
{customer_data['company']} Agent: {call_openai(messages=messages)}\n\n
*Source(s):*\n\n
{source_content}
"""
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
