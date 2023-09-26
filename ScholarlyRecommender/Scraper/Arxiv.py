# import logging
import pandas as pd
import arxiv
from ScholarlyRecommender.const import BASE_REPO
from ScholarlyRecommender.config import get_config

config = get_config()
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

logging.disable(logging.CRITICAL)
"""


def search(
    query: str, max_results: int = 100, sort_by=arxiv.SortCriterion.SubmittedDate
) -> pd.DataFrame:
    """
    Scrape arxiv.org for papers matching the query and return a dataframe matching the BASE_REPO format.
    """

    search_client = arxiv.Client(page_size=max_results, delay_seconds=3, num_retries=5)

    repository = BASE_REPO()

    arx_search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_by)

    for result in search_client.results(arx_search):
        try:
            repository["Id"].append(result.entry_id.split("/")[-1])
            repository["Category"].append(result.primary_category)
            repository["Title"].append(result.title.strip("\n"))
            repository["Published"].append(result.published)
            repository["Abstract"].append(result.summary.strip("\n"))
            repository["URL"].append(result.pdf_url)
        except arxiv.arxiv.UnexpectedEmptyPageError as error:
            print(error)
            # logging.error(error)
            continue
    if len(repository["Id"]) == 0:
        raise ValueError("No papers found for this query")
    return pd.DataFrame(repository).set_index("Id")


def source_candidates(
    queries: list,
    max_results: int = 100,
    to_path: str = None,
    as_df: bool = False,
    prev_days: int = 7,
    sort_by=arxiv.SortCriterion.SubmittedDate,
):
    """
    Scrape arxiv.org for papers matching the queries, filter them and return a dataframe or save it to a csv file.
    """
    if queries is None:
        queries = config["queries"]
    if not isinstance(queries, list) or len(queries) == 0:
        raise ValueError("queries must be a list of strings with at least one element")
    if prev_days <= 0 or prev_days >= 30:
        raise ValueError("prev_days must be greater than 0 and at most 30")
    if len(queries) > 100:
        raise ValueError("Too many queries, please reduce the number of queries ")
    # normalize queries if for recommendations
    if sort_by == arxiv.SortCriterion.SubmittedDate:
        max_results = max(((100 * prev_days) // len(queries)), 100)
        num_days = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=prev_days)
    else:
        max_results = 100
        num_days = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=1095)
    # logging.info(f"Searching for {max_results} papers for each query")
    # print(f"Searching for {max_results} papers for each query")

    dfs = []
    for query in queries:
        # logging.info(f"Searching for {query}")
        # print(f"Searching for {query}")

        df2 = search(query, max_results=max_results, sort_by=sort_by)
        # logging.info(f"Number of papers extracted : {len(df2.index)}")
        # print(f"Number of papers extracted : {len(df2.index)}")
        dfs.append(df2)

    df = pd.concat(dfs)
    if df.index.has_duplicates:
        df = df[~df.index.duplicated(keep="first")]
    # Filter

    # Remove duplicates
    # df = df[~df.index.duplicated(keep="first")]

    # Only keep papers from the last week
    df["Published"] = pd.to_datetime(df["Published"])

    df = df[df["Published"] >= num_days]
    # logging.info(f"Number of papers extracted : {len(df.index)}")
    # print(f"Number of papers extracted : {len(df.index)}")
    if to_path is not None:
        df.to_csv(to_path)
    if as_df:
        return df
