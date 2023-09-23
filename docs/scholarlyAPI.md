# Scholarly Recommender API Documentation

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

- **parameters:**
  - None
- **returns:**
  - config: dict
    - A python dictionary representing the current configuration being used by the system. It is internally stored as a json file.

### update_config

```sh
ScholarlyRecommender.update_config(new_config, **kwargs) -> None:
```
 
what it does

- **parameters:**
  - new_config: dict
    - A python dictionary representing the new configuration the system will use. This will be internally stored as a json file to configuration.json and will overwrite the previous configuration.
  - **kwargs: optional params
    - Optional keyword arguments used for testing and debugging. 
- **returns:**
  - None

### source_candidates

```sh
ScholarlyRecommender.source_candidates(
    queries: list,
    max_results: int = 100,
    to_path: str = None,
    as_df: bool = False,
    prev_days: int = 7,
    sort_by=arxiv.SortCriterion.SubmittedDate,
) -> pd.DataFrame:
```
 
Scrapes the web for papers matching the queries, filters them and returns a dataframe containing the results. Results can also be saved to a csv file.

- **parameters:**
  - queries: list of str
    - The search queries to scrape, represented as strings. At least one query is required.
  - max_results
  - to_path
  - as_df
  - prev_dats
  - sort_by

  
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

- **parameters:**
  - None
- **returns:**
  - None

### evaluate

```sh
ScholarlyRecommender.evaluate(n: int = 5, k: int = 6, on: str = "Abstract") -> float:
```
 
what it does

- **parameters:**
  - None
- **returns:**
  - None

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

- **parameters:**
  - None
- **returns:**
  - None
