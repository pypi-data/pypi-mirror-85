"""named spark data frames"""

from pandas import DataFrame as PandasDataFrame


class PandasNamedFrame(PandasDataFrame):
    def __init__(self, pandas_df):
        super().__init__(pandas_df)
        self._validate()

    def _validate(self):
        missing_columns = []
        for column_name, column_type in self.__annotations__.items():
            if column_name not in self.columns:
                missing_columns.append((column_name, column_type))
        if missing_columns:
            raise ValueError(f"missing columns: {missing_columns}")
