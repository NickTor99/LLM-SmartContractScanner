import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
import io
import sys

# Importa le tue funzioni qui (sostituisci con l'import corretto)
from src.utils import map_vulnerability, load_string, merge_vuln, get_valid_filepath

class TestMapVulnerability(unittest.TestCase):
    def test_standard_mappings(self):
        self.assertEqual(map_vulnerability("Arbitrary delete"), "arbitrary_delete")
        self.assertEqual(map_vulnerability("rekey_to"), "Unchecked Rekey to")
        self.assertEqual(map_vulnerability("no vuln"), "Not Vulnerable")

    def test_reverse_mappings(self):
        self.assertEqual(map_vulnerability("arbitrary_delete"), "Arbitrary delete")
        self.assertEqual(map_vulnerability("close_remainder_to"), "Unchecked Close Remainder To")

    def test_edge_cases(self):
        self.assertEqual(map_vulnerability(""), "Unknown")
        self.assertEqual(map_vulnerability(None), "Unknown")
        self.assertEqual(map_vulnerability("non_existent"), "Unknown")

    def test_case_sensitivity(self):
        self.assertEqual(map_vulnerability("UNCHECKED ASSET RECEIVER"), "Unknown")
        self.assertEqual(map_vulnerability("Unchecked_Asset_Receiver"), "Unchecked Asset Receiver")


class TestLoadString(unittest.TestCase):
    @patch('os.path.abspath')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    def test_load_string_success(self, mock_open_file, mock_join, mock_abspath):
        mock_join.return_value = "/fake/path/file.txt"
        mock_abspath.return_value = "/fake/path"

        result = load_string("file.txt")
        self.assertEqual(result, "file content")
        mock_open_file.assert_called_with("/fake/path/file.txt", 'r', encoding='utf-8')

    @patch('os.path.abspath')
    @patch('os.path.join')
    def test_load_string_file_not_found(self, mock_join, mock_abspath):
        mock_join.return_value = "/fake/path/nonexistent.txt"
        mock_abspath.return_value = "/fake/path"

        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                load_string("nonexistent.txt")

    @patch('os.path.abspath')
    @patch('os.path.join')
    def test_load_string_encoding_error(self, mock_join, mock_abspath):
        mock_join.return_value = "/fake/path/file.txt"
        mock_abspath.return_value = "/fake/path"

        with patch('builtins.open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid byte')):
            with self.assertRaises(UnicodeDecodeError):
                load_string("file.txt")


class TestMergeVuln(unittest.TestCase):
    def test_merge_empty_lists(self):
        self.assertEqual(merge_vuln([], []), [])
        self.assertEqual(merge_vuln([], ["A"]), ["A"])
        self.assertEqual(merge_vuln(["A"], []), ["A"])

    def test_merge_no_duplicates(self):
        self.assertEqual(merge_vuln(["A", "B"], ["C"]), ["A", "B", "C"])
        self.assertEqual(merge_vuln(["A"], ["B", "C"]), ["A", "B", "C"])

    def test_merge_with_duplicates(self):
        self.assertEqual(merge_vuln(["A", "B"], ["B", "C"]), ["A", "B", "C"])
        self.assertEqual(merge_vuln(["A", "B", "C"], ["B"]), ["A", "B", "C"])

    def test_merge_preserves_order(self):
        self.assertEqual(merge_vuln(["B", "A"], ["C"]), ["B", "A", "C"])

    def test_merge_different_types(self):
        self.assertEqual(merge_vuln([1, 2], [3]), [1, 2, 3])
        self.assertEqual(merge_vuln(["A"], [1]), ["A", 1])


class TestGetValidFilepath(unittest.TestCase):
    @patch('builtins.input', side_effect=["valid_file.txt"])
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_valid_file(self, mock_isfile, mock_exists, mock_input):
        result = get_valid_filepath()
        self.assertEqual(result, "valid_file.txt")

    @patch('builtins.input', side_effect=["nonexistent.txt", "valid_file.txt"])
    @patch('os.path.exists', side_effect=[False, True])
    @patch('os.path.isfile', side_effect=[True, True])
    def test_retry_after_file_not_found(self, mock_isfile, mock_exists, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = get_valid_filepath()
            self.assertEqual(result, "valid_file.txt")
            self.assertIn("Error: Path not found", fake_out.getvalue())

    @patch('builtins.input', side_effect=["directory/", "valid_file.txt"])
    @patch('os.path.exists', side_effect=[True, True])
    @patch('os.path.isfile', side_effect=[False, True])
    def test_retry_after_directory(self, mock_isfile, mock_exists, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = get_valid_filepath()
            self.assertEqual(result, "valid_file.txt")
            self.assertIn("Error: The path points to a directory", fake_out.getvalue())

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_keyboard_interrupt(self, mock_input):
        with self.assertRaises(KeyboardInterrupt):
            get_valid_filepath()


if __name__ == '__main__':
    unittest.main()
