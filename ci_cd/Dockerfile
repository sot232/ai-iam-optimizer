# Use an official AWS Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11

# Copy the contents of src directory into the container
COPY src/ ${LAMBDA_TASK_ROOT}

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Change permissions
RUN chmod 644 $(find . -type f)
RUN chmod 755 $(find . -type d)

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]