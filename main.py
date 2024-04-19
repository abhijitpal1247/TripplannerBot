import os
import uuid

import streamlit as st
from langchain.agents import AgentType
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from streamlit_folium import st_folium
from langchain.agents import load_tools

from chatAgent import OpenAIAgent
from chatCallback import SimpleCallback
from chatTools import PlacesOfInterestTool, RouteRetriever
from utils import get_route_leafmap


st.set_page_config(page_title="Trip-planner Bot using LangChain", page_icon="🦜", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

st.title("Trip-planner Bot (langchain) 🦜⛓️")
st.info(
    "Trip-planner Bot",
    icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me anything about anywhere!"}
    ]

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    openai_api_key = os.environ.get('OPENAI_API_KEY', None)
    if openai_api_key is None:
        raise ValueError("API KEY for OpenAI must be set")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    memory = ConversationSummaryMemory(memory_key="chat_history", llm=llm, max_token_limit=10, verbose=True)
    travel_agent = OpenAIAgent(llm=llm, memory=memory, agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                               verbose=True, callback=SimpleCallback(st_state=st.session_state))
    wiki_tool = load_tools(['wikipedia'], llm=llm)[0]
    travel_agent.add_tool(PlacesOfInterestTool())
    travel_agent.add_tool(RouteRetriever())
    travel_agent.add_tool(wiki_tool)
    st.session_state.chat_engine = travel_agent

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    if 'role' in message.keys():
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if 'geocode_points' in message.keys():
        route = message['geocode_points']
        figure_key = message['figure_key']
        m = get_route_leafmap(route)
        _ = st_folium(m, key=figure_key)

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.make_request(prompt)
            if len(st.session_state.messages) > 1 and 'geocode_points' in st.session_state.messages[-1].keys():
                route = st.session_state.messages[-1]['geocode_points']
                figure_key = str(uuid.uuid4())
                m = get_route_leafmap(route)
                _ = st_folium(m, key=figure_key)
                st.session_state.messages[-1]['figure_key'] = figure_key
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)  # Add response to message history
