import ScholarlyRecommender as sr
import pandas as pd
import numpy as np
import test_mail as tm


def Pipeline():
    # Scrape

    c = sr.source_candidates(as_df=True)
    r = sr.get_recommendations(
        data=c,
        as_df=True,
    )

    sr.get_feed(
        data=r,
        to_path="ScholarlyRecommender/Newsletter/html/TestUserFeed.html",
    )
    tm.send_email("ScholarlyRecommender/Newsletter/html/TestUserFeed.html")
