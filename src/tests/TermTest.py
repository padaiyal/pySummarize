import pdb
from contextlib import redirect_stdout
from unittest import TestCase

from src.summarize import summarize


class TermTest(TestCase):

    temp_file = None

    @classmethod
    def setUpClass(cls):
        cls.temp_file_path = 'temp.txt'
        cls.debug_flag = False

    def assertActualOutputMatchesExpectedOutput(self, test_name, test_details, expected_output_file_path=None):
        if self.debug_flag:
            print(test_name)
            pdb.set_trace()
        if expected_output_file_path is None:
            expected_output_file_path = f'expected_output/{test_name.replace(" ", "").lower()}.txt'
        with open(self.temp_file_path, "w") as temp_file:
            with redirect_stdout(temp_file):
                summarize(**test_details['args'])
        with open(self.temp_file_path, "r") as temp_file:
            temp_op = temp_file.read()
        with open(expected_output_file_path, 'r') as expected_output_file:
            expected_op = expected_output_file.read()
        self.assertEqual(expected_op, temp_op)

    def test_term_summary_1(self):
        # --summary_type fd --file_type CSV --graph_type term --label_regex "normal|neptune"
        test_details = {
                "args": {
                    "summary_type": "fd",
                    "file_type": "CSV",
                    "graph_type": "term",
                    "label_regex": "normal|neptune",
                    "file_path": "data/NSL_KDD.csv"
                },
                "description": "fd csv term label_regex"
            }
        self.assertActualOutputMatchesExpectedOutput('Term Test 1', test_details)

    def test_term_summary_2(self):
        # --summary_type fd --file_type CSV --graph_type term --label_regex "enormal|eneptune"
        test_details = {
                "args": {
                    "summary_type": "fd",
                    "file_type": "CSV",
                    "graph_type": "term",
                    "label_regex": "enormal|eneptune",
                    "file_path": "data/NSL_KDD.csv"
                },
                "description": "fd csv term label_regex"
            }
        self.assertActualOutputMatchesExpectedOutput('Term Test 2', test_details)

    def test_term_summary_3(self):
        # --summary_type fd --file_type CSV --graph_type term --label_column_index -2
        test_details = {
                "args": {
                    "summary_type": "fd",
                    "file_type": "CSV",
                    "graph_type": "term",
                    "label_column_index": -2,
                    "file_path": "data/NSL_KDD.csv"
                },
                "description": "fd csv term label_regex"
            }
        self.assertActualOutputMatchesExpectedOutput('Term Test 3', test_details)

    def test_term_summary_4(self):
        # --summary_type timeline --file_type CSV --graph_type term --legend_column_index -2 --legend_regex "^n\w+"
        # --label_frequency 40 --rows_limit 10000
        test_details = {
                        "args": {
                            "summary_type": "timeline",
                            "file_type": "CSV",
                            "graph_type": "term",
                            "legend_column_index": -2,
                            "legend_regex": r"^n\w+",
                            "label_frequency": 40,
                            "rows_limit": 10000,
                            "file_path": "data/NSL_KDD.csv"
                        },
                        "description": "timeline csv term legend_column_index"
                    }
        self.assertActualOutputMatchesExpectedOutput('Term Test 4', test_details)

    @classmethod
    def tearDownClass(cls):
        pass
