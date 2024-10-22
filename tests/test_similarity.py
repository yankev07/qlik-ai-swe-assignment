import unittest
from api.api import calculate_similarity

class TestSimilarity(unittest.TestCase):

    def test_calculate_similarity_high(self):
        prompt1 = "How is the weather today?"
        prompt2 = "What's the weather like today?"
        similarity = calculate_similarity(prompt1, prompt2)
        self.assertGreater(similarity, 0.7)  

    def test_calculate_similarity_low(self):
        prompt1 = "How is the weather today?"
        prompt2 = "I am passionate about machine learning."
        similarity = calculate_similarity(prompt1, prompt2)
        self.assertLess(similarity, 0.5)  

    def test_calculate_similarity_exact_match(self):
        prompt1 = "This is a test prompt."
        prompt2 = "This is a test prompt."
        similarity = calculate_similarity(prompt1, prompt2)
        self.assertEqual(similarity, 1.0)  

    def test_calculate_similarity_empty_input(self):
        prompt1 = ""
        prompt2 = ""
        similarity = calculate_similarity(prompt1, prompt2)
        self.assertEqual(similarity, 0.0)  

if __name__ == '__main__':
    unittest.main()
