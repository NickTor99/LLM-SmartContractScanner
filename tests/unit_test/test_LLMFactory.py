import unittest
from api_server.core.configuration.llm_factory import LLMFactory
from api_server.core.llm.openai_llm import OpenAILLM
from api_server.core.llm.hf_llm import HFLLM


class TestLLMFactory(unittest.TestCase):

    def test_build_openai_model(self):
        """
        Verifica che venga restituita un'istanza di OpenAILLM per source='openai'.
        """
        config = {
            "source": "openai",
            "model_name": "gpt-4",
            "api_key": "sk-test",
            "base_url": "https://api.openai.com"
        }

        model = LLMFactory.build(config)
        self.assertIsInstance(model, OpenAILLM)

    def test_build_openai_model_missing_baseurl(self):
        """
        Verifica che venga restituita un'istanza di OpenAILLM anche se manca base_url.
        """
        config = {
            "source": "openai",
            "model_name": "gpt-4",
            "api_key": "sk-test"
        }

        model = LLMFactory.build(config)
        self.assertIsInstance(model, OpenAILLM)


    def test_build_openai_model_missing_apikey(self):
        """
        Verifica che venga sollevato un ValueError se manca apikey.
        """
        config = {
            "source": "openai",
            "model_name": "gpt-4",
            "base_url": "https://api.openai.com"
        }

        with self.assertRaises(KeyError) as context:
            LLMFactory.build(config)

    def test_build_huggingface_model(self):
        """
        Verifica che venga restituita un'istanza di HFLLM per source='huggingface'.
        """
        config = {
            "source": "huggingface",
            "model_name": "sshleifer/tiny-gpt2",
        }

        model = LLMFactory.build(config)
        self.assertIsInstance(model, HFLLM)



    def test_build_invalid_source(self):
        """
        Verifica che venga sollevato un ValueError se la source non è supportata.
        """
        config = {
            "source": "invalid",
            "model_name": "something"
        }

        with self.assertRaises(ValueError) as context:
            LLMFactory.build(config)
        self.assertIn("Fonte del modello LLM non supportata", str(context.exception))


if __name__ == "__main__":
    unittest.main()
