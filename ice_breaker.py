from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

import os
from dotenv import load_dotenv


def ice_break_with(name: str) -> None:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    summary_template = """
        Given the LinkedIn information {information} about a person, I want you to create:
        1. A short summary
        2. Three interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # temperature=0 means that it will not be creative
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # Basically an API call happening here
    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/gerhard-bekker-a6867b14a/",
        mock=True,
    )
    result = chain.invoke(input={"information": linkedin_data})

    print(result.content)


if __name__ == "__main__":
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    print("Ice Breaker Enter")

    ice_break_with(name="Gerhard Bekker ENGYS")
