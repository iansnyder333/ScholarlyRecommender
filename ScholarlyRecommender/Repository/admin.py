"""
This module contains functions to create and manage the database for the
 recommender system.
"""
import pandas as pd
import arxiv

from ScholarlyRecommender.const import BASE_REPO


def get_papers(ids: list, query: str = "") -> pd.DataFrame:
    """
    Scrape arxiv.org for papers matching the query and return a dataframe matching
      the BASE_REPO format.
    """
    repository = BASE_REPO()
    search = arxiv.Search(
        query=query,
        id_list=ids,
    )
    for result in search.results():
        repository["Id"].append(result.entry_id.split("/")[-1])
        repository["Category"].append(result.primary_category)
        repository["Title"].append(result.title.strip("\n"))
        repository["Published"].append(result.published)
        repository["Abstract"].append(result.summary.strip("\n"))
        repository["URL"].append(result.pdf_url)
    return pd.DataFrame(repository).set_index("Id")


def build_arxiv_repo(ids: list, path: str) -> None:
    """Build a csv file containing the papers matching the ids."""
    if not path.endswith(".csv"):
        raise AssertionError("Path must be a csv file")
    df = get_papers(ids)
    df.to_csv(path)


def add_paper(ids: list, to_repo: str) -> None:
    """Add papers matching the ids to the repository. Duplicates are removed."""
    if not to_repo.endswith(".csv"):
        raise AssertionError("Repository must be a csv file")
    df1 = pd.read_csv(to_repo, index_col="Id")
    df2 = get_papers(ids)
    df = pd.concat([df1, df2])
    df = df[~df.index.duplicated(keep="first")]
    df.to_csv(to_repo)


def remove_paper(ids: list, from_repo: str) -> None:
    """Remove papers matching the ids from the repository."""
    if not from_repo.endswith(".csv"):
        raise AssertionError("Repository must be a csv file")
    df1 = pd.read_csv(from_repo, index_col="Id")
    df2 = get_papers(ids)
    df = df1.drop(df2.index)
    df.to_csv(from_repo)
