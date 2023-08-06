from typing import Dict, List, Tuple
from numbers import Number
import pandas as pd
from pandas import DataFrame

from .constants import MIN_ROWS_FOR_ACC


class DataFrameUtils:
    @staticmethod
    def get_query_value(value) -> str:
        if not isinstance(value, Number):
            return f"'{value}'"

        return f"{value}"

    @staticmethod
    def compose_query(options: Dict[str, Dict]) -> str:
        filters = []
        for key in options:
            key_options = options[key]
            if 'equal' in key_options:
                filters.append(f"{key} == {DataFrameUtils.get_query_value(key_options['equal'])}")
            else:
                if 'gte' in key_options:
                    filters.append(f"{key} >= {DataFrameUtils.get_query_value(key_options['gte'])}")
                if 'lte' in key_options:
                    filters.append(f"{key} <= {DataFrameUtils.get_query_value(key_options['lte'])}")

        return ' and '.join(filters)

    @staticmethod
    def eval_query(input_data: DataFrame, query: str) -> DataFrame:
        """
        'python' engine is faster for a small data
        """
        if len(input_data.index) < MIN_ROWS_FOR_ACC:
            return input_data.query(query, engine='python')

        return input_data.query(query)

    @staticmethod
    def concatenate(parts: List[DataFrame]) -> DataFrame:
        return pd.concat(
            [part.reset_index(drop=True) for part in parts],
            sort=False,
            axis='columns',
            copy=False,
        ).dropna(how='all').reset_index(drop=True)

    @staticmethod
    def decompose(input_data: DataFrame, include: List[str] = None) -> Tuple[DataFrame, DataFrame]:
        if not include:
            include = ['number']

        return input_data.select_dtypes(include=include), input_data.select_dtypes(exclude=include)

    @staticmethod
    def fillna(input_data: DataFrame) -> DataFrame:
        data = input_data.copy()
        numeric_part, other_part = DataFrameUtils.decompose(data)
        data[numeric_part.columns] = data[numeric_part.columns].fillna(0)
        data[other_part.columns] = data[other_part.columns].fillna('')

        return data

    @staticmethod
    def repeat_rows(input_data: DataFrame, n_repeat: int) -> DataFrame:
        return input_data.loc[input_data.index.repeat(n_repeat)].reset_index(drop=True)
