import pandas as pd
from sklearn.datasets import load_iris as _sk_load_iris

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs) -> pd.DataFrame:
    """Load the 150-row Iris data set as a DataFrame (4 features + 'target')."""
    return _sk_load_iris(as_frame=True).frame


@test
def test_output(df, *args) -> None:
    assert df is not None, 'The output is undefined'
    assert len(df) == 150, f'expected 150 rows, got {len(df)}'
    assert 'target' in df.columns, "missing 'target' column"
