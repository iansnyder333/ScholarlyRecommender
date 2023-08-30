import pandas as pd
import arxiv
from queries import queries
from copy import deepcopy

BASE_REPO = lambda: deepcopy(
    {
        "Id": [],
        "Category": [],
        "Title": [],
        "Published": [],
        "Abstract": [],
        "URL": [],
    }
)


def search(
    query: str, max_results: int = 100, sort_by=arxiv.SortCriterion.SubmittedDate
):
    repository = BASE_REPO()
    search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_by)
    for result in search.results():
        repository["Id"].append(result.entry_id.split("/")[-1])
        repository["Category"].append(result.primary_category)
        repository["Title"].append(result.title.strip("\n"))
        repository["Published"].append(result.published)
        repository["Abstract"].append(result.summary.strip("\n"))
        repository["URL"].append(result.pdf_url)
    return pd.DataFrame(repository).set_index("Id")


def source_candidates(queries: list = queries, max_results: int = 100):
    # Source
    repo = BASE_REPO()
    df = pd.DataFrame(repo).set_index("Id")
    for query in queries:
        print(f"Searching for {query}")
        df2 = search(query, max_results=max_results)
        print(f"Number of papers extracted : {df2.shape[0]}")
        df = pd.concat([df, df2])

    # Filter
    print(f"Number of papers extracted : {df.shape[0]}")
    # Remove duplicates
    df = df[~df.index.duplicated(keep="first")]
    print(f"Number of papers extracted : {df.shape[0]}")
    # Only keep papers from the last week
    df["Published"] = pd.to_datetime(df["Published"])
    df = df[df["Published"] > (pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=8))]
    print(f"Number of papers extracted : {df.shape[0]}")
    df.to_csv("Repository/Candidates.csv")
