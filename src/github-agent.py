from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.components.agents import Agent
from haystack_integrations.tools.mcp import MCPTool, StdioServerInfo
from haystack.utils import Secret

import os

GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

github_mcp_server = StdioServerInfo(
        ## TODO: Add correct params for the Github MCP Server (official or legacy)
        command = "docker",
        args = ["run",
          "-i",
          "--rm",
          "-e",
          "GITHUB_PERSONAL_ACCESS_TOKEN",
          "ghcr.io/github/github-mcp-server"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN":  GITHUB_PERSONAL_ACCESS_TOKEN, # DO NOT ADD IT TO YOUR COMMIT
            }
    )

print("MCP server is created")

## TODO: Create your tools here:
get_issue = MCPTool(name="get_issue", server_info=github_mcp_server)
create_issue = MCPTool(name="create_issue", server_info=github_mcp_server)
search_issues = MCPTool(name="search_issues", server_info=github_mcp_server)
search_repositories = MCPTool(name="search_repositories", server_info=github_mcp_server)
get_file_contents = MCPTool(name="get_file_contents", server_info=github_mcp_server)


tools = [get_issue, create_issue, search_issues, search_repositories, get_file_contents ## TODO: Add tools tool_1, tool_2, tool_3,..
    ]

print("MCP tools are created")

## TODO: Create your Agent here:
agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini", api_key=Secret.from_token(OPENAI_API_KEY)),
    tools=tools,
       system_prompt="""
You are a GitHub Assistant with the following capabilities:
1. get_issue: Retrieve detailed information about a specific GitHub issue by querying the GitHub repository.
2. create_issue: Create a new issue within a GitHub repository, allowing you to specify the issue title, description, labels, and other relevant details.
3. search_issues: Search for issues across GitHub repositories using various search criteria such as keywords, labels, assignees, and more.
4. search_repositories: Search for GitHub repositories based on criteria such as repository name, owner, description, or other attributes.
5. get_file_contents: Retrieve the contents of a specific file from a GitHub repository.
You are capable of assisting with:
* Finding, creating, and managing GitHub issues.
* Searching and retrieving repositories or specific files from repositories.
* Exploring, querying, and analyzing GitHub repository content and issues.
Please utilize these tools to perform any necessary actions based on the user's requests. When interacting with the GitHub API, ensure accuracy and provide detailed information in your responses.
""",
    exit_conditions=["text"],
    max_agent_steps=100)
    
print("Agent created")

## Example query to test your agent
user_input = "Can you find the typos in the README of simonamazzarino/spring-into-haystack and open an issue about how to fix it?"

## (OPTIONAL) Feel free to add other example queries that can be resolved with this Agent

response = agent.run(messages=[ChatMessage.from_user(text=user_input)])

## Print the agent thinking process
print(response)
## Print the final response
print(response["messages"][-1].text)
