import asyncio
import datetime
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

load_dotenv()

# From .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FABRIC_USER_TAPESTRY_ID = os.getenv("FABRIC_USER_TAPESTRY_ID")
FABRIC_AUTHORIZATION_HEADER_VALUE = "Bearer " + os.getenv("FABRIC_BEARER_TOKEN")

CHROME_USER_DATA_DIR = os.getenv("CHROME_USER_DATA_DIR")
CHROME_PROFILE_DIR = os.getenv("CHROME_PROFILE_DIR")

# Constants
FABRIC_API_URL = "https://api.onfabric.io/api/v1"
FABRIC_OPENAPI_URL = f"{FABRIC_API_URL}/openapi.json"
AGENT_MAX_STEPS = 100
OPENAI_LLM_MODEL = "gpt-5"


async def main():
    # Create configuration dictionary
    config = {
        "mcpServers": {
            "browser-use": {
                "command": "uvx",
                "args": [
                    "browser-use[cli]",
                    "--user-data-dir",
                    CHROME_USER_DATA_DIR,
                    "--profile-directory",
                    CHROME_PROFILE_DIR,
                    "--mcp",
                ],
                "env": {
                    "BROWSER_USE_HEADLESS": "false",
                    "OPENAI_API_KEY": OPENAI_API_KEY,
                },
            },
            "fabric": {
                "command": "npx",
                "args": [
                    "-y",
                    "@tyk-technologies/api-to-mcp",
                    "--spec",
                    FABRIC_OPENAPI_URL,
                ],
                "env": {
                    "OPENAPI_OVERLAY_PATHS": "",  # Override needed as the tool is apparently injecting some demo data
                    "TARGET_API_BASE_URL": FABRIC_API_URL,
                    "MCP_WHITELIST_OPERATIONS": "GET:/tapestries/{tapestry_id}/summaries,POST:/tapestries/{tapestry_id}/summaries/search",
                    "HEADER_AUTHORIZATION": FABRIC_AUTHORIZATION_HEADER_VALUE,
                },
            },
        }
    }

    client = MCPClient(config)

    llm = ChatOpenAI(model=OPENAI_LLM_MODEL)

    system_prompt = f"""
    Use Fabric to get information about my recent activities. Available providers: google. Tapestry ID: {FABRIC_USER_TAPESTRY_ID}.

    Use DuckDuckGo in browser-use to search the web.
    Use browser-use to navigate to web pages and click on buttons when needed.

    Current date and time is {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.
    """

    additional_instructions = """
    Always use the search_summaries_tapestries__tapestry_id__summaries_search_post tool to ask questions about my online activity. Use natural language for the query property of the body. For example, use 'What did the user watch on YouTube last week?' as the query.
    """

    # Create agent with the client
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=AGENT_MAX_STEPS,
        system_prompt=system_prompt,
        additional_instructions=additional_instructions,
    )

    # Run the query
    result = await agent.run(
        "Based on the interests I expressed in the last month, open the three best fitting GitHub repositories for me to contribute to.",
    )
    print(f"\nResult: {result}")


if __name__ == "__main__":
    asyncio.run(main())
