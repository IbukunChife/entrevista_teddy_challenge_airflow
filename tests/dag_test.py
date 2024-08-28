import pytest
from unittest.mock import patch, MagicMock
from airflow.models import DagBag
from dags.teddy_dag import fetch_data, store_data


@pytest.fixture
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)


def test_dag_import(dagbag):
    print("DAGBag: ", dagbag.dags)
    assert "teddy_dag" in dagbag.dags
    assert len(dagbag.import_errors) == 0
