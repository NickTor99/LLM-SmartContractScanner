def map_vulnerability(name):
    mapping = {
        "Arbitrary delete": "arbitrary_delete",
        "Arbitrary update": "arbitrary_update",
        "Unchecked Asset Close To": "asset_close_to",
        "Unchecked Close Remainder To": "close_remainder_to",
        "Unchecked Rekey to": "rekey_to",
        "Unchecked Transaction Fee": "transaction_fee",
        "Unchecked Asset Receiver": "Unchecked_Asset_Receiver",
        "Unchecked Payment Receiver": "Unchecked_Payment_Receiver",
        "arbitrary_delete": "Arbitrary delete",
        "arbitrary_update": "Arbitrary update",
        "asset_close_to": "Unchecked Asset Close To",
        "close_remainder_to": "Unchecked Close Remainder To",
        "rekey_to": "Unchecked Rekey to",
        "transaction_fee": "Unchecked Transaction Fee",
        "Unchecked_Asset_Receiver": "Unchecked Asset Receiver",
        "Unchecked_Payment_Receiver": "Unchecked Payment Receiver",
        "no vuln": "Not Vulnerable"
    }

    return mapping.get(name, "Unknown")


def load_string(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def merge_vuln(list1: list, list2: list) -> list:
    for vuln in list2:
        if vuln not in list1:
            list1.append(vuln)
    return list1
