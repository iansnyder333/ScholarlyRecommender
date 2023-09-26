import pandas as pd
import re
from ScholarlyRecommender.config import get_config

config = get_config()


def clean_feed(dataframe: pd.DataFrame):
    """Clean the dataframe to match the BASE_REPO format."""
    df = dataframe[
        ["Id", "Category", "Title", "Published", "Abstract", "URL", "Author"]
    ].copy()
    df.reset_index(inplace=True)
    df["Author"] = df["Author"].astype(str)
    df["Id"] = df["Id"].apply(lambda x: "Entry Id: " + str(x))
    df["Published"] = pd.to_datetime(df["Published"]).dt.strftime("%m-%d-%Y")
    df["Published"] = df["Published"].apply(lambda x: "Published on " + str(x))
    df["Author"] = df["Author"].apply(extract_author_names)
    df["Author"] = df["Author"].str[:500] + "..."
    df["Abstract"] = df["Abstract"].str[:500] + "..."

    df["Abstract"] = df["Abstract"].apply(remove_latex)
    df["Title"] = df["Title"].apply(remove_latex)
    return df


def extract_author_names(author_string):
    """Extract the author names from the author string."""
    # The regular expression to match any characters enclosed within single quotes
    pattern = r"\'(.*?)\'"

    # Find all matches of the pattern
    matches = re.findall(pattern, author_string)

    return ", ".join(matches)


def remove_latex(text):
    """Remove LaTeX from the text."""
    # Remove inline LaTeX
    clean_text = re.sub(r"\$.*?\$", "", text)

    # Remove block LaTeX
    clean_text = re.sub(r"\\begin{.*?}\\end{.*?}", "", clean_text)

    return clean_text


def build_email(
    df: pd.DataFrame,
    email: bool = False,
    to_path: str = None,
    web: bool = False,
):
    """Build the HTML email."""
    flanT5_out = {
        "headline": "Your Scholarly Recommender Newsletter Feed",
        "intro": "Thank you for using Scholarly Recommender. Here is your feed.",
    }

    html_content = """<!DOCTYPE html>
    <html>
    <body style="background-color: #FFFFFF; color: #A2A2F5">
    """
    if email:
        body_template = """
    <h2 class="title-main" style='font-family: "Open Sans", sans-serif; color: #262730;
    font-family: Arial, sans-serif;
        font-size: 28px;
        letter-spacing: 0.05em;

        color: #2C3E50;
        margin-bottom: 10px;'>{headline}</h2>
    <p style='font-family: "Open Sans", sans-serif; color: #262730; font-size: 18px;
        margin-bottom: 20px; line-height: 1.6;'>
        Dear Reader,
        </p>
    <p style='font-family: "Open Sans", sans-serif; color: #262730; font-size: 18px;
        margin-bottom: 20px; line-height: 1.6;'>
            {intro}
    </p>
        """
        body_html = body_template.format(
            headline=flanT5_out["headline"],
            intro=flanT5_out["intro"],
        )
        html_content += body_html
    # HTML template for each feed item
    html_template = """
    <div class="feed-item" style="border: 1px solid #ccc;
    padding: 15px;
    margin: 15px;
    border-radius: 8px;">
    <h2 class="title" style=" font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px; color: #262730;">{title}</h2>
    <h4 class="author" style="font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px; color:#262730;">{author}</h4>
    <div class="metadata" style="font-size: 14px;
    color: #262730;
    margin-bottom: 10px;">
        <span class="id">{id}</span> |
        <span class="category">{category}</span> |
        <span class="published">{published}</span>
    </div>
    <div class="abstract" style="font-size: 16px;
    margin-bottom: 10px; color: #262730;">
        {abstract}
    </div>
    <a href="{url}" target="_blank" style="display: inline-block;
    background-color: #A2A2F5;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;">Read More</a>
    </div>
    """

    # Iterate through the DataFrame and fill in the HTML template
    for _, row in df.iterrows():
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
    if web:
        return html_content
    if to_path is None:
        to_path = config["feed_path"]
    html_file_path = to_path
    with open(html_file_path, "w") as f:
        f.write(html_content)
    return True


def get_feed(
    data,
    email: bool = False,
    to_path: str = None,
    web: bool = False,
):
    """Get the feed."""
    if isinstance(data, pd.DataFrame):
        df = clean_feed(data)
        res = build_email(df, email=email, to_path=to_path, web=web)
        return res

    if isinstance(data, str):
        df = clean_feed(pd.read_csv(data))
        res = build_email(df, email=email, to_path=to_path, web=web)
        return res
    raise TypeError("data must be a pandas DataFrame or a path to a csv file")
