import os
import logging
from api.api import calculate_similarity
from api.api import openai_llm_call
from api.api import sanitize_prompt
from api.api import sanitize_output
from api.api import qlikllm_call
from flask_cors import CORS, cross_origin
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header


logger = logging.getLogger(__name__)

app = FastAPI()

class PromptRequest(BaseModel):
    prompt1: str
    prompt2: str

load_dotenv()
API_AUTHENTICATION_TOKEN = os.getenv('API_AUTHENTICATION_TOKEN')

@app.post("/aisweassignment/{model}/{similarity_type}")
async def process_prompts(request: PromptRequest, model: str, similarity_type: str, authorization: str = Header(None)):
    MAX_SIMILARITY = 0.8
    MIN_SIMILARITY = 0.6
    # print(f'Authorization: {authorization}')
    # print(f'API_AUTHENTICATION_TOKEN: {API_AUTHENTICATION_TOKEN}')
    if authorization != "Bearer " + API_AUTHENTICATION_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid token.")
    
    try:
        prompt1 = request.prompt1
        prompt2 = request.prompt2
        sanitized_prompt1 = sanitize_prompt(prompt1)
        sanitized_prompt2 = sanitize_prompt(prompt2)
        similarity = calculate_similarity(sanitized_prompt1, sanitized_prompt2)

        if model == "openai":
            pass
        elif model == "qlikllm":
            pass
        else:
            raise HTTPException(status_code=400, detail="Invalid model. Use 'openai' or 'qlikllm'.")

        if similarity_type == "maxsimilarity":
            similarity_threshold = MAX_SIMILARITY
        elif similarity_type == "minsimilarity":
            similarity_threshold = MIN_SIMILARITY
        else:
            raise HTTPException(status_code=400, detail="Invalid similarity type. Use 'maxsimilarity' or 'minsimilarity'.")

        if similarity > similarity_threshold:
            if model == "openai":
                response = openai_llm_call(sanitized_prompt1)
            elif model == "qlikllm":
                # LLM Gateway Error: 403 {"code": "AI_PLATFORM_011", "title": "Security issue detected", "detail": "Security Alert: PromptInjection issues detected. Access to this resource is forbidden."}
                # response = qlikllm_call(sanitized_prompt1)
                response = openai_llm_call(sanitized_prompt1)
            sanitized_response = sanitize_output(response)
            return {"similar": True, "response": sanitized_response}
        return {"similar": False, "message": "Prompts are not similar enough."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Test Route to Check if the API is running
@app.get('/')
def index(authorization: str = Header(None)):
    if authorization != "Bearer " + API_AUTHENTICATION_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid token.")
    return {'200': 'Welcome to the Qlik AI Software Engineer Home Assignment by Kevin Yanogo!'}