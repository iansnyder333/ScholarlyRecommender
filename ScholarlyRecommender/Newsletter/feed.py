import pandas as pd
import numpy as np
from datetime import datetime


def clean_feed(path: str = "ScholarlyRecommender/Repository/Feed.csv"):
    df = pd.read_csv(path)
    df["Published"] = pd.to_datetime(df["Published"]).dt.strftime("%Y-%m-%d")
    df["Abstract"] = df["Abstract"].str[:150] + "..."
    # df.to_csv("Repository/CleanFeed.csv", index=False)
    return df


# df = clean_feed()


def build_html_feed(
    df: pd.DataFrame, to_path: str = "ScholarlyRecommender/Newsletter/html/Feed.html"
):
    # df = pd.read_csv("Repository/CleanFeed.csv")

    # Initialize an empty string to store the HTML content
    html_content = """<!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>"""

    # HTML template for each feed item
    html_template = """
    <div class="feed-item">
    <h2 class="title">{title}</h2>
    <div class="metadata">
        <span class="id">{id}</span> | 
        <span class="category">{category}</span> | 
        <span class="published">{published}</span>
    </div>
    <div class="abstract">
        {abstract}
    </div>
    <a href="{url}" target="_blank">Read More</a>
    </div>
    """

    # Iterate through the DataFrame and fill in the HTML template
    for index, row in df.iterrows():
        item_html = html_template.format(
            title=row["Title"],
            id=row["Id"],
            category=row["Category"],
            published=row["Published"],
            abstract=row["Abstract"],
            url=row["URL"],
        )
        html_content += item_html
    html_content += """ </body>
    </html>"""
    # Save the generated HTML to a file for demonstration
    html_file_path = to_path
    with open(html_file_path, "w") as f:
        f.write(html_content)

    html_file_path


# build_html_feed(clean_feed())
