# Scholarly Recommender API Documentation (In Progress)

## TODO

source_candidates
get_recommendations
evaluate
get_feed
get_config
update_config
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-this-document">About This Document</a>
      <ul>
        <li><a href="#frequently-asked-questions">Frequently Asked Questions</a></li>
      </ul>
    </li>
    <li>
      <a href="#functions-and-usage">Functions and Usage</a>
      <ul>
        <li><a href="#get_config">get_config</a></li>
        <li><a href="#update_config">update_config</a></li>
        <li><a href="#source_candidates">source_candidates</a></li>
        <li><a href="#get_recommendations">get_recommendations</a></li>
        <li><a href="#evaluate">evaluate</a></li>
        <li><a href="#get_feed">get_feed</a></li>
      </ul>
    </li>
  </ol>
</details>


## About this Document

TODO

## Frequently Asked Questions

TODO

<!-- FUNCTIONS AND USAGE -->
## Functions and Usage

TODO


### get_config

```sh
ScholarlyRecommender.get_config() -> dict:
```
 
Retrieves the current configurations being used by the ScholarlyRecommender system.

- **Parameters:**
  - None
- **Returns:**
  - config: dict
    - A python dictionary representing the current configuration being used by the system. It is internally stored as a json file.
- **Example**
  - ```sh
    import ScholarlyRecommender as sr

    config = sr.get_config
    queries = config['queries]
    ```

### update_config

```sh
ScholarlyRecommender.update_config(new_config, **kwargs) -> None:
```
 
what it does

- **Parameters:**
  - new_config: dict
    - A python dictionary representing the new configuration the system will use. This will be internally stored as a json file to configuration.json and will overwrite the previous configuration.
  - **kwargs: optional params
    - Optional keyword arguments used for testing and debugging. 
- **Returns:**
  - None
- **Example**
  - ```sh
    import ScholarlyRecommender as sr
    ```

### source_candidates

```sh
ScholarlyRecommender.source_candidates(
    queries: list,
    max_results: int = 100,
    to_path: str = None,
    as_df: bool = True,
    prev_days: int = 7,
    sort_by=arxiv.SortCriterion.SubmittedDate,
) -> pd.DataFrame:
```
 
Scrapes the web for papers matching the queries, filters them and returns a dataframe containing the results. Results can also be saved to a csv file.

- **Parameters:**
  - queries: list of str
    - The search queries to scrape, represented as strings. The length of queries must be greater than zero and less than 100.
  - max_results: int, *optional*
    - The maximum number of candidates to source per query, defaults to 100 and dynamically scales based on the length of queries.
  - to_path: str, path object, file-like object, *optional*
    - Where to store the resulting candidates if desired, the dataframe will be saved here as a csv. Defaults to None.
  - as_df: bool, *optional*
    - Boolean to indicate if the resulting candidates should be returned as a Pandas Dataframe. defaults to True, and should only be changed to False if to_path is provided.
  - prev_days: int, *optional*
    - The maximum number of days (inclusive) since the publication date for candidates, defaults to 7, must be greater than 0 and less than 31.
  - sort_by: arxiv.SortCriterion, *optional*
    - TODO
- **Returns:**
  - None
- **Example**
  - ```sh
    import ScholarlyRecommender as sr
    ```
  
### get_recommendations

```sh
ScholarlyRecommender.get_recommendations(
    data,
    labels,
    size: int = None,
    to_path: str = None,
    as_df: bool = False,
):
```
 
what it does

- **Parameters:**
  - None
- **Returns:**
  - None
- **Example**
  - ```sh
    import ScholarlyRecommender as sr
    ```

### evaluate

```sh
ScholarlyRecommender.evaluate(n: int = 5, k: int = 6, on: str = "Abstract") -> float:
```
 
Evaluate the recommender system on the labeled dataset. Uses the normalized compression distance to predict the masked rating.
Calculates the mean squared error between the predicted and actual ratings and returns the total loss.


- **Parameters:**
  - None
- **Returns:**
  - None
- **Example**
  - ```sh
    import ScholarlyRecommender as sr
    ```

### get_feed

```sh
ScholarlyRecommender.get_feed(
    data,
    email: bool = False,
    to_path: str = None,
    web: bool = False,
):
```
 
what it does

- **Parameters:**
  - None
- **Returns:**
  - None
- **Example**
  - ```sh
    import ScholarlyRecommender as sr
    ```
