"""
Cleaning utilities for the scraped Wuzzuf job listings.
"""

import pandas as pd


def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw scraped jobs dataframe:
    - Drop exact duplicate rows (e.g. from overlapping pagination)
    - Drop rows with a missing title (parsing failures)
    - Reset the index

    Args:
        df (pd.DataFrame): Raw scraped jobs dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["title"])
    df = df.reset_index(drop=True)
    return df


def make_full_urls(df: pd.DataFrame, base_url: str = "https://wuzzuf.net") -> pd.DataFrame:
    """
    Convert relative job links into full, clickable URLs.

    Args:
        df (pd.DataFrame): Dataframe with a 'link' column of relative paths.
        base_url (str): The site's base URL to prepend.

    Returns:
        pd.DataFrame: Dataframe with 'link' converted to full URLs.
    """
    df = df.copy()
    df["link"] = df["link"].apply(
        lambda x: x if (isinstance(x, str) and x.startswith("http")) else f"{base_url}{x}" if isinstance(x, str) else x
    )
    return df
