import json


def format_code(code) -> tuple[bool, str]:
    '''
    Format the code to a string
    Accepts a string or a dictionary with file names and file contents
    '''
    if isinstance(code, str):
        return True, code
    elif isinstance(code, dict):
        output = ""
        for key, value in code.items():
            output += f"Code File Name: {key}\nCode File Content: ```{value}```\n\n"
        return True, output
    else:
        raise False, build_return_json(400, "Invalid code type")
    

def build_return_json(
    code, message
    ) -> dict:
    '''
    Build the return json for the lambda function
    '''
    response_body = {
        'message': message
    }
    
    #  need the headers for the security reason
    return {
        'statusCode': code,
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'strict-transport-security': 'max-age=63072000; includeSubdomains; preload',
            'content-security-policy': "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
            'x-content-type-options': 'nosniff',
            'x-frame-options': 'DENY',
            'x-xss-protection': '1; mode=block'
        }
    }


def sanitize_input(event) -> tuple[bool, str]:
    '''
    Sanitize the input to ensure the required fields are present
    '''
    if not event.get('iam_policy'):
        return False, build_return_json(400, "IAM policy is required")
    if not event.get('code'):
        return False, build_return_json(400, "Code is required")
    return True, ""
