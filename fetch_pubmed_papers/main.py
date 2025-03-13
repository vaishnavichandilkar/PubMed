import argparse
from fetch_pubmed_papers.pubmed_fetcher import fetch_pubmed_ids, fetch_pubmed_details
from fetch_pubmed_papers.parser import parse_pubmed_data
from fetch_pubmed_papers.writer import save_to_csv


def main() -> None:
    """Main function to fetch and process PubMed papers."""
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers with industry-affiliated authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    try:
        pubmed_ids = fetch_pubmed_ids(args.query)
        if args.debug:
            print(f"Fetched {len(pubmed_ids)} PubMed IDs.")

        xml_data = fetch_pubmed_details(pubmed_ids)
        results = parse_pubmed_data(xml_data)

        if args.file:
            save_to_csv(args.file, results)
            print(f"Results saved to {args.file}")
        else:
            for row in results:
                print(row)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
