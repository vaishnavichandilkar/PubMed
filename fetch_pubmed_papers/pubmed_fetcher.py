import requests
import xml.etree.ElementTree as ET
from typing import List

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def fetch_pubmed_ids(query: str, max_results: int = 100) -> List[str]:
    """Fetch PubMed article IDs based on a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml",
        "usehistory": "y"
    }
    response = requests.get(PUBMED_API_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    return [id_elem.text for id_elem in root.findall(".//Id")]


def fetch_pubmed_details(pubmed_ids: List[str]) -> str:
    """Fetch full details for the given PubMed article IDs."""
    if not pubmed_ids:
        return ""

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_API_URL + "efetch.fcgi", params=params)
    response.raise_for_status()
    return response.text
