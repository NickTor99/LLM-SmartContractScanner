import unittest
from src.llm.openai_llm import OpenAILLM  # cambia con il path corretto
from openai import OpenAI, AuthenticationError, APIConnectionError, BadRequestError
from openai import OpenAIError

class TestOpenAILLM(unittest.TestCase):
    def setUp(self):
        self.valid_api_key = "sk-36dc60b2590248549d81a309aaf3f912"
        self.valid_base_url = "https://api.deepseek.com"
        self.valid_model = "deepseek-chat"

    def test_generate_success(self):
        model = OpenAILLM(api_key=self.valid_api_key, base_url=self.valid_base_url, model_name=self.valid_model)
        prompt = "What is the capital of France?"
        response = model.generate(prompt)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_generate_invalid_apikey(self):
        model = OpenAILLM(api_key="invalid", base_url=self.valid_base_url, model_name=self.valid_model)
        with self.assertRaises(AuthenticationError):
            print(model.generate("test"))

    def test_generate_invalid_modelname(self):
        model = OpenAILLM(api_key=self.valid_api_key, base_url=self.valid_base_url, model_name="invalid-model")
        with self.assertRaises(BadRequestError) as context:
            model.generate("test")

    def test_generate_invalid_url(self):
        model = OpenAILLM(api_key=self.valid_api_key, base_url="https://invalid.url", model_name=self.valid_model)
        with self.assertRaises(APIConnectionError) as context:
            model.generate("test")

    def test_generate_long_prompt(self):
        model = OpenAILLM(api_key=self.valid_api_key, base_url=self.valid_base_url, model_name=self.valid_model)
        long_prompt = "token " * 130000
        with self.assertRaises(BadRequestError) as context:
            model.generate(long_prompt)