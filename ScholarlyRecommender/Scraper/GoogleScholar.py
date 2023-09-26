import requests
from bs4 import BeautifulSoup
import pandas as pd


class ScraperForGoogleScholar:
    def __init__(self, headers, repository: dict = None):
        self.headers = headers
        if repository is None:
            self.repository = {
                "Paper Title": [],
                "Author": [],
                "Publication": [],
                "Url of paper": [],
                "Abstract": [],
            }
        else:
            self.repository = repository

    def _get_paperinfo(self, paper_url: str):
        # download the page
        response = requests.get(paper_url, headers=self.headers)
        # check successful response
        if response.status_code != 200:
            raise AssertionError(f"Failed to fetch web page {paper_url}")
        # parse using beautiful soup
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def _get_tags(doc: BeautifulSoup) -> tuple:
        paper_tag = doc.select("[data-lid]")
        link_tag = doc.find_all("h3", {"class": "gs_rt"})
        author_tag = doc.find_all("div", {"class": "gs_a"})
        abstract_tag = doc.find_all("div", {"class": "gs_rs"})
        return (paper_tag, link_tag, author_tag, abstract_tag)

    @staticmethod
    def _get_papertitle(paper_tag: list) -> list:
        return [tag.select("h3")[0].get_text() for tag in paper_tag]

    @staticmethod
    def _get_link(link_tag: list) -> list:
        return [link_tag[i].a["href"] for i in range(len(link_tag))]

    @staticmethod
    def _get_author_publisher_info(authors_tag: list) -> tuple:
        authors = []
        publishers = []
        for v, _ in enumerate(authors_tag):
            authortag_text = (authors_tag[v].text).split("-")

            if len(authortag_text) == 0:
                authors.append("None")
                publishers.append("None")
            elif len(authortag_text) == 1:
                authors.append(authortag_text[0])
                publishers.append("None")
            else:
                authors.append(authortag_text[0])
                publishers.append(authortag_text[-1])

        return (authors, publishers)

    @staticmethod
    def _get_abstract(abstract_tag: list) -> list:
        abstract = []
        for i, _ in enumerate(abstract_tag):
            s = (abstract_tag[i].text).strip().split("-")
            s = " ".join(s[1:])
            s = s.strip("\n")
            abstract.append(s)
        return abstract

    def _add_in_paper_repo(self, **kwargs) -> pd.DataFrame:
        self.repository["Paper Title"].extend(kwargs["papername"])
        self.repository["Author"].extend(kwargs["author"])
        self.repository["Publication"].extend(kwargs["publisher"])
        self.repository["Url of paper"].extend(kwargs["url"])
        self.repository["Abstract"].extend(kwargs["abstract"])
        return pd.DataFrame(self.repository)

    def scrape(self, url: str, to_df: bool = True):
        # get url for the each page

        # function for the get content of each page
        doc = self._get_paperinfo(url)

        # function for the collecting tags
        paper_tag, link_tag, author_tag, abstract_tag = self._get_tags(doc)

        # paper title from each page
        papername = self._get_papertitle(paper_tag)

        # year , author , publication of the paper
        author, public = self._get_author_publisher_info(author_tag)

        # url of the paper
        link = self._get_link(link_tag)
        abstract = self._get_abstract(abstract_tag)
        # add in paper repo dict
        paper = self._add_in_paper_repo(
            papername=papername,
            author=author,
            publisher=public,
            url=link,
            abstract=abstract,
        )

        if to_df:
            return paper
        return paper.to_dict()


if __name__ == "__main__":
    test = ScraperForGoogleScholar(
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
    )
    ret = test.scrape(
        "https://scholar.google.com/scholar?scisbd=1&q=%22deep+learning%22&hl=en&as_sdt=0,39"
    )
    print(ret["Abstract"][0])
