from ScholarlyRecommender.Recommender import rec_sys
import ScholarlyRecommender.Scraper.Arxiv as scrape
import ScholarlyRecommender.Newsletter.feed as feed
import pandas as pd


def Pipeline():
    # Scrape
    scrape.source_candidates(
        to_path="ScholarlyRecommender/Repository/TestCandidates.csv"
    )
    # RecSys
    rec_sys.run(path="ScholarlyRecommender/Repository/TestFeed.csv")
    feed.build_html_feed(
        feed.clean_feed("ScholarlyRecommender/Repository/TestFeed.csv"),
        to_path="ScholarlyRecommender/Newsletter/html/TestFeed.html",
    )
    # feed = pd.read_csv("Repository/Feed.csv", index_col="Id")
    # print(feed.head())


Pipeline()
