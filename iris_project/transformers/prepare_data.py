from sklearn.model_selection import train_test_split

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """Add a 'split' column: 80% 'train', 20% 'test' (stratified, fixed seed)."""
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=42, stratify=df['target']
    )
    out = df.copy()
    out['split'] = 'train'
    out.loc[test_idx, 'split'] = 'test'
    return out


@test
def test_split_sizes(df, *args) -> None:
    assert (df['split'] == 'train').sum() == 120
    assert (df['split'] == 'test').sum() == 30
