from langchain.agents import create_react_agent, AgentExecutor, Tool, initialize_agent
from langchain import hub
# from load_file_gcs import load_files_from_gcs
from langchain_groq import ChatGroq
from langchain.globals import set_llm_cache
from tools_config import tools
set_llm_cache(None)  # disables caching

prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  # or llama3-8b-8192 / gemma-7b-it
    api_key="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"
)

# Create the agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True 
)