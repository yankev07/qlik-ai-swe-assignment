import os
import unittest
from app import app  
from dotenv import load_dotenv
from fastapi.testclient import TestClient

client = TestClient(app)

load_dotenv()

class TestIntegration(unittest.TestCase):
    CUSTOM_AUTH_TOKEN = os.getenv('API_AUTHENTICATION_TOKEN')

    def post_with_auth(self, url, json_data):
        headers = {
            "Authorization": f"Bearer {self.CUSTOM_AUTH_TOKEN}"
        }
        return client.post(url, json=json_data, headers=headers)

    def test_process_prompts_success_openai(self):
        request_data = {
            "prompt1": "What is the capital of France?",
            "prompt2": "Where is Paris?"
        }
        response = self.post_with_auth("/aisweassignment/openai/maxsimilarity", request_data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(json_response["similar"])
        self.assertIn("Paris", json_response["response"])

    def test_process_prompts_failure_openai(self):
        request_data = {
            "prompt1": "What is the capital of France?",
            "prompt2": "Let's go for a walk."
        }
        response = self.post_with_auth("/aisweassignment/openai/maxsimilarity", request_data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertFalse(json_response["similar"])

    def test_process_prompts_invalid_model(self):
        request_data = {
            "prompt1": "What is the capital of France?",
            "prompt2": "Where is Paris?"
        }
        response = self.post_with_auth("/aisweassignment/invalid_model/maxsimilarity", request_data)
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn("Invalid model", json_response["detail"])

    def test_process_prompts_invalid_similarity_type(self):
        request_data = {
            "prompt1": "What is the capital of France?",
            "prompt2": "Where is Paris?"
        }
        response = self.post_with_auth("/aisweassignment/openai/invalid_similarity", request_data)
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn("Invalid similarity type", json_response["detail"])

if __name__ == '__main__':
    unittest.main()
