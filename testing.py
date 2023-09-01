import ScholarlyRecommender as sr
import pandas as pd
import numpy as np

# from test_mail import send_email


def Pipeline():
    # Scrape

    c = sr.source_candidates(max_results=500, as_df=True)
    r = sr.get_recommendations(
        data=c,
        as_df=True,
    )

    sr.get_feed(
        data=r,
        email=True,
        to_path="ScholarlyRecommender/Newsletter/html/LargeTestFeed.html",
    )
    # send_email(path="ScholarlyRecommender/Newsletter/html/TestFeed.html")


def short_Pipeline():
    sr.get_feed(
        data="ScholarlyRecommender/Repository/Recommendations.csv",
        to_path="ScholarlyRecommender/Newsletter/html/NewTestFeed.html",
    )


def main_Pipeline(q: list = None, n: int = 5, days: int = 7):
    # Scrape

    c = sr.source_candidates(queries=q, as_df=True, prev_days=days)
    r = sr.get_recommendations(
        data=c,
        size=n,
        as_df=True,
    )

    sr.get_feed(
        data=r,
        to_path="ScholarlyRecommender/Newsletter/html/WebTestFeed.html",
    )
    return "ScholarlyRecommender/Newsletter/html/WebTestFeed.html"
    # send_email(path="ScholarlyRecommender/Newsletter/html/TestFeed.html")
