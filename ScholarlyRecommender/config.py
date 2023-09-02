# Default configuration for ScholarlyRecommender
import json


def get_config():
    with open("ScholarlyRecommender/configuration.json") as json_file:
        config = json.load(json_file)
    return config


def update_config(new_config):
    with open("ScholarlyRecommender/configuration.json", "w") as json_file:
        json.dump(new_config, json_file, indent=4)
