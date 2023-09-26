import ScholarlyRecommender as sr
import pandas as pd
from pandas.testing import assert_frame_equal
from json import load
import unittest
import time
import tracemalloc

"""
This module contains unit tests for the ScholarlyRecommender package.
Before pushing to the repository, please run the tests to ensure that the package is working as expected.
More tests will be added as the package is developed.

TODO Test feed outputs for email, webapp, etc. Add more tests for the webapp, and more comprehensive tests for the API.
"""


# Test Constants
# Base directory for testing
BASE_TEST_DIR = "ScholarlyRecommender/Repository/tests/"
TEST_INPUT_DIR = BASE_TEST_DIR + "inputs/"
TEST_OUTPUT_DIR = BASE_TEST_DIR + "outputs/"
# Test Configuration files
TEST_CONFIG_PATH = TEST_INPUT_DIR + "test_configuration.json"
TEST_CONFIG_UPDATE_OUT = TEST_OUTPUT_DIR + "test_configuration_update.json"
# Test Reference input files
REF_CANDIDATES_PATH = TEST_INPUT_DIR + "ref_candidates.csv"
REF_LABELS_PATH = TEST_INPUT_DIR + "ref_labels.csv"
REF_RECOMMENDATIONS_PATH = TEST_INPUT_DIR + "ref_recommendations.csv"
# Test Output files
TEST_CANDIDATES_OUT = TEST_OUTPUT_DIR + "test_candidates.csv"
TEST_LABELS_OUT = TEST_OUTPUT_DIR + "test_labels.csv"
TEST_RECOMMENDATIONS_OUT = TEST_OUTPUT_DIR + "test_recommendations.csv"
TEST_FEED_OUT = TEST_OUTPUT_DIR + "test_feed.html"


class TestScholarlyRecommender(unittest.TestCase):
    # Setup the test environment
    def setUp(self):
        with open(TEST_CONFIG_PATH) as json_file:
            self.ref_config = load(json_file)
        self.config = sr.get_config()
        self.candidates = pd.read_csv(REF_CANDIDATES_PATH)
        self.candidates_labeled = pd.read_csv(REF_LABELS_PATH)
        self.recommendations = pd.read_csv(REF_RECOMMENDATIONS_PATH)

    """
    CONFIGURATION TESTS

    First, these tests ensure that the current configuration is valid, validating the keys, value types, and value shapes against the reference.
    Second, the retrieval and update functions for the ScholarlyRecommender configuration API are tested.
    """

    # Test the configuration file and its contents
    def test_config(self):
        # Check that the config file is valid
        self.assertEqual(self.config.keys(), self.ref_config.keys())

    def test_config_query(self):
        # Test the queries
        config_queries = self.config["queries"]
        self.assertTrue(isinstance(config_queries, list))
        self.assertTrue(len(config_queries) > 0)
        self.assertTrue(all(isinstance(item, str) for item in config_queries))

    def test_config_labels(self):
        # Test the labels
        config_labels = pd.read_csv(self.config["labels"])
        expected_columns = list(self.candidates_labeled.columns)
        columns = list(config_labels.columns)
        self.assertEqual(columns, expected_columns)

    def test_config_feed_length(self):
        # Test the feed length
        self.assertTrue(isinstance(self.config["feed_length"], int))
        self.assertTrue(self.config["feed_length"] > 0)
        self.assertTrue(self.config["feed_length"] <= 10)

    # Test the config retrieval function
    def test_get_config(self):
        with open("ScholarlyRecommender/configuration.json") as json_file:
            expected_config = load(json_file)

        config = sr.get_config()
        self.assertEqual(config, expected_config)

    # Test the config update function
    def test_update_config(self):
        # Change as necessary
        expected_config = {
            "queries": ["Computer Science", "Mathematics"],
            "labels": "ScholarlyRecommender/Repository/tests/test_candidates_labeled.csv",
            "feed_length": 7,
            "feed_path": "ScholarlyRecommender/Repository/tests/test_feed.html",
        }
        sr.update_config(
            expected_config, test_mode=True, test_path=TEST_CONFIG_UPDATE_OUT
        )
        with open(TEST_CONFIG_UPDATE_OUT) as json_file:
            config = load(json_file)

        self.assertEqual(config, expected_config)

    """
    ScholarlyRecommender API TESTS

    These tests ensure that the ScholarlyRecommender API is working as expected. 
    Each test checks that the output is the correct shape and type, in both return formats.
    These tests are run under the assumption that the configuration is valid.

    """

    # Test that the outputs from candidate sourcing are the correct shape and type, in both return formats
    def test_source_candidates(self):
        out = TEST_CANDIDATES_OUT
        df_candidates = sr.source_candidates(
            queries=self.config["queries"],
            as_df=True,
            prev_days=7,
            to_path=out,
        )
        df_candidates.reset_index(inplace=True)

        candidates = pd.read_csv(out)
        expected_columns = list(self.candidates.columns)
        expected_dtypes = self.candidates.dtypes.astype(str).to_dict()

        # Compare the column names
        self.assertListEqual(list(candidates.columns), expected_columns)
        self.assertListEqual(list(df_candidates.columns), expected_columns)

        # Compare the data types of each column
        self.assertDictEqual(candidates.dtypes.astype(str).to_dict(), expected_dtypes)

    # Test that the outputs from the ranking are the correct shape and type, in both return formats
    def test_get_recommendations(self):
        out = TEST_RECOMMENDATIONS_OUT
        df_recommendations = sr.get_recommendations(
            data=REF_CANDIDATES_PATH,
            labels=REF_LABELS_PATH,
            to_path=out,
            as_df=True,
        )

        recommendations = pd.read_csv(out)
        expected_columns = list(self.recommendations.columns)
        expected_dtypes = self.recommendations.dtypes.astype(str).to_dict()

        # Compare the column names
        self.assertListEqual(list(recommendations.columns), expected_columns)
        self.assertListEqual(list(df_recommendations.columns), expected_columns)
        # Compare the data types of each column
        self.assertDictEqual(
            recommendations.dtypes.astype(str).to_dict(), expected_dtypes
        )


