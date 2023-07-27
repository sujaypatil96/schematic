from multiprocessing.sharedctypes import Value
import os
import logging
import sys

import shutil
import pytest
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from schematic.schemas.explorer import SchemaExplorer
from schematic.configuration.configuration import CONFIG
from schematic.utils.df_utils import load_df

load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Silence some very verbose loggers
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("googleapiclient").setLevel(logging.INFO)
logging.getLogger("google_auth_httplib2").setLevel(logging.INFO)


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TESTS_DIR, "data")

@pytest.fixture(scope="session")
def dataset_id():
    yield "syn25614635"


# This class serves as a container for helper functions that can be
# passed to individual tests using the `helpers` fixture. This approach
# was required because fixture functions cannot take arguments.
class Helpers:
    @staticmethod
    def get_data_path(path, *paths):
        return os.path.join(DATA_DIR, path, *paths)

    @staticmethod
    def get_data_file(path, *paths, **kwargs):
        fullpath = os.path.join(DATA_DIR, path, *paths)
        return open(fullpath, **kwargs)

    @staticmethod
    def get_data_frame(path, *paths, **kwargs):
        fullpath = os.path.join(DATA_DIR, path, *paths)
        return load_df(fullpath, **kwargs)

    @staticmethod
    def get_schema_explorer(path=None, *paths):
        if path is None:
            return SchemaExplorer()

        fullpath = Helpers.get_data_path(path, *paths)

        se = SchemaExplorer()
        se.load_schema(fullpath)
        return se

    @staticmethod
    def get_python_version(self):
        version=sys.version
        base_version=".".join(version.split('.')[0:2])

        return base_version

    @staticmethod
    def get_python_project(self):

        version = self.get_python_version(Helpers)

        python_projects = {
            "3.7":  "syn47217926",
            "3.8":  "syn47217967",
            "3.9":  "syn47218127",
            "3.10": "syn47218347",
        }

        return python_projects[version]

@pytest.fixture(scope="session")
def helpers():
    yield Helpers

@pytest.fixture(scope="session")
def config():
    yield CONFIG
