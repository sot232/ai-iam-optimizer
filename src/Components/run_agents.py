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
def run_langchain_client(llm: ChatOpenAI, iam_policy: str, code: str, service_category: str = 'lambda') -> dict:
    template = """
    INSTRUCTION: {INSTRUCTION}

    SERVICE CATEGORY: {service_category}

    IAM POLICY:
    {iam_policy}

    CODE:
    {code}
    """

    custom_prompt = PromptTemplate.from_template(template)

    chain = custom_prompt | llm | SimpleJsonOutputParser()

    return chain.invoke({"INSTRUCTION": INSTRUCTION, "service_category": service_category, "iam_policy": iam_policy, "code": code})



