import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage
import uuid
#*********************************Utility Functions*********************************
def generate_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['messagehistory'] =[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state =  workflow.get_state(config={'configurable':{'thread_id':thread_id}})
    return state.values.get('messages',[])

#*********************************Session Setup*********************************


if 'messagehistory' not in st.session_state:
    st.session_state['messagehistory'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
add_thread(st.session_state['thread_id'])

#*********************************Side bar UI*********************************
st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'message':message.content})
        st.session_state['messagehistory'] = temp_messages

#*********************************Main UI*********************************
for message in st.session_state ['messagehistory']:
    with st.chat_message(message['role']):
        st.text(message['message'])

userinput = st.chat_input('Type here')

if userinput:

    st.session_state['messagehistory'].append({'role':'user','message':userinput})
    with st.chat_message('user'):
        st.text(userinput)
    config = {'configurable': {'thread_id': st.session_state['thread_id']}}
    with st.chat_message('assistant'):
        ai_message = st.write(message_chunk.content for message_chunk, metadata in workflow.stream(
            {'messages':[HumanMessage(content=userinput)]},
            config=config,
            stream_mode='messages'
        ))
    st.session_state['messagehistory'].append({'role': 'assistant', 'message': ai_message})