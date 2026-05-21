import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from tool_definitions import get_tools_for_agent_oneshot
from agent_initializer import initialize_agent
import asyncio

load_dotenv()

SHOPPER_AGENT_PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'prompts', 'ShopperAgentPrompt.txt')
with open(SHOPPER_AGENT_PROMPT_PATH, 'r', encoding='utf-8') as file:
    SHOPPER_AGENT_PROMPT = file.read()

project_endpoint = os.environ["FOUNDRY_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

# Create function tools for cora agent
functions = asyncio.run(get_tools_for_agent_oneshot("cora"))

initialize_agent(
    project_client=project_client,
    model=os.environ["gpt_deployment"],
    name="cora",
    description="Zava Shopper Assistant Agent",
    instructions=SHOPPER_AGENT_PROMPT,
    tools=functions
)
