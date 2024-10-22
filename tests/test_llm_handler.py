import unittest
from api.api import openai_llm_call, qlikllm_call

class TestLLMHandler(unittest.TestCase):

    def test_openai_llm_call(self):
        prompt = "What's the capital of France?"
        response = openai_llm_call(prompt)
        self.assertIsInstance(response, str)  
        self.assertIn("Paris", response) 

    # def test_qlikllm_call(self):
    #     prompt = "Explain data science in simple terms."
    #     response = qlikllm_call(prompt)
    #     self.assertIsInstance(response, str)
    #     self.assertGreater(len(response), 10)

if __name__ == '__main__':
    unittest.main()
