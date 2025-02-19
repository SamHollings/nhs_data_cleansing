from datetime import datetime
from typing import Union

import inflection
from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T


def check_nhs_number(df: DataFrame, num_col: str, result_col: str):
    """
    Adds a column indicating if the num_col is a valid nhs number using the checksum
    df: the dataframe to use
    num_col: the column containing the possible nhs number
    result_col: the name of the new boolean column to add, true if the num_col is a valid
    nhs number, otherwise false
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
