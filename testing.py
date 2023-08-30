from Recommender import rec_sys
import Scraper.Arxiv as scrape
import pandas as pd


def Pipeline():
    # Scrape
    scrape.source_candidates()
    # RecSys
    rec_sys.run()

    feed = pd.read_csv("Repository/Feed.csv", index_col="Id")
    print(feed.head())


Pipeline()
