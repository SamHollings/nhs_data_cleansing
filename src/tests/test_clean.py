from src.nhs_foundry_common.clean import (
    clean_schema,
    cast_columns,
    trim_and_empty_string_to_null,
    check_nhs_number,
    convert_text_to_camel_case,
)
from pyspark.sql import types as T
from pyspark.sql import functions as F


def test_clean_schema(spark_session):
    df = spark_session.createDataFrame(
        [["a", "a", "a"]], ["standard_column", "NonStandardColumn", "Explicit_Column"]
    )
    renamed_col_name = "explicit_column_renamed"
    df = clean_schema(df, {"Explicit_Column": renamed_col_name})
    assert df.schema.names == [
        "standard_column",
        "non_standard_column",
        renamed_col_name,
    ]


def test_cast_columns(spark_session):
    df = spark_session.createDataFrame(
        [["a", "1", 1], [" b ", "2 ", 2], ["   ", "3", 3]],
        [
            "string_col",
            "integer_col",
        ],
    )
    cast_schema = T.StructType(
        [
            T.StructField("string_col", T.StringType()),
            T.StructField("integer_col", T.IntegerType()),
        ]
    )

    df = cast_columns(df, cast_schema)

    assert df.dtypes == [("string_col", "string"), ("integer_col", "int")]
    assert (
        df.where((F.col("string_col") == "a") & (F.col("integer_col") == 1)).count()
        == 1
    )
    assert (
        df.where((F.col("string_col") == "b") & (F.col("integer_col") == 2)).count()
        == 1
    )
    assert (
        df.where((F.col("string_col").isNull()) & (F.col("integer_col") == 3)).count()
        == 1
    )


def test_cast_columns_for_already_cast_columns(spark_session):
    df = spark_session.createDataFrame([[1], [2]], ["int_col"])
    cast_schema = T.StructType([T.StructField("int_col", T.IntegerType())])

    df = cast_columns(df, cast_schema)

    assert df.dtypes == [("int_col", "int")]
    assert df.where((F.col("int_col") == 1)).count() == 1
    assert df.where((F.col("int_col") == 2)).count() == 1


def test_trim_and_empty_string_to_null(spark_session):
    df = spark_session.createDataFrame(
        [["a", "a"], [" b ", "b"], ["   ", None]], ["col", "expected"]
    )
    df = df.withColumn("result", trim_and_empty_string_to_null("col"))
    assert df.where(F.col("result") != F.col("expected")).count() == 0


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
    df = check_nhs_number(df, "col", "result")
    assert df.where(F.col("result") != F.col("expected")).count() == 0


def test_convert_text_to_camel_case(spark_session):
    df = spark_session.createDataFrame(
        [
            ["1234512345", "1234512345"],
            ["Free Text", "free_text"],
            ["S0m£ R@nD0m T£xt", "s0m_rnd0m_txt"],
            ["camel_case", "camel_case"],
            ["", ""],
            ["!^_", "_"],
            ["Lots      Of      Spaces", "lots_of_spaces"],
        ],
        ["col", "expected"],
    )
    df = df.withColumn("result", convert_text_to_camel_case(F.col("col")))
    assert df.where(F.col("result") != F.col("expected")).count() == 0
