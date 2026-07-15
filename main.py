"""
End-to-end scraping pipeline for Wuzzuf job listings.

Run with:
    python main.py

Output is saved to data/wuzzuf_jobs.csv
"""

import os

from src.cleaning import clean_jobs, make_full_urls
from src.scraper import scrape_jobs


def main():
    print("Scraping Wuzzuf job listings (Egypt)...")
    df = scrape_jobs(country="Egypt", max_pages=5)

    print(f"Raw scraped rows: {len(df)}")

    df = clean_jobs(df)
    df = make_full_urls(df)

    print(f"Cleaned rows: {len(df)}")
    print(df.head())

    os.makedirs("data", exist_ok=True)
    output_path = "data/wuzzuf_jobs.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    main()
