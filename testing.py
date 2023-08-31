import ScholarlyRecommender as sr


def Pipeline():
    # Scrape

    c = sr.source_candidates(as_df=True)
    r = sr.get_recommendations(
        data=c,
        as_df=True,
    )

    sr.get_feed(
        data=r,
        to_path="ScholarlyRecommender/Newsletter/html/4TestUserFeed.html",
    )
