"""named spark data frames"""

from pyspark.sql import SQLContext, SparkSession, DataFrame as SparkDataFrame
from pyspark.ml.common import _py2java


class SparkNamedFrame(SparkDataFrame):
    def __init__(self, spark_df, spark_session=None):
        if spark_session is None:
            spark_session = SparkSession.builder.getOrCreate()
        super().__init__(
            _py2java(spark_session.sparkContext, spark_df),
            SQLContext(spark_session.sparkContext, spark_session),
        )
        self._validate()

    def _validate(self):
        missing_columns = []
        for column_name, column_type in self.__annotations__.items():
            if column_name not in self.columns:
                missing_columns.append((column_name, column_type))
        if missing_columns:
            raise ValueError(f"missing columns: {missing_columns}")
