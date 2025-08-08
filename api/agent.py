from langchain.agents import create_react_agent, AgentExecutor, Tool, initialize_agent
from langchain import hub
from pydantic import BaseModel
from load_from_gcs_pdf_to_image import pdf_to_text_extractor_tool
from images_to_text import text_extractor_tool
from text_mcq_test import generate_mcq_test
from summary_to_pdf import save_summary_to_pdf
# from load_file_gcs import load_files_from_gcs
from langchain_groq import ChatGroq
from langchain.globals import set_llm_cache
from tools_config import tools
from agent_config import agent_executor
# from routes import app

set_llm_cache(None)  # disables caching

prompt_user = input("Enter your query: ")

# Use invoke() instead of run()
result = agent_executor.invoke({"input": f"{prompt_user} from Homework.pdf in the GCS bucket assignment_agent."})

# Print result
print(result)




