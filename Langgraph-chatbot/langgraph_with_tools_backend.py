import os
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

search_tool = DuckDuckGoSearchRun(region="us-en")

llm = ChatOpenAI(
    model="meta-llama/llama-3.2-3b-instruct",  # Example model, adjust as needed
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),  # Get key from environment
)

@tool
def calculator(a:float,b:float,op:str)->dict:
    """Performs a basic arithmetic operation on two numbers.
    Supported operations: add,sub,mul,div"""

    try:
        if op == "add":
            result = a+b
        elif op == "sub":
            result = a-b
        elif op == "mul":
            result = a*b
        elif op == "div":
            if b == 0:
                return {"error":"Division by zero not allowed"}
            else:
                result = a / b
        else:
            return {"error":"Invalid operation"}
        return {'a':a,'b':b,'op':op,"result":result}
    except Exception as e:
        return {"error":str(e)}

tools = [search_tool,calculator]
llm_with_tools = llm.bind_tools(tools)

def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

tool_node = ToolNode(tools)
# Rest of the code remains the same
checkpoint = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_node('tools',tool_node)
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools','chat_node')
graph.add_edge('chat_node', END)
workflow = graph.compile(checkpointer=checkpoint)