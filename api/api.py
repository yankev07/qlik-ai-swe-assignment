import os
import torch
import openai
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
QLIK_LLM_API_KEY = os.getenv('QLIK_LLM_API_KEY')
# print(f'API Key: {OPENAI_API_KEY}')


model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def calculate_similarity(prompt1, prompt2):
    try:
        inputs1 = tokenizer(prompt1, return_tensors="pt", padding=True, truncation=True)
        inputs2 = tokenizer(prompt2, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embedding1 = model(**inputs1).last_hidden_state.mean(dim=1)
            embedding2 = model(**inputs2).last_hidden_state.mean(dim=1)
            
        cosine_similarity = torch.nn.functional.cosine_similarity(embedding1, embedding2)
        return cosine_similarity.item()
    except Exception as e:
        print(f'Error: {e}')
        return str(e)


def openai_llm_call(prompt):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        assistant_reply = response['choices'][0]['message']['content']
        print(f'Assistant Reply: {assistant_reply}')
        return assistant_reply
    except Exception as e:
        print(f'Error: {e}')
        return str(e)


def qlikllm_call(prompt):
    try:
        api_key = QLIK_LLM_API_KEY

        url = 'https://6ynua95x15ix2yi.us.qlik-stage.com/api/v1/ai-platform/actions/generate-chat-completions'

        # Payload data
        data = {
            "model": "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            message_content = response_data['choices'][0]['message']['content']
            return(message_content)
        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print(f'Error: {e}')
        return str(e)


def sanitize_prompt(prompt, max_length: int = 200):
    banned_words = [
        'violence', 'terrorism', 'anti-Semitic', 'Islamophobic', 'drug', 'cocaine', 'heroin', 'meth', 'addict', 'weed', 'marijuana', 'LSD', 'bomb', 'explosive', 'kidnap', 'hijack', 'cartel', 'gang', 'suicide', 'threaten', 'insult', 'demean', 'stalk', 'mock'
    ]
    
    def censor(text):
        for word in banned_words:
            text = text.replace(word, '*' * len(word))  
        return text

    try:
        if len(prompt) > max_length:
            print(f"Error: The prompt exceeds the maximum length of {max_length} characters.")
            return None
        elif any(banned_word in prompt for banned_word in banned_words):
            print("Profanity detected! Sanitizing prompt...")
            sanitized_prompt = censor(prompt)
            return sanitized_prompt
        else:
            return prompt
    except Exception as e:
        return f"Error: {e}"


def sanitize_output(response):
    banned_words = [
        'violence', 'terrorism', 'anti-Semitic', 'Islamophobic', 'drug', 'cocaine', 'heroin', 'meth', 'addict', 'weed', 'marijuana', 'LSD', 'bomb', 'explosive', 'kidnap', 'hijack', 'cartel', 'gang', 'suicide', 'threaten', 'insult', 'demean', 'stalk', 'mock'
    ]
    
    def censor(text):
        for word in banned_words:
            text = text.replace(word, '*' * len(word))  
        return text

    try:
        if any(banned_word in response for banned_word in banned_words):
            print("Profanity detected! Sanitizing prompt...")
            sanitized_prompt = censor(response)
            return sanitized_prompt
        else:
            return response
    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
    response = qlikllm_call("How many people live in the United States?")
    print(response)
    # prompt = "This contains some hate speech and violence."
    # sanitized_prompt = sanitize_prompt(prompt, max_length=200)
    # print(sanitized_prompt)