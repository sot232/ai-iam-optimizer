ai-iam-optimizer
=================

*This is created for a research project to optimize the IAM policy for a given lambda function or fargate task.*

This is currently deployed in AWS as a lambda function, and available as a REST API.

## Parameters

- `iam_policy`: The IAM policy to optimize.
- `code`: The code to optimize the IAM policy for. Can be a string or a dictionary with file names and file contents.
- `service_category`: The service category to optimize the IAM policy for. Can be either `lambda` or `fargate`. Defaults to `lambda`.

## Example

```bash
curl -X POST https://{your-api-endpoint} -H "Content-Type: application/json" -d '{"iam_policy": "...", "code": "...", "service_category": "lambda"}'
```

```bash
curl -X POST https://{your-api-endpoint} -H "Content-Type: application/json" -d '{"iam_policy": "...", "code": {"file1.py": "...", "file2.py": "..."}, "service_category": "fargate"}'
```

## Authors
- **Primary Contact:**
  - Jeong Kim
    - [@sot232](https://github.com/sot232)
    - [@dalmad2](https://github.com/dalmad2)
    - [jeong@wrench.ai](mailto:jeong@wrench.ai)
    - [linkedin](https://www.linkedin.com/in/jeongkimbyu/)
