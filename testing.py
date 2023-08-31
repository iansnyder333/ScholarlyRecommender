import ScholarlyRecommender as sr
import pandas as pd
import numpy as np

# from test_mail import send_email


def Pipeline():
    # Scrape

    c = sr.source_candidates(as_df=True)
    r = sr.get_recommendations(
        data=c,
        as_df=True,
    )

    sr.get_feed(
        data=r,
        to_path="ScholarlyRecommender/Newsletter/html/NewTestFeed.html",
    )
    # send_email(path="ScholarlyRecommender/Newsletter/html/TestFeed.html")


def short_Pipeline():
    sr.get_feed(
        data="ScholarlyRecommender/Repository/Recommendations.csv",
        to_path="ScholarlyRecommender/Newsletter/html/NewTestFeed.html",
    )


short_Pipeline()
