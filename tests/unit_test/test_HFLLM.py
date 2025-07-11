import unittest
from src.llm.hf_llm import HFLLM  # importa qui la tua classe se ha un nome modulo diverso

class TestHFLLM(unittest.TestCase):

    def test_init_invalid_model(self):
        with self.assertRaises(RuntimeError) as context:
            HFLLM(model_name="non-existent-model-xyz")
        self.assertIn("Errore nel caricamento del modello", str(context.exception))

    def test_init_success(self):
        model = HFLLM(model_name="sshleifer/tiny-gpt2", device="cpu")  # modello leggero per test
        self.assertIsNotNone(model.generator)

    def test_generate_valid_prompt(self):
        model = HFLLM(model_name="sshleifer/tiny-gpt2", device="cpu")
        prompt = "What is a smart contract?"
        response = model.generate(prompt)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_generate_long_prompt(self):
        model = HFLLM(model_name="sshleifer/tiny-gpt2", device="cpu")
        long_prompt = "Smart contract logic. " * 1000  # Crea un prompt molto lungo
        with self.assertRaises(Exception):
            model.generate(long_prompt)

    def test_generate_empty_prompt(self):
        model = HFLLM(model_name="sshleifer/tiny-gpt2", device="cpu")
        prompt = ""
        response = model.generate(prompt)
        self.assertIsInstance(response, str)


if __name__ == "__main__":
    unittest.main()
