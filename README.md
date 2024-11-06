ai-iam-optimizer
=================

*This project is currently in research phase. It is not ready for production use yet.*

*This is created for a research project to optimize the IAM policy for a given lambda function or fargate task.*

This is currently deployed in AWS as a lambda function, and it is going to be available via an API endpoint.

Please do not abuse this API endpoint.

If you like this project, please buy me a coffee :)

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=DK7UYMMK7FPZN&no_recurring=1&currency_code=USD)

## Parameters
- `iam_policy` (required): The IAM policy to optimize.
- `code` (required): The code to optimize the IAM policy for. Can be a string or a dictionary with file names and file contents.
- `service_category` (optional): The service category to optimize the IAM policy for. Can be either `lambda` or `fargate`. Defaults to `lambda`.
- `readme` (optional): The README file to optimize the IAM policy for.
- `additional_instructions` (optional): Additional instructions to optimize the IAM policy for.
## API
URL: https://...

### API Example
```bash
curl -X POST https://{your-api-endpoint} -H "Content-Type: application/json" -d '{"iam_policy": "...", "code": "...", "service_category": "lambda"}'
```

```bash
curl -X POST https://{your-api-endpoint} -H "Content-Type: application/json" -d '{"iam_policy": "...", "code": {"file1.py": "...", "file2.py": "..."}, "service_category": "fargate"}'
```

## License
This project is licensed under the MIT License.

## Authors
- **Primary Contact:**
  - Jeong Kim
    - [@sot232](https://github.com/sot232)
    - [@dalmad2](https://github.com/dalmad2)
    - [jeong@wrench.ai](mailto:jeong@wrench.ai)
    - [linkedin](https://www.linkedin.com/in/jeongkimbyu/)
