from copy import deepcopy


def BASE_REPO():
    """
    initialize a new base repo as a deep copy
    @param: None
    @return: a dictionary (str:list)
    """
    return deepcopy(
    {
        "Id": [],
        "Category": [],
        "Title": [],
        "Published": [],
        "Abstract": [],
        "URL": [],
    }
)
