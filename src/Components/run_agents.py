from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import traceable

from Config.constants import INSTRUCTION, DEFAUL_MODEL, OPENAI_API_KEY


def set_llm(openai_api_key: str = OPENAI_API_KEY, model: str = DEFAUL_MODEL):
    llm = ChatOpenAI(openai_api_key=openai_api_key, model=model, max_tokens=None,
        timeout=None, max_retries=2, )
    return llm


@traceable
def run_langchain_client(llm: ChatOpenAI, iam_policy: str, code: str, service_category: str = 'lambda', readme: str = None, additional_instructions: str = None) -> dict:
    template = "INSTRUCTION: {INSTRUCTION}"

    if additional_instructions:
        template += "\nADDITIONAL INSTRUCTIONS:\n{additional_instructions}"

    template += """
    SERVICE CATEGORY: {service_category}

    IAM POLICY:
    {iam_policy}

    CODE:
    {code}
    """

    if readme:
        template += "\nREADME:\n{readme}"

    custom_prompt = PromptTemplate.from_template(template)

    chain = custom_prompt | llm | SimpleJsonOutputParser()

    input_data = {"INSTRUCTION": INSTRUCTION, "service_category": service_category, "iam_policy": iam_policy, "code": code}
    if readme:
        input_data["readme"] = readme

    if additional_instructions:
        input_data["additional_instructions"] = additional_instructions

    return chain.invoke(input_data)



