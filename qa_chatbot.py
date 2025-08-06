"""
Simple Langchain Streamlit App with Groq
A beginner friendly version focusing on core concepts
"""

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
import os
from langchain_core.prompts import ChatPromptTemplate

## page config
st.set_page_config(page_title="Simple Langchain chatbot with Groq",page_icon="🎉")
## Title

st.title("Simple Langchain Chat with Groq")
st.markdown("Learn Langchain basics with Groq's ultra-fast inference!")

with st.sidebar:
    st.header("settings")
    ## API Key

    api_key=st.text_input("GROQ API Key",type="password",help="GET FREE API KEY at console.groq.com")

    # Model Selection

    model_name=st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile","deepseek-r1-distill-llama-70b"],
        index=0
    )
    # clear button
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

# Initialize Chat history
if "messages" not in st.session_state:
    st.session_state.messages=[]

## Initialize LLM
@st.cache_resource
def get_chain(api_key,model_name):
    if not api_key:
        return None
    # Initialize Chat Groq
    llm=ChatGroq(groq_api_key=api_key,model_name=model_name,
             temperature=0.7,streaming=True)
    
    # Create Prompt Template
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are a helpful assistant powered by Groq. Answer clearly and concisely"),
        ("user","{question}")

    ])

    ## create chain
    chain=prompt| llm| StrOutputParser()
    return chain
## get chain

chain=get_chain(api_key,model_name)

if not chain:
    st.warning("Please enter your Groq API Key in the side bar to start chatting!")
    st.markdown("[Get your free API Key here](https://console.groq.com)")

else:
    ## Display the chat message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    ## Chat input
    if question:=st.chat_input("Ask me anything"):
        ## Add user message to session state
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)
        
        # Generate Response
        with st.chat_message("assistant"):
            message_placeholder=st.empty()
            full_response=""

            try:
                # Streamlit response from GROQ
                for chunk in chain.stream({"question":question}):
                    full_response+=chunk
                    message_placeholder.markdown(full_response +" ")
                    message_placeholder.markdown(full_response)

                    # Add to history
                st.session_state.messages.append({"role":"assistant","content":full_response})
            except Exception as e:
                st.error(f"Error:{str(e)}")
