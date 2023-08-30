import gzip
import numpy as np
from tqdm import tqdm
import pandas as pd
import arxiv
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


def rank(n: int = 5, k: int = 5, on: str = "Abstract"):
    likes = pd.read_csv("Repository/Goodpapers.csv")
    candidates = pd.read_csv("Repository/Candidates.csv")

    train = np.array([(row[on], row["Id"]) for _, row in likes.iterrows()])
    test = np.array([(row[on], row["Id"]) for _, row in candidates.iterrows()])

    results = []
    print(f"Starting to rank {len(test)} candidates...\n")
    for x1, id in tqdm(test):
        # calculate the compressed length of the utf-8 encoded text
        Cx1 = len(gzip.compress(x1.encode()))
        # create a distance array
        similarity_to_x1 = []
        for x2, _ in train:
            # calculate the compressed length of the utf-8 encoded text
            Cx2 = len(gzip.compress(x2.encode()))
            # concatenate the two texts
            x1x2 = " ".join([x1, x2])
            # calculate the compressed length of the utf-8 encoded concatenated text
            Cx1x2 = len(gzip.compress(x1x2.encode()))
            # calculate the normalized compression distance: a normalized version of information distance
            ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)

            similarity_to_x1.append(ncd)
        sorted_idx = np.sort(np.array(similarity_to_x1))
        mean = np.mean(sorted_idx[0:5])
        results.append((mean, id))

    df = pd.DataFrame(results, columns=["Similarity", "Id"])
    df["rank"] = df["Similarity"].rank(ascending=True)
    df = df.sort_values(by=["rank"])
    df["Id"] = df["Id"].apply(lambda x: str(x))
    reccommended = df["Id"].tolist()[0:n]
    print(f"Finished Ranking.\n")
    return reccommended


def rankV2(n: int = 5, k: int = 5, on: str = "Abstract"):
    likes = pd.read_csv("Repository/Candidates_Labeled.csv")
    candidates = pd.read_csv("Repository/Candidates.csv")

    train = np.array([(row[on], row["label"]) for _, row in likes.iterrows()])
    test = np.array([(row[on], row["Id"]) for _, row in candidates.iterrows()])

    results = []
    print(f"Starting to rank {len(test)} candidates...\n")
    for x1, id in tqdm(test):
        # calculate the compressed length of the utf-8 encoded text
        Cx1 = len(gzip.compress(x1.encode()))
        # create a distance array
        similarity_to_x1 = []
        for x2, _ in train:
            # calculate the compressed length of the utf-8 encoded text
            Cx2 = len(gzip.compress(x2.encode()))
            # concatenate the two texts
            x1x2 = " ".join([x1, x2])
            # calculate the compressed length of the utf-8 encoded concatenated text
            Cx1x2 = len(gzip.compress(x1x2.encode()))
            # calculate the normalized compression distance: a normalized version of information distance
            ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)

            similarity_to_x1.append(ncd)
        sorted_idx = np.argsort(np.array(similarity_to_x1))
        top_k_ratings = train[sorted_idx[:k], 1]
        topk = top_k_ratings.astype(int)
        mean = np.mean(topk)

        results.append((mean, id))

    df = pd.DataFrame(results, columns=["Similarity", "Id"])
    df["rank"] = df["Similarity"].rank(ascending=False)
    df = df.sort_values(by=["rank"])
    df["Id"] = df["Id"].apply(lambda x: str(x))
    reccommended = df["Id"].tolist()[0:n]
    print(f"Finished Ranking.\n")

    return reccommended


def fetch(ids: list):
    print(f"Fetching {len(ids)} papers from arxiv... \n")
    repository = BASE_REPO()
    search = arxiv.Search(
        query="",
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


def run(path: str = "Repository/Feed.csv"):
    reccommended = rankV2(n=5, on="Abstract")
    feed = fetch(reccommended)

    feed.to_csv(path)
    print(f"Feed saved to {path} \n")
    # TO DO filter and format feed, store feed
    # improve source_candidates, and rank
    # improve reusability of code and modularity
    # build user interface for front end and backend api


if __name__ == "__main__":
    run()
