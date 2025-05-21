import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    template = """Given the full name {name_of_person}, I want you to find their LinkedIn profile page.
    Your answer should only contain a URL."""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for you to get the LinkedIn Page URL",  # This is what the LLM will use to determine if the tool will be useful for what it is trying to do.
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        {"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]

    return linked_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Gerhard Bekker")
