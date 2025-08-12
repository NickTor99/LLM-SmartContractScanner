import unittest
from fastapi.testclient import TestClient
from entrypoint import app  # importa la tua app FastAPI

client = TestClient(app)


class TestSetModelController(unittest.TestCase):

    def _send_request(self, model_name, source, api_key, base_url):
        payload = {
            "model_name": model_name,
            "source": source,
            "api_key": api_key,
            "base_url": base_url
        }
        return client.post("/api/setmodel", json=payload)

    def test_SCo1(self):
        r = self._send_request("gpt-4", "openai", "my_api_key", "https://api.openai.com")
        self.assertEqual(r.status_code, 200)

    def test_SCo2(self):
        r = self._send_request("", "openai", "my_api_key", "https://api.openai.com")
        self.assertEqual(r.status_code, 422)

    def test_SCo3(self):
        r = self._send_request("gpt-4", "not_valid_source", "my_api_key", "https://api.openai.com")
        self.assertEqual(r.status_code, 422)

    def test_SCo4(self):
        r = self._send_request("gpt-4", "openai", "", "https://api.openai.com")
        self.assertEqual(r.status_code, 422)

    def test_SCo5(self):
        r = self._send_request("bert-base", "huggingface", "", "")
        self.assertEqual(r.status_code, 200)

    def test_SCo6(self):
        r = self._send_request("bert-base", "huggingface", "", "https://huggingface.co")
        self.assertEqual(r.status_code, 422)

    def test_SCo7(self):
        r = self._send_request("bert-base", "huggingface", "my_api_key", "")
        self.assertEqual(r.status_code, 422)


if __name__ == "__main__":
    unittest.main()
