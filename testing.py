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


# Unit Tests
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

        # Test the queries
        config_queries = self.config["queries"]
        self.assertTrue(isinstance(config_queries, list))
        self.assertTrue(len(config_queries) > 0)
        self.assertTrue(all(isinstance(item, str) for item in config_queries))

        # Test the labels
        config_labels = pd.read_csv(self.config["labels"])
        expected_columns = list(self.candidates_labeled.columns)
        columns = list(config_labels.columns)
        self.assertEqual(columns, expected_columns)

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


class ManualTests:
    """
    MANUAL TESTS

    These tests are for manual testing of the ScholarlyRecommender package.
    They are not run automatically when the tests are run. Usefull for debugging.
    """

    def __init__(self):
        self.config = sr.get_config()
        self.candidates = pd.read_csv(REF_CANDIDATES_PATH)
        self.candidates_labeled = pd.read_csv(REF_LABELS_PATH)
        self.recommendations = pd.read_csv(REF_RECOMMENDATIONS_PATH)

    def run_all(self):
        can = sr.source_candidates(
            queries=self.config["queries"],
            as_df=True,
            prev_days=7,
        )
        rec = sr.get_recommendations(
            data=REF_CANDIDATES_PATH,
            labels=REF_LABELS_PATH,
            as_df=True,
        )
        fee = sr.get_feed(
            data=REF_RECOMMENDATIONS_PATH,
            to_path="man_test.html",
        )

    # Test speed of recommendation function
    def performance_test(self, n: int = 1):
        times = []
        memory = []
        peaks = []
        for i in range(n):
            tracemalloc.start()
            start_time = time.time()

            rec = sr.get_recommendations(
                data=REF_CANDIDATES_PATH,
                labels=REF_LABELS_PATH,
                as_df=True,
            )
            end_time = time.time()
            mem = tracemalloc.get_traced_memory()

            elapsed_time = end_time - start_time
            memory.append(mem)
            peaks.append(tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
            times.append(elapsed_time)
            print(f"Elapsed time for test_get_recommendations: {elapsed_time} seconds")
            print(f"Memory for test_get_recommendations: {mem} bytes")
        print(f"Average time: {sum(times)/len(times)} seconds")
        print(f"Average memory: {sum(peaks)/len(peaks)} bytes")


if __name__ == "__main__":
    unittest.main()
    # mt = ManualTests().run_all()
    # ManualTests().performance_test(n=5)
