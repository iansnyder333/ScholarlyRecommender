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
