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

    response = workflow.invoke({'messages':[HumanMessage(content=userinput)]},config=config)

    ai_message = response['messages'][1].content

    st.session_state['messagehistory'].append({'role': 'assistant', 'message': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)