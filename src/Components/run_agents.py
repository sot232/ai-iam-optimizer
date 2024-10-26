from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import traceable

from Config.constants import (
    IAM_OPTIMIZER_INSTRUCTION,
    DESCRIPTION_EXTRACTOR_INSTRUCTION,
    IAM_POLICY_VALIDATOR_INSTRUCTION,
    CODE_VALIDATOR_INSTRUCTION,
    DEFAUL_MODEL, OPENAI_API_KEY
)

def set_llm(openai_api_key: str = OPENAI_API_KEY, model: str = DEFAUL_MODEL):
    llm = ChatOpenAI(openai_api_key=openai_api_key, model=model, max_tokens=None,
        timeout=None, max_retries=2, )
    return llm


def set_template(
        readme: str = None,
        additional_instructions: str = None,
        **kwargs
):
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

    for key, value in kwargs.items():
        template += f"\n{key}:\n{value}"

    return template


@traceable
def run_langchain_client(
        llm: ChatOpenAI,
        iam_policy: str,
        code: str,
        service_category: str = 'lambda',
        readme: str = None,
        additional_instructions: str = None
) -> dict:
    '''
    Run the langchain client

    This agent is responsible for:
    - Optimizing the IAM policy based on the code and additional resources
    '''
    template = set_template(
        readme=readme,
        additional_instructions=additional_instructions
    )

    custom_prompt = PromptTemplate.from_template(template)

    chain = custom_prompt | llm | SimpleJsonOutputParser()

    input_data = {"INSTRUCTION": IAM_OPTIMIZER_INSTRUCTION, "service_category": service_category, "iam_policy": iam_policy, "code": code}
    if readme:
        input_data["readme"] = readme

    if additional_instructions:
        input_data["additional_instructions"] = additional_instructions

    return chain.invoke(input_data)


@traceable
def run_validation_agent(
        llm: ChatOpenAI,
        iam_policy: str,
        code: str,
        service_category: str = 'lambda',
        readme: str = None,
        additional_instructions: str = None
) -> dict:
    '''
    Run the validation agent

    The goal of this agent is
    to minimize the risk of the code not working as expected
    without user intervention.
    We want to automate the process of identifying potential issues.
    
    Steps:
    1. Extract the description of the service from the code and additional resources including the readme
    2. Validate the IAM policy against the service description
    3. Validate the code against the service description
    '''

    # extract the description of the service
    description_template = set_template(
        readme=readme,
        additional_instructions=additional_instructions
    )

    description_prompt = PromptTemplate.from_template(description_template)
    description_chain = description_prompt | llm | SimpleJsonOutputParser()

    description_chain_input_data = {"INSTRUCTION": DESCRIPTION_EXTRACTOR_INSTRUCTION, "service_category": service_category, "code": code, "iam_policy": iam_policy}
    if readme:
        description_chain_input_data["readme"] = readme

    if additional_instructions:
        description_chain_input_data["additional_instructions"] = additional_instructions

    description_result = description_chain.invoke(description_chain_input_data)

    # validate the IAM policy against the service description
    iam_policy_validator_template = set_template(
        readme=readme,
        additional_instructions=additional_instructions
    )

    iam_policy_validator_prompt = PromptTemplate.from_template(iam_policy_validator_template)
    iam_policy_validator_chain = iam_policy_validator_prompt | llm | SimpleJsonOutputParser()

    iam_policy_validator_input_data = {"INSTRUCTION": IAM_POLICY_VALIDATOR_INSTRUCTION, "service_category": service_category, "iam_policy": iam_policy, "description": description_result}
    if readme:
        iam_policy_validator_input_data["readme"] = readme

    if additional_instructions:
        iam_policy_validator_input_data["additional_instructions"] = additional_instructions

    iam_policy_validator_result = iam_policy_validator_chain.invoke(iam_policy_validator_input_data)

    # validate the code against the service description
    code_validator_template = set_template(
        readme=readme,
        additional_instructions=additional_instructions
    )

    code_validator_prompt = PromptTemplate.from_template(code_validator_template)
    code_validator_chain = code_validator_prompt | llm | SimpleJsonOutputParser()

    code_validator_input_data = {"INSTRUCTION": CODE_VALIDATOR_INSTRUCTION, "service_category": service_category, "code": code, "description": description_result}
    if readme:
        code_validator_input_data["readme"] = readme

    if additional_instructions:
        code_validator_input_data["additional_instructions"] = additional_instructions  

    code_validator_result = code_validator_chain.invoke(code_validator_input_data)

    return {
        "iam_policy_validator_result": iam_policy_validator_result,
        "code_validator_result": code_validator_result
    }
