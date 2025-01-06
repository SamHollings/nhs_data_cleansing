from datetime import datetime
import inflection
from pyspark.sql import types as T, functions as F, DataFrame, Column
from typing import Union


def clean_schema(df, column_renames=None):
    """
    Takes a dataframe and an optional mapping of column renames, and returns a dataframe with each column \
    renamed to the new name if specified, \
    otherwise to a snake_case version of the old name.
    """
    column_renames = {} if column_renames is None else column_renames
    for field in df.schema.fields:
        df = df.withColumnRenamed(
            field.name,
            column_renames[field.name]
            if field.name in column_renames
            else inflection.underscore(field.name),
        )
    return df


def get_last_ingest_timestamp(filesystem):
    """
    Takes in the fileystem of a TransformInput and returns the timestamp of the latest ingested file.
    filesystem: fileystem of a TransformInput (e.g. input.filesystem())
    """
    last_ingest_date = max(map(lambda status: status.modified, filesystem.ls()))
    return datetime.fromtimestamp(last_ingest_date / 1000.0)


def cast_columns(dataframe: DataFrame, schema: T.StructType) -> DataFrame:
    """
    Takes in the dataframe and casts its columns to the expected schema.
    This function will trim whitespace from columns before attempting the cast.
    dataframe: the dataframe to cast the columns of
    schema: the schema to use in casting
    """
    for col in schema.fields:
        dataframe = dataframe.withColumn(
            col.name, trim_and_empty_string_to_null(col.name)
        )
    dataframe = dataframe.select(
        *[F.col(col.name).cast(col.dataType) for col in schema.fields]
    )
    return dataframe


def trim_and_empty_string_to_null(col: Union[str, Column]):
    """
    Trims whitespace from a column and converts to null in the case the column is now empty
    col: the Column or column name to trim
    """
    if isinstance(col, str):
        col = F.col(col)
    col = F.trim(col)
    return F.when(col == "", F.lit(None)).otherwise(col).cast("string")


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


def convert_text_to_camel_case(string_col: Column) -> Column:
    """
    This function takes an input text column `string_col` and converts it into camel_case. Special characters
    (e.g. not an uppercase or lowercase letter, number or space character) will be dropped from the input string.
    The string is then cast to lowercase and the spaces replaced with '_'.
    string_col: input string column that we want to camelcase-ify
    """
    special_chars = r"[^a-zA-Z0-9\s_]"
    col = F.regexp_replace(string_col, special_chars, "")
    return F.lower(
        F.regexp_replace(col, r"\s+", "_")
    )  # replace sequences of at least one space with a '_'


def clean_ods_code(col):
    """
    This function takes a column containing ods codes and cleans the ods codes by
    removing any non-alphanumeric characters and covernting all letters to uppercase.
    If the column is then empty it is converted to null.
    col: the Column or column name to clean
    """
    if isinstance(col, str):
        col = F.col(col)
    col = F.upper(F.regexp_replace(col, r"[^a-zA-Z0-9]", ""))
    return F.when(col == "", F.lit(None)).otherwise(col).cast("string")
