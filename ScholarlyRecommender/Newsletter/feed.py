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
    <meta charset="utf-8"/><meta content="width=device-width, initial-scale=1.0" name="viewport"/><link href="https://fonts.googleapis.com/css2?family=Open+Sans&amp;display=swap" rel="stylesheet"/>

    <title>Weekly Newsletter</title>
    <style>
    .title-main{
    font-family: "Helvetica Neue", sans-serif;
    font-size: 28px;
    letter-spacing: 0.05em;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    color: #2C3E50;
    margin-bottom: 10px;
}
p {
    font-family: "Georgia", serif;
    font-size: 18px;
    line-height: 1.6;
    text-align: justify;
    color: #333;
    margin-bottom: 20px;
}
/* General styles for each feed item */
.feed-item {
    border: 1px solid #ccc;
    padding: 15px;
    margin: 15px;
    border-radius: 8px;
}

/* Style for the title */
.title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}
.author {
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px;
}
/* Style for the metadata section */
.metadata {
    font-size: 14px;
    
    margin-bottom: 10px;
}

/* Style for the abstract */
.abstract {
    font-size: 16px;
    margin-bottom: 10px;
}

/* Style for the read more link */
a {
    display: inline-block;
    background-color: #007BFF;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
}
    </style><style>
/* Responsive Design */
@media only screen and (max-width: 600px) {
    body {
        font-size: 16px;
    }
}

/* Custom Fonts */
body {
    font-family: 'Open Sans', sans-serif;
}

/* Improved Color Scheme */
.title-main {
    color: #34495e;
}

p {
    color: #2c3e50;
}
</style>
        
    </head>
    <body>
    <h2 class="title-main" style='font-family: "Open Sans", sans-serif; color: #34495e;'>Decoding the Future of AI: Ethical Dilemmas, Embedding Logic, and Emotion Analytics in Conversational Tech—A Curated Selection of Cutting-Edge Research</h2>
<p style='font-family: "Open Sans", sans-serif; color: #2c3e50;'>
    Dear Reader,
    </p>
<p style='font-family: "Open Sans", sans-serif; color: #2c3e50;'>
        This edition aims to immerse you in the nuanced fabric of Large Language Models, spanning topics from ethical concerns in moderation and gender biases to highly technical advancements like embedding logic programming into Python's deep-learning ecosystem. Expect in-depth analyses and pioneering solutions that push the boundaries of conventional wisdom, handpicked to empower your specialized interest in these paradigms.
</p>"""

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


def build_email(
    df: pd.DataFrame, to_path: str = "ScholarlyRecommender/Newsletter/html/Feed.html"
):
    # df = pd.read_csv("Repository/CleanFeed.csv")

    # Initialize an empty string to store the HTML content
    html_content = """<!DOCTYPE html>
    <html>
    <body>
    <h2 class="title-main" style='font-family: "Open Sans", sans-serif; color: #34495e;font-family: Arial, sans-serif;
    font-size: 28px;
    letter-spacing: 0.05em;
    
    color: #2C3E50;
    margin-bottom: 10px;'>Decoding the Future of AI: Ethical Dilemmas, Embedding Logic, and Emotion Analytics in Conversational Tech—A Curated Selection of Cutting-Edge Research</h2>
<p style='font-family: "Open Sans", sans-serif; color: #2c3e50;'>
    Dear Reader,
    </p>
<p style='font-family: "Open Sans", sans-serif; color: #2c3e50;'>
        This edition aims to immerse you in the nuanced fabric of Large Language Models, spanning topics from ethical concerns in moderation and gender biases to highly technical advancements like embedding logic programming into Python's deep-learning ecosystem. Expect in-depth analyses and pioneering solutions that push the boundaries of conventional wisdom, handpicked to empower your specialized interest in these paradigms.
</p>
   """

    # HTML template for each feed item
    html_template = """
    <div class="feed-item" style="border: 1px solid #ccc;
    padding: 15px;
    margin: 15px;
    border-radius: 8px;">
    <h2 class="title" style=" font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;">{title}</h2>
    <h4 class="author" style="font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px; color:#000000;">{author}</h4>
    <div class="metadata" style="font-size: 14px;
    color: #000000;
    margin-bottom: 10px;">
        <span class="id">{id}</span> | 
        <span class="category">{category}</span> | 
        <span class="published">{published}</span>
    </div>
    <div class="abstract" style="font-size: 16px;
    margin-bottom: 10px; color: #000000;">
        {abstract}
    </div>
    <a href="{url}" target="_blank" style="display: inline-block;
    background-color: #007BFF;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;">Read More</a>
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
        # build_html_feed(df, to_path)
        build_email(df, to_path)
    elif isinstance(data, str):
        df = clean_feed(data)
        build_email(df, to_path)
        # build_html_feed(df, to_path)
    else:
        raise TypeError("data must be a pandas DataFrame or a path to a csv file")
