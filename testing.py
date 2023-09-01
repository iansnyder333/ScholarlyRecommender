import ScholarlyRecommender as sr
import pandas as pd
import numpy as np


# Example of how to use the recommender system in a pipeline
# This is useful for testing and debugging, along with quick execution if you don't want to use the webapp.
# If you run Pipeline(), it will generate a feed of 5 papers based on whatever calibration is currently in the repository.
# You also must modify the queries.py file to include the categories you want to search for. or manually enter them in the function call.
def Pipeline():
    candidates = sr.source_candidates(queries=None, as_df=True, prev_days=7)
    recommendations = sr.get_recommendations(
        data=candidates,
        labels=None,
        size=5,
        to_path=None,
        as_df=True,
    )
    sr.get_feed(
        data=recommendations,
        email=False,
        to_path="ScholarlyRecommender/Newsletter/html/Feed.html",
    )
    print(
        "Feed Generated, it is saved to ScholarlyRecommender/Newsletter/html/Feed.html"
    )
