import gzip
import numpy as np
from tqdm import tqdm
import pandas as pd
import arxiv
from ScholarlyRecommender.const import BASE_REPO


def rankerV3(
    context: pd.DataFrame, n: int = 5, k: int = 5, on: str = "Abstract"
) -> pd.DataFrame:
    """
    Rank the papers in the context using the normalized compression distance combined with a weighted top-k mean rating.
    Return a list of the top n ranked papers.
    This is a modified version of the algorithm described in the paper "“Low-Resource” Text Classification- A Parameter-Free Classification Method with Compressors."
    The algorithim gets the top k most similar papers to each paper in the context that the user rated and calculates the mean rating of those papers as its prediction.

    """
    likes = pd.read_csv(
        "ScholarlyRecommender/Repository/labeled/Candidates_Labeled.csv"
    )
    candidates = context

    train = np.array([(row[on], row["label"]) for _, row in likes.iterrows()])
    test = np.array([(row[on], row["Id"]) for _, row in candidates.iterrows()])

    results = []
    print(f"Starting to rank {len(test)} candidates on {on}\n")
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
        top_k_ratings = train[sorted_idx[:k], 1].astype(int)
        # calculate the prediction as the inverse weighted mean of the top k ratings
        prediction = np.sum(np.dot(inverse_weights_norm, top_k_ratings))

        results.append((prediction, id))

    df = pd.DataFrame(results, columns=["predicted", "Id"])
    return df


def rank(context, n: int = 5) -> list:
    """
    Run the rankerV3 algorithm on the context and return a list of the top 5 ranked papers.
    """
    df1 = rankerV3(context, on="Abstract")
    df2 = rankerV3(context, on="Title")
    df = df1.copy()
    df["predicted"] = (df1["predicted"] + df2["predicted"]) / 2
    df["rank"] = df["predicted"].rank(ascending=False)
    df = df.sort_values(by=["rank"])
    df["Id"] = df["Id"].apply(lambda x: str(x))
    reccommended = df["Id"].tolist()[0:n]
    print(f"Finished Ranking.\n")

    return reccommended


def evaluate(n: int = 5, k: int = 6, on: str = "Abstract") -> float:
    """
    Evaluate the recommender system using the normalized compression distance.
    Calculate the mean squared error between the predicted and actual ratings.
    Return the loss.
    """
    likes = pd.read_csv(
        "ScholarlyRecommender/Repository/labeled/Candidates_Labeled.csv"
    )
    # Set train and test equal to 90% and 10% of the data respectively
    train_data = likes.sample(frac=0.9, random_state=0)
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
    print(f"Fetching {len(ids)} papers from arxiv... \n")
    repository = BASE_REPO()
    repository["Author"] = []
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
        repository["Author"].append(result.authors)

    return pd.DataFrame(repository)


def get_recommendations(data, size: int = 5, to_path: str = None, as_df: bool = False):
    """
    Rank the papers in the data and return a dataframe or save it to a csv file.
    Data can be a pandas DataFrame or a path to a csv file.
    """
    if isinstance(data, pd.DataFrame):
        df = data
        df.reset_index(inplace=True)
    elif isinstance(data, str):
        assert data.endswith(".csv"), "data must be a csv file"
        df = pd.read_csv(data)
    else:
        raise TypeError("data must be a pandas DataFrame or a path to a csv file")
    assert size > 0, "size must be greater than 0"
    assert size < len(df.index), "size must be less than the length of the data"

    reccommended = rank(context=df, n=size)
    feed = fetch(reccommended)
    if to_path is not None:
        feed.set_index("Id").to_csv(to_path)
        print(f"Feed saved to {to_path} \n")
        # feed.to_csv(to_path)
    if as_df:
        return feed
