import gzip
import numpy as np
from tqdm import tqdm
import pandas as pd
import arxiv
from ScholarlyRecommender.const import BASE_REPO


def rankV2(n: int = 5, k: int = 5, on: str = "Abstract"):
    likes = pd.read_csv("ScholarlyRecommender/Repository/Candidates_Labeled.csv")
    candidates = pd.read_csv("ScholarlyRecommender/Repository/TestCandidates.csv")

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


def evaluate(n: int = 5, k: int = 5, on: str = "Abstract"):
    likes = pd.read_csv("ScholarlyRecommender/Repository/Candidates_Labeled.csv")
    # Set train and test equal to 90% and 10% of the data respectively
    train_data = likes.sample(frac=0.9, random_state=1)
    test_data = likes.drop(train_data.index)

    train = np.array([(row[on], row["label"]) for _, row in train_data.iterrows()])
    test = np.array([(row[on], row["label"]) for _, row in test_data.iterrows()])

    results = []
    print(f"Starting to rank {len(test)} candidates...\n")
    for x1, label in tqdm(test):
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

        results.append((mean, label))

    df = pd.DataFrame(results, columns=["predicted", "actual"])

    df["actual"] = df["actual"].astype(int)
    # calculate the mean squared error
    df["squared_error"] = (df["predicted"] - df["actual"]) ** 2
    # loss function
    loss = np.sqrt(df["squared_error"].sum() / df.shape[0])
    print(df)
    print(loss)


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


def run(path: str = "ScholarlyRecommender/Repository/Feed.csv"):
    reccommended = rankV2(n=5, on="Abstract")
    feed = fetch(reccommended)

    feed.to_csv(path)
    print(f"Feed saved to {path} \n")


if __name__ == "__main__":
    evaluate()
    # run()