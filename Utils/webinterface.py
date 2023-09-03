def build_query(selected_sub_categories: dict) -> list:
    """
    Build a query from the selected sub-categories
    @param selected_sub_categories: dict
    @return: list of queries represented as strings
    """
    return


def generate_feed_pipeline(query: list, n: int, days: int):
    """
    Generate a feed from a query, this is the main pipeline for generating recommendations
    @param query: list of queries represented as strings, defaults to sys_config()["queries"]
    @param n: number of recommendations to generate, defaults to 5
    @param days: number of days back to search, defaults to 7
    @return: None
    """
    return


def fetch_papers(num_papers: int = 10):
    """
    Collect a sample of papers from arXiv for calibration, sourced using the default configuration of interest categories
    Papers are collected, shuffled, and returned as a formatted DataFrame
    @param num_papers: number of papers to collect, defaults to 10
    @return: DataFrame of papers formatted for labeling
    """
    return


def calibrate_rec_sys(num_papers: int = 10):
    """
    Interactive calibration tool for the recommender system, essentially serves as a user interface for manual labeling
    @param num_papers: number of papers to rate, defaults to 10
    @return: None, labels configured in sys_config["labels"]
    """
    return
