# Default configuration for ScholarlyRecommender

from json import load, dump

with open("ScholarlyRecommender/configuration.json") as json_file:
    config = load(json_file)


def get_config():
    with open("ScholarlyRecommender/configuration.json") as json_file:
        config = load(json_file)
    return config


def update_config(new_config, **kwargs):
    if kwargs["test_mode"]:
        with open(kwargs["test_path"], "w") as json_file:
            dump(new_config, json_file, indent=4)
    else:
        with open("ScholarlyRecommender/configuration.json", "w") as json_file:
            dump(new_config, json_file, indent=4)
