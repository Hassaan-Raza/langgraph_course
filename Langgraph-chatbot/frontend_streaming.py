import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage

config = {'configurable':{'thread_id':'thread-1'}}

if 'messagehistory' not in st.session_state:
    st.session_state['messagehistory'] = []

messagehistory = []



for message in st.session_state ['messagehistory']:
    with st.chat_message(message['role']):
        st.text(message['message'])

userinput = st.chat_input('Type here')

if userinput:

    st.session_state['messagehistory'].append({'role':'user','message':userinput})
    with st.chat_message('user'):
        st.text(userinput)




    with st.chat_message('assistant'):
        ai_message = st.write(message_chunk.content for message_chunk, metadata in workflow.stream(
            {'messages':[HumanMessage(content=userinput)]},
            config=config,
            stream_mode='messages'
        ))
    st.session_state['messagehistory'].append({'role': 'assistant', 'message': ai_message})