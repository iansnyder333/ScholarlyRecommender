from ScholarlyRecommender.Recommender import rec_sys
import ScholarlyRecommender.Scraper.Arxiv as scrape
import ScholarlyRecommender.Newsletter.feed as feed
import pandas as pd


def Pipeline():
    # Scrape
    scrape.source_candidates()
    # RecSys
    rec_sys.evaluate()
    feed.build_html_feed(feed.clean_feed("ScholarlyRecommender/Repository/Feed.csv"))
    # feed = pd.read_csv("Repository/Feed.csv", index_col="Id")
    # print(feed.head())


Pipeline()
