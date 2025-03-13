import csv
from typing import List, Dict


def save_to_csv(filename: str, data: List[Dict[str, str]]) -> None:
    """Saves parsed data to a CSV file."""
    if not data:
        print("No results to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
