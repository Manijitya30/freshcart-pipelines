"""C4 (own block): data-quality gate between load_iris and prepare_data."""
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    # Pass the data through unchanged. The @test below is the actual gate.
    return df


@test
def test_no_missing_values(df, *args) -> None:
    n = int(df.isnull().sum().sum())
    assert n == 0, f'found {n} missing values'


@test
def test_three_classes(df, *args) -> None:
    classes = sorted(df['target'].unique())
    assert len(classes) == 3, f'expected exactly 3 classes, found {classes}'
