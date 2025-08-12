import unittest
from fastapi.testclient import TestClient
from entrypoint import app  # importa la tua app FastAPI

client = TestClient(app)


class TestRunController(unittest.TestCase):

    def _send_request(self, model, source_code, vuln_limit, contract_limit):
        payload = {
            "model": model,
            "source_code": source_code,
            "vuln_limit": vuln_limit,
            "contract_limit": contract_limit
        }
        return client.post("/api/run", json=payload)

    def test_RCo1(self):
        r = self._send_request("gpt-4", "contract A {}", 5, 2)
        self.assertEqual(r.status_code, 200)

    def test_RCo2(self):
        r = self._send_request("", "contract A {}", 5, 2)
        self.assertEqual(r.status_code, 422)

    def test_RCo3(self):
        r = self._send_request("gpt-4", "", 5, 2)
        self.assertEqual(r.status_code, 422)

    def test_RCo4(self):
        r = self._send_request("gpt-4", "codice_non_valido", 5, 2)
        self.assertEqual(r.status_code, 200)

    def test_RCo5(self):
        r = self._send_request("gpt-4", "contract A {}", -1, 2)
        self.assertEqual(r.status_code, 422)

    def test_RCo6(self):
        r = self._send_request("gpt-4", "contract A {}", 0, 2)
        self.assertEqual(r.status_code, 200)

    def test_RCo7(self):
        r = self._send_request("gpt-4", "contract A {}", 5, -1)
        self.assertEqual(r.status_code, 422)

    def test_RCo8(self):
        r = self._send_request("gpt-4", "contract A {}", 5, 0)
        self.assertEqual(r.status_code, 200)

    def test_RCo9(self):
        r = self._send_request("", "", -1, -1)
        self.assertEqual(r.status_code, 422)


if __name__ == "__main__":
    unittest.main()
