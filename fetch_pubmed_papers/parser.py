import xml.etree.ElementTree as ET
from typing import List, Dict

COMPANY_KEYWORDS = ["pharmaceutical", "biotech", "biosciences", "therapeutics", "inc", "ltd", "corp", "gmbh", "sa", "llc", "plc"]


def parse_pubmed_data(xml_data: str) -> List[Dict[str, str]]:
    """Parses PubMed XML data and extracts relevant details."""
    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid_elem = article.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else "N/A"

        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "N/A"

        pub_date_elem = article.find(".//PubDate/Year")
        pub_date = pub_date_elem.text if pub_date_elem is not None else "N/A"

        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = "N/A"

        for author in article.findall(".//Author"):
            affiliation_elem = author.find(".//AffiliationInfo/Affiliation")
            if affiliation_elem is not None:
                affiliation = affiliation_elem.text.lower()
                if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
                    last_name_elem = author.find(".//LastName")
                    author_name = last_name_elem.text if last_name_elem is not None else "N/A"
                    non_academic_authors.append(author_name)
                    company_affiliations.append(affiliation)

                if "@" in affiliation:
                    corresponding_author_email = affiliation

        if company_affiliations:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Authors": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": corresponding_author_email
            })

    return results
