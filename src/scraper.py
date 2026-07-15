"""
Scraping utilities for extracting job listings from Wuzzuf.net.

IMPORTANT: Wuzzuf (like most modern sites) uses CSS-in-JS, so its class
names (e.g. "css-lptxge") are auto-generated and can change without notice
whenever the site is redeployed. If this scraper stops finding results,
the first thing to check is whether these class names have changed —
inspect the page in your browser's DevTools and update SELECTORS below.

Always check a website's robots.txt and Terms of Service before scraping,
and add delays between requests to avoid overloading the server or
getting your IP blocked.
"""

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://wuzzuf.net/search/jobs"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

# CSS selectors observed on Wuzzuf's job search results page.
# These WILL need updating if Wuzzuf changes its frontend build.
SELECTORS = {
    "job_card": ("div", {"class": "css-lptxge"}),
    "title_link": ("a", {"class": "css-o171kl"}),
    "company": ("a", {"class": "css-17s97q8"}),
    "location": ("span", {"class": "css-5wys0k"}),
}


def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch a URL and return a parsed BeautifulSoup object.

    Args:
        url (str): The URL to fetch.

    Returns:
        BeautifulSoup: Parsed HTML content.

    Raises:
        requests.HTTPError: If the request fails.
    """
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_job_cards(soup: BeautifulSoup) -> list:
    """
    Extract job listings from a single search results page.

    Args:
        soup (BeautifulSoup): Parsed HTML of a search results page.

    Returns:
        list[dict]: One dict per job, with keys: title, link, company, location.
                    Fields that couldn't be found are set to None rather than
                    raising an error, so one malformed card doesn't break the
                    whole page.
    """
    tag, attrs = SELECTORS["job_card"]
    cards = soup.find_all(tag, attrs=attrs)

    jobs = []
    for card in cards:
        job = {"title": None, "link": None, "company": None, "location": None}

        tag, attrs = SELECTORS["title_link"]
        title_el = card.find(tag, attrs=attrs)
        if title_el:
            job["title"] = title_el.get_text(strip=True)
            job["link"] = title_el.attrs.get("href")

        tag, attrs = SELECTORS["company"]
        company_el = card.find(tag, attrs=attrs)
        if company_el:
            job["company"] = company_el.get_text(strip=True)

        tag, attrs = SELECTORS["location"]
        location_el = card.find(tag, attrs=attrs)
        if location_el:
            job["location"] = location_el.get_text(strip=True)

        jobs.append(job)

    return jobs


def scrape_jobs(query: str = None, country: str = "Egypt", max_pages: int = 5, delay: float = 1.5) -> pd.DataFrame:
    """
    Scrape multiple pages of Wuzzuf job search results into a DataFrame.

    Args:
        query (str, optional): Search keyword (e.g. "AI Engineer"). If None,
                                browses all jobs without a keyword filter.
        country (str): Country filter. Defaults to "Egypt".
        max_pages (int): Number of result pages to scrape (30 jobs/page on Wuzzuf).
        delay (float): Seconds to wait between requests, to be polite to the server.

    Returns:
        pd.DataFrame: Columns: title, link, company, location.
    """
    all_jobs = []

    for page in range(max_pages):
        start = page * 30
        params = f"start={start}"
        if query:
            params += f"&q={requests.utils.quote(query)}"
        if country:
            params += f"&filters%5Bcountry%5D%5B0%5D={country}"

        url = f"{BASE_URL}?{params}"

        try:
            soup = fetch_page(url)
            jobs = parse_job_cards(soup)
            if not jobs:
                # No more results — stop early
                break
            all_jobs.extend(jobs)
        except requests.HTTPError as e:
            print(f"Request failed on page {page}: {e}")
            break

        time.sleep(delay)

    return pd.DataFrame(all_jobs)
