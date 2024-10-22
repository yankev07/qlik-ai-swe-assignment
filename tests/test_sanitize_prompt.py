import unittest
from api.api import sanitize_prompt

class TestSanitizePrompt(unittest.TestCase):

    def test_sanitize_with_profanity(self):
        prompt = "I hate violence."
        sanitized_prompt = sanitize_prompt(prompt)
        self.assertNotIn('hate', sanitized_prompt)
        self.assertNotIn('violence', sanitized_prompt)

    def test_sanitize_without_profanity(self):
        prompt = "I love AI."
        sanitized_prompt = sanitize_prompt(prompt)
        self.assertEqual(sanitized_prompt, prompt)  

    def test_prompt_exceeds_max_length(self):
        long_prompt = "This is a really long prompt to say that the assessment is awesome" * 50
        sanitized_prompt = sanitize_prompt(long_prompt, max_length=100)
        self.assertIsNone(sanitized_prompt)

    def test_prompt_with_special_characters(self):
        prompt = "I @hate#! violence?"
        sanitized_prompt = sanitize_prompt(prompt)
        self.assertNotIn("hate", sanitized_prompt)
        self.assertNotIn("violence", sanitized_prompt)

if __name__ == '__main__':
    unittest.main()