class BenchmarkTests:
    """
    This class contains a basic benchmarking tests for the ScholarlyRecommender package.
    The benchmarking tests are run under the assumption that the configuration is valid.

    Gives the runtime and memory usage of each function in the package, as well as the total runtime and memory usage for the whole pipeline.

    """

    def __init__(self):
        self.config = sr.get_config()
        self.candidates = pd.read_csv(REF_CANDIDATES_PATH)
        self.candidates_labeled = pd.read_csv(REF_LABELS_PATH)
        self.recommendations = pd.read_csv(REF_RECOMMENDATIONS_PATH)

    def benchmark(self, save_log=False):
        print(f"\n Running benchmarks... \n")
        times = []
        memory = []
        tracemalloc.start()
        full_start_time = time.time()

        start_time = time.time()
        can = sr.source_candidates(
            queries=self.config["queries"],
            as_df=True,
            prev_days=7,
        )
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        memory.append(tracemalloc.get_traced_memory())
        self._display(
            "Source Candidates",
            times[0],
            memory[0][0],
            memory[0][1],
        )

        start_time = time.time()
        rec = sr.get_recommendations(
            data=REF_CANDIDATES_PATH,
            labels=REF_LABELS_PATH,
            as_df=True,
        )
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        memory.append(tracemalloc.get_traced_memory())
        self._display(
            "Get Recommendations",
            times[1],
            memory[1][0] - memory[0][0],
            memory[1][1],
        )

        start_time = time.time()
        fee = sr.get_feed(
            data=REF_RECOMMENDATIONS_PATH,
            to_path=TEST_FEED_OUT,
        )
        elapsed_time = time.time() - start_time

        times.append(elapsed_time)
        memory.append(tracemalloc.get_traced_memory())
        self._display(
            "Get Feed",
            times[2],
            memory[2][0] - memory[1][0],
            memory[2][1],
        )

        full_time = time.time() - full_start_time
        tracemalloc.stop()
        self._display(
            "Total",
            full_time,
            memory[2][0],
            memory[2][1],
        )
        if save_log:
            return times, memory

    @staticmethod
    def _display(name, runtime, current_memory, peak_memory):
        print(
            f"{name} \n Runtime: {runtime} seconds \n Memory: {current_memory} bytes in current memory, {peak_memory} bytes in peak memory \n"
        )


if __name__ == "__main__":
    unittest.main()
    # BenchmarkTests().benchmark()
