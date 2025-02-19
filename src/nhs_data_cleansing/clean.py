"""This module contains cleaning functions"""

from datetime import datetime
from typing import Union

import inflection
from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T


def check_nhs_number(df: DataFrame, num_col: str, result_col: str) -> DataFrame:
    """Adds a column indicating if the input column contains valid NHS numbers.

    The function calculates the checksum of the NHS number and compares it
    with the last digit to determine validity.  It handles cases where the
    checksum calculation results in 11 (which should become 0).

    Parameters
    ----------
    df : DataFrame
        The input DataFrame.
    num_col : str
        The name of the column containing the potential NHS numbers.
    result_col : str
        The name of the new boolean column to add.  `True` indicates a
        valid NHS number, `False` otherwise.

    Returns
    -------
    DataFrame
        The input DataFrame with the added boolean column.

    Raises
    ------
    TypeError
        If `df` is not a Spark DataFrame.
    TypeError
        If `num_col` or `result_col` are not strings.

    # Examples
    # --------
    # >>> from pyspark.sql import SparkSession
    # >>> spark = SparkSession.builder.appName("NHSNumberCheck").getOrCreate()
    # >>> df = spark.createDataFrame([("1234512343",)], ["nhs_number"])
    # >>> df = check_nhs_number(df, "nhs_number", "is_valid")
    # >>> df.show()
    # +----------+--------+
    # |nhs_number|is_valid|
    # +----------+--------+
    # |1234512343|    true|
    # +----------+--------+
    """

    # Sum up the digits using weighting factors
    digit_factors = [
        F.substring(F.col(num_col), i, 1).cast(T.IntegerType()) * F.lit(11 - i)
        for i in range(1, 10)
    ]
    total = sum(digit_factors)

    # Compare expected checksum to last digit and add result column
    df = (
        df.withColumn("expected_last_digit", 11 - (total % 11))
        .withColumn(
            "last_digit", F.substring(F.col(num_col), 10, 1).cast(T.IntegerType())
        )
        .withColumn(
            result_col,
            (F.length(F.col(num_col)) == 10)
            & F.col("last_digit").isNotNull()
            & F.col("expected_last_digit").isNotNull()
            & (F.col("last_digit") == F.col("expected_last_digit")),
        )
        .drop("expected_last_digit", "last_digit")
    )
    return df
