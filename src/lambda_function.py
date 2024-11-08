import logging
import json
import argparse

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from Components.run_agents import run_langchain_client, set_llm
from Components.helper import format_code, sanitize_input, build_return_json

# Logging configuration
MSG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT, level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    is_valid_input, is_valid_message = sanitize_input(event)
    if not is_valid_input:
        return is_valid_message

    code = format_code(event.get('code'))
    if not code[0]:
        return code[1]
    
    llm = set_llm()

    result = run_langchain_client(
        llm=llm,
        iam_policy=event.get('iam_policy'),
        code=code[1],
        service_category=event.get('service_category', None),
        additional_instructions=event.get('additional_instructions', None),
        readme=event.get('readme', None)
    )
    
    return build_return_json(200, result)


if __name__ == "__main__":
    # for command line use
    parser = argparse.ArgumentParser(description="Run lambda_handler with a JSON event.")
    parser.add_argument('--event', type=str, required=True, help="Event data as JSON string")

    args = parser.parse_args()

    # Load event JSON from the command line argument
    event = json.loads(args.event)

    # Run the lambda_handler with the provided event
    print(lambda_handler(event, None))