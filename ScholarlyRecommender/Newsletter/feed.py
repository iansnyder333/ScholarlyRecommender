import pandas as pd
import numpy as np
from datetime import datetime
import re


def clean_feed(path: str):
    df = pd.read_csv(path)
    df["Id"] = df["Id"].apply(lambda x: "Entry Id: " + str(x))
    df["Published"] = pd.to_datetime(df["Published"]).dt.strftime("%m-%d-%Y")
    df["Published"] = df["Published"].apply(lambda x: "Published on " + str(x))
    df["Author"] = df["Author"].apply(extract_author_names)
    df["Abstract"] = df["Abstract"].str[:500] + "..."
    return df


def extract_author_names(author_string):
    # The regular expression to match any characters enclosed within single quotes
    pattern = r"\'(.*?)\'"

    # Find all matches of the pattern
    matches = re.findall(pattern, author_string)

    return ", ".join(matches)


# Pipeline()


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
    <h4 class="author">{author}</h4>
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
            author=row["Author"],
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
def get_feed(data, to_path: str = "ScholarlyRecommender/Newsletter/html/Feed.html"):
    if isinstance(data, pd.DataFrame):
        data.to_csv("ScholarlyRecommender/Repository/TempFeed.csv", index=False)
        df = clean_feed("ScholarlyRecommender/Repository/TempFeed.csv")
        build_html_feed(df, to_path)
    elif isinstance(data, str):
        df = clean_feed(data)
        build_html_feed(df, to_path)
    else:
        raise TypeError("data must be a pandas DataFrame or a path to a csv file")
