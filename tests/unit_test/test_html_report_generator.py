import os
import unittest
from unittest.mock import mock_open, patch
from report.html_report_generator import HTMLReportGenerator


class TestHTMLReportGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = HTMLReportGenerator(os.path.join(os.path.dirname(__file__), "output_report"))

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_valid_report(self, mock_file):
        """
        RG1: Lista ben formata, percorso valido, nome non specificato
        """
        data = [{"vulnerability": "Arbitrary delete", "analysis": """### Step 3 – Final Evaluation:

**Determine Vulnerability Status:**
The contract is **vulnerable** to the "arbitrary_delete" vulnerability. The deletion of the application is unrestricted, allowing any caller to delete the contract and potentially causing loss of state and funds.

### Step 4 – Remediation:

**Vulnerable code snippet:**
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0)
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```

**Secure code snippet:**
To fix this, add an authorization check to ensure only the creator (or another authorized address) can delete the application. For example:
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0),
    Txn.sender() == Global.creator_address()  # Only creator can delete
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```
"""}]
        self.generator.generate(data, file_path="../system_test/test_contracts/valid.teal", report_name=None)
        written_content = mock_file().write.call_args[0][0] # mock_file è un file fittizio deve viene scritto il risultato

        #Controllo che il file HTML abbia tutti i campi che ci aspettiamo
        self.assertIn("Arbitrary delete", written_content)
        self.assertIn("Vulnerable Code Snippet", written_content)
        self.assertIn("Remediation Snippet", written_content)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_empty_list(self, mock_file):
        """
        RG2: Lista vuota, percorso valido, nome non specificato
        """
        data = []
        self.generator.generate(data, file_path="out/test.teal", report_name=None)
        written_content = mock_file().write.call_args[0][0]
        self.assertIn("No vulnerabilities found in the contract.", written_content)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_malformed_data(self, mock_file):
        """
        RG3: Lista malformata
        """
        malformed_data = [{"invalid_key": "no vuln"}]
        with self.assertRaises(Exception):
            self.generator.generate(malformed_data, file_path="out/test.teal", report_name=None)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_partial_data(self, mock_file):
        """
        RG4: Lista con dati parziali, percorso valido, nome valido
        """
        # Non sono presenti riferimenti allo snippet affetto dalla vulnerabilità o eventuali rimedi ad essa
        partial_data = [{"vulnerability": "Arbitrary delete", "analysis": """### Step 3 – Final Evaluation:

**Determine Vulnerability Status:**
The contract is **vulnerable** to the "arbitrary_delete" vulnerability. The deletion of the application is unrestricted, allowing any caller to delete the contract and potentially causing loss of state and funds.

### Step 4 – Remediation:
"""}]
        self.generator.generate(partial_data, file_path="out/test.teal", report_name="partial")
        written_content = mock_file().write.call_args[0][0]

        #Controllo che il file HTML abbia tutti i campi che ci aspettiamo
        self.assertIn("Arbitrary delete", written_content)
        self.assertIn("N/A", written_content)



    def test_generate_empty_path(self):
        """
        RG5: Percorso vuoto, nome valido
        """
        output_path = self.generator.make_outpath(report_name="fromname", file_path="")
        self.assertEqual(output_path, os.path.join(os.path.dirname(__file__), "output_report\\fromname.html"))



    @patch("builtins.open", side_effect=OSError("Invalid path"))
    def test_generate_invalid_path(self, mock_file):
        """
        RG6: Percorso non valido
        """
        valid_data = [{"vulnerability": "Arbitrary delete", "analysis": """### Step 3 – Final Evaluation:

**Determine Vulnerability Status:**
The contract is **vulnerable** to the "arbitrary_delete" vulnerability. The deletion of the application is unrestricted, allowing any caller to delete the contract and potentially causing loss of state and funds.

### Step 4 – Remediation:

**Vulnerable code snippet:**
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0)
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```

**Secure code snippet:**
To fix this, add an authorization check to ensure only the creator (or another authorized address) can delete the application. For example:
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0),
    Txn.sender() == Global.creator_address()  # Only creator can delete
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```
"""}]
        with self.assertRaises(OSError):
            self.generator.generate(valid_data, file_path="invalid///path.teal", report_name="fail")

    def test_generate_existing_report_name(self):
        """
        RG7: Nome report già esistente (simulato)
        """
        output_path = self.generator.make_outpath(report_name="test", file_path="")
        self.assertEqual(output_path, os.path.join(os.path.dirname(__file__), "output_report\\test3.html"))


    def test_generate_invalid_report_name(self):
        """
        RG8: Lista ben formata, percorso valido, nome non valido
        """
        data = [{"vulnerability": "Arbitrary delete", "analysis": """### Step 3 – Final Evaluation:

**Determine Vulnerability Status:**
The contract is **vulnerable** to the "arbitrary_delete" vulnerability. The deletion of the application is unrestricted, allowing any caller to delete the contract and potentially causing loss of state and funds.

### Step 4 – Remediation:

**Vulnerable code snippet:**
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0)
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```

**Secure code snippet:**
To fix this, add an authorization check to ensure only the creator (or another authorized address) can delete the application. For example:
```pyteal
is_delete_application = And(
    Txn.on_completion() == OnComplete.DeleteApplication,
    Txn.application_id() != Int(0),
    Txn.sender() == Global.creator_address()  # Only creator can delete
)

[is_delete_application, Seq([
    Log(Bytes("Delete Application")),
    Return(Int(1))
])]
```
"""}]
        with self.assertRaises(Exception):
            self.generator.generate(data, file_path="../system_test/test_contracts/valid.teal", report_name="<report>")



if __name__ == "__main__":
    unittest.main()
