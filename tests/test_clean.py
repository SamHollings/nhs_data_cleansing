from pyspark.sql import functions as F
from pyspark.sql import types as T

import src.nhs_data_cleansing.clean as clean


def test_nhs_number(spark_session):
    df = spark_session.createDataFrame(
        [
            ["1234512343", True],
            ["4010232137", True],
            ["1234512344", False],
            ["4010232134", False],
            ["", False],
            ["40102321341", False],
            ["401023213a", False],
            ["4010a32131", False],
            ["a", False],
        ],
        ["col", "expected"],
    )
    df = clean.check_nhs_number(df, "col", "result")
    assert df.where(F.col("result") != F.col("expected")).count() == 0
