# Default configuration for ScholarlyRecommender
import json

with open("ScholarlyRecommender/congiguration.json") as json_file:
    config = json.load(json_file)


def get_config():
    with open("ScholarlyRecommender/congiguration.json") as json_file:
        config = json.load(json_file)
    return config


def update_config(new_config):
    with open("ScholarlyRecommender/congiguration.json", "w") as json_file:
        json.dump(new_config, json_file, indent=4)
