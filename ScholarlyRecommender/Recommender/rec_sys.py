# import logging

import gzip
import numpy as np
from tqdm import tqdm
import pandas as pd
from arxiv.arxiv import Search


from ScholarlyRecommender.const import BASE_REPO
from ScholarlyRecommender.config import get_config
from ScholarlyRecommender.Recommender.cython_functions import calculate_ncd


config = get_config()
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

logging.disable(logging.CRITICAL)
"""


def rankerV3(
    context: pd.DataFrame, labels: pd.DataFrame, k: int = 6, on: str = "Abstract"
) -> pd.DataFrame:
    likes = labels
    candidates = context

    # train_texts = np.array([row[on] for _, row in likes.iterrows()])
    # test_texts = np.array([row[on] for _, row in candidates.iterrows()])
    # train_texts = np.array([row[on] for _, row in likes.iterrows()], dtype=np.str_)
    # test_texts = np.array([row[on] for _, row in candidates.iterrows()], dtype=np.str_)
    train_texts = np.array([row[on] for _, row in likes.iterrows()], dtype="object")
    test_texts = np.array([row[on] for _, row in candidates.iterrows()], dtype="object")
    train_ratings = np.array(
        [row["label"] for _, row in likes.iterrows()], dtype=int
    )  # Assuming 'Rating' is the column you want

    results = []

    ncd_results = calculate_ncd(test_texts, train_texts)

    # logging.info(f"Starting to rank {len(test)} candidates on {on}\n")
    # print(f"Starting to rank {len(test)} candidates on {on}\n")
    for i, (x1, id) in enumerate(
        tqdm(np.column_stack((test_texts, candidates["Id"])), disable=True)
    ):
        similarity_to_x1 = ncd_results[i]

        # calculate the similarity weights for the top k most similar papers
        # Converting the list to a numpy array for vectorized operations
        similarity_to_x1 = np.array(similarity_to_x1)
        # sort the array and get the top k most similar papers
        sorted_idx = np.argsort(similarity_to_x1)
        values = similarity_to_x1[sorted_idx[:k]]
        # calculate the similarity weights for the top k most similar papers
        weights = values / np.sum(values)
        # Weights need to be inverted so that the most similar papers (lowest distance) have the highest weights
        inverse_weights = 1 / weights
        inverse_weights_norm = (inverse_weights) / np.sum(inverse_weights)
        # get the top k ratings
        top_k_ratings = train_ratings[sorted_idx[:k]]
        # calculate the prediction as the inverse weighted mean of the top k ratings
        prediction = np.sum(np.dot(inverse_weights_norm, top_k_ratings))

        results.append((prediction, id))

    df = pd.DataFrame(results, columns=["predicted", "Id"])
    return df


def rank(context, labels=None, n: int = 5) -> list:
    """
    Run the rankerV3 algorithm on the context and return a list of the top 5 ranked papers.
    """
    if labels is None:
        labels = config["labels"]
    if isinstance(labels, str):
        labels = pd.read_csv(labels)
    if not isinstance(labels, pd.DataFrame):
        raise TypeError("labels must be a pandas DataFrame")
    df1 = rankerV3(context, labels, on="Abstract")
    df2 = rankerV3(context, labels, on="Title")
    df = df1.copy()
    df["predicted"] = (df1["predicted"] + df2["predicted"]) / 2
    df["rank"] = df["predicted"].rank(ascending=False)
    df = df[df["rank"] <= n]
    if len(df.index) > n:
        df = df.sort_values(by=["rank"])
    df["Id"] = df["Id"].apply(lambda x: str(x))
    reccommended = df["Id"].tolist()[0:n]
    # logging.info(f"Finished Ranking.\n")
    # print(f"Finished Ranking.\n")

    return reccommended


def evaluate(n: int = 5, k: int = 6, on: str = "Abstract") -> float:
    """
    Evaluate the recommender system using the normalized compression distance.
    Calculate the mean squared error between the predicted and actual ratings.
    Return the loss.
    """
    likes = pd.read_csv(config["labels"])
    # Set train and test equal to 90% and 10% of the data respectively
    train_data = likes.sample(frac=0.9, random_state=0)
    test_data = likes.drop(train_data.index)

    train = np.array([(row[on], row["label"]) for _, row in train_data.iterrows()])
    test = np.array([(row[on], row["label"]) for _, row in test_data.iterrows()])
    results = []
    # logging.info(f"Starting to rank {len(test)} candidates...\n")
    # print(f"Starting to rank {len(test)} candidates...\n")
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
        # Converting the list to a numpy array for vectorized operations
        similarity_to_x1 = np.array(similarity_to_x1)
        # sort the array and get the top k most similar papers
        sorted_idx = np.argsort(similarity_to_x1)
        values = similarity_to_x1[sorted_idx[:k]]
        # calculate the similarity weights for the top k most similar papers
        weights = values / np.sum(values)
        # Weights need to be inverted so that the most similar papers (lowest distance) have the highest weights
        inverse_weights = 1 / weights
        inverse_weights_norm = (inverse_weights) / np.sum(inverse_weights)
        # get the top k ratings
        top_k_ratings = train[sorted_idx[:k], 1].astype(int)
        # calculate the prediction as the inverse weighted mean of the top k ratings
        prediction = np.sum(np.dot(inverse_weights_norm, top_k_ratings))

        results.append((prediction, label))

    df = pd.DataFrame(results, columns=["predicted", "actual"])

    df["actual"] = df["actual"].astype(int)
    # calculate the mean squared error
    df["squared_error"] = (df["predicted"] - df["actual"]) ** 2
    # loss function
    loss = np.sqrt(df["squared_error"].sum() / df.shape[0])
    # print(df.head())
    return loss


def fetch(ids: list) -> pd.DataFrame:
    """
    Fetch papers from arxiv.org matching the ids and return a dataframe matching the BASE_REPO including the authors.
    """
    # logging.info(f"Fetching {len(ids)} papers from arxiv... \n")
    # print(f"Fetching {len(ids)} papers from arxiv... \n")
    repository = BASE_REPO()
    repository["Author"] = []
    search = Search(
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
        # repository["Author"].append(result.authors)
        repository["Author"].append([author.name for author in result.authors])

    return pd.DataFrame(repository)


def get_recommendations(
    data,
    labels,
    size: int = None,
    to_path: str = None,
    as_df: bool = False,
):
    """
    Rank the papers in the data and return a dataframe or save it to a csv file.
    Data can be a pandas DataFrame or a path to a csv file.
    """
    if labels is None:
        labels = config["labels"]
    if size is None:
        size = config["feed_length"]
    if isinstance(data, pd.DataFrame):
        df = data
        df.reset_index(inplace=True)
    elif isinstance(data, str):
        # assert data.endswith(".csv"), "data must be a csv file"
        df = pd.read_csv(data)
    else:
        raise TypeError("data must be a pandas DataFrame or a path to a csv file")
    if size < 0 or size > len(df.index):
        raise ValueError(
            "size must be greater than 0 and less than the length of the data"
        )

    reccommended = rank(
        context=df,
        labels=labels,
        n=size,
    )
    feed = fetch(reccommended)
    if to_path is not None:
        feed.set_index("Id").to_csv(to_path)
        # logging.info(f"Feed saved to {to_path} \n")
        # print(f"Feed saved to {to_path} \n")
        # feed.to_csv(to_path)
    if as_df:
        return feed
