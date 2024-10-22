# qlik-ai-swe-assignment

## Description
This repository contains a scalable microservice developed in Python as part of the home assignment for the Qlik AI SWE role. The service accepts two prompts, estimates the text similarity measures between them, and then sends one of the prompts to an LLM if they are similar. The sanitizes the input prompts and output responses to ensure safety and includes comprehensive tests.

## Requirements
- Python 3.10 or higher
- Docker


## Setup Instructions
1. Clone the Repository

````markdown
git clone https://github.com/yankev07/qlik-ai-swe-assignment.git
cd qlik-ai-swe-assignment
````

2. Create a Virtual Environment
````markdown
python -m venv qlik-ai-swe-assignment-venv
source qlik-ai-swe-assignment-venv/bin/activate  # On Windows use `qlik-ai-swe-assignment-venv\Scripts\activate`
````

4. Install Dependencies
````markdown
pip install -r requirements.txt
````

6. Include Environment Variables
Credentials and environment variables are stored in a ".env" file which will be provided separately for safety

8. Run the Application
````markdown
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
````

## Running Tests
1. Unit Tests
````markdown
pytest test/test_similarity.py
pytest test/test_llm_handler.py
````

3. Integration Tests
````markdown
pytest test/test_integration.py
````

   
## Deployment
To deploy the microservice using Docker, follow these steps:
1. Build the Docker Image
````markdown
docker build -t qlik-ai-swe-assignment .
````

2. Run the Docker Container
````markdown
docker run -p 8000:8000 qlik-ai-swe-assignment
````

## Try it on the Cloud!
### Cloud API Documentation

- Base URL: https://qlik-ai-swe-assignment-96327188529.us-west1.run.app
- Endpoint: https://qlik-ai-swe-assignment-96327188529.us-west1.run.app/aisweassignment/{model}/{similarity_type}
- Method: POST
- Parameters:
   - model (string): The model to be used for comparison. Options: "openai", "qlikllm"
   - similarity_type (string): The type of similarity to check. Options: "maxsimilarity" for a similarity threshold of 80% and "minsimilarity" for a similarity threshold of 60%
- Request Body (JSON):
````markdown
{
    "prompt1": "This is my first prompt.",
    "prompt2": "This is my second prompt."
}
````
   - prompt1: The first text prompt to compare.
   - prompt2: The second text prompt to compare.
- Headers
   - Authorization: Bearer Token (Provided separately for testing)
- Response
   - 200: If the request is successful and similarity is computed.
````markdown
{
  "similar": true,
  "response": "The response from the chosen model"
}
````
   - 200: If the prompts are not similar enough.
````markdown
{
  "similar": false,
  "message": "Prompts are not similar enough."
}
````
- Example Request
````markdown
curl -X POST "https://qlik-ai-swe-assignment-96327188529.us-west1.run.app/aisweassignment/openai/maxsimilarity" \
     -H "Authorization: <BEARER TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt1": "This is the first prompt.",
           "prompt2": "This is the second prompt."
         }'
````
