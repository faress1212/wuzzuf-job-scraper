# Wuzzuf Job Scraper 🕸️

A web scraping project that extracts job listings (title, company, location, and link) from [Wuzzuf.net](https://wuzzuf.net), Egypt's leading online job search platform, using `requests` and `BeautifulSoup`.

## Important: Selectors May Need Updating

Wuzzuf, like most modern websites, uses **CSS-in-JS**, meaning its CSS class names (e.g. `css-lptxge`) are auto-generated at build time and can change whenever the site is redeployed — sometimes without any change to the visible page.

**If this scraper returns zero results:**
1. Open the [search results page](https://wuzzuf.net/search/jobs) in your browser.
2. Right-click a job card → "Inspect" (DevTools).
3. Find the current class names for the job card, title link, company, and location.
4. Update the `SELECTORS` dictionary at the top of `src/scraper.py`.

This is normal scraper maintenance, not a bug in the code logic itself — the parsing logic was tested against mock HTML with the same structure Wuzzuf used at the time this project was built, and works correctly as long as the selectors match the live site.

## Project Overview

- Fetch and parse Wuzzuf job search results pages
- Extract job title, company, location, and application link
- Paginate through multiple pages of results, with polite delays between requests
- Clean the scraped data (deduplicate, drop failed parses, build full URLs)
- Export to CSV for further analysis

## Project Structure

```
wuzzuf-job-scraper/
├── data/                       # Scraped CSV output goes here (gitignored)
├── notebooks/
│   └── wuzzuf_job_scraper.ipynb   # Full walkthrough notebook
├── src/
│   ├── scraper.py              # Fetching & parsing job listings
│   └── cleaning.py             # Deduplication & URL cleanup
├── main.py                     # Runs the full scrape end-to-end
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<faress1212>/wuzzuf-job-scraper.git
cd wuzzuf-job-scraper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the scraper
```bash
python main.py
```

This saves results to `data/wuzzuf_jobs.csv`.

Or explore step-by-step in the notebook:
```bash
jupyter notebook notebooks/wuzzuf_job_scraper.ipynb
```

## Responsible Scraping

- Check [wuzzuf.net/robots.txt](https://wuzzuf.net/robots.txt) and Wuzzuf's Terms of Service before scraping at scale.
- The scraper includes a delay (`time.sleep`) between page requests by default — don't remove this, as hammering a site with rapid requests can get your IP blocked or cause harm to the service.
- This project is for educational/personal data analysis purposes.

## Tech Stack

- Python
- Requests (HTTP requests)
- BeautifulSoup4 (HTML parsing)
- Pandas (data handling)

## License

This project is open source and available under the [MIT License](LICENSE). Note that scraped data belongs to its original source (Wuzzuf/employers) — respect the site's terms of use.
