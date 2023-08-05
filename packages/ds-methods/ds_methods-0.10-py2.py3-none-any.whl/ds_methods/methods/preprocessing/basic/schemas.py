from schema import Schema, And, Use, Or, Optional

from ds_methods.common.enums import BaseEnum


class BasicMethod(BaseEnum):
    MIN = 'min'
    MAX = 'min'
    MEAN = 'mean'
    MEDIAN = 'median'
    STD = 'std'
    QUANTILE = 'quantile'


options_schema = Schema(
    And({
        'method': And(
            str,
            lambda x: BasicMethod.validate(x),
        ),
        Optional('q'): And(
            Or(float, [float]),
            And(
                Use(lambda x: x if isinstance(x, list) else [x]),
                lambda x: 0 <= min(x) and max(x) <= 1,
            ),
        ),
    }, lambda x: (x['method'] != 'quantile') or ('q' in x)),
    ignore_extra_keys=True,
)
