import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

MIN_ACCURACY = 0.90   # the quality gate for C2


@transformer
def transform(df, *args, **kwargs):
    """Train a decision tree. max_depth comes from --runtime-vars (default 3)."""
    max_depth = int(kwargs.get('max_depth', 3))
    features = [c for c in df.columns if c not in ('target', 'split')]
    train, test_ = df[df['split'] == 'train'], df[df['split'] == 'test']

    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train[features], train['target'])
    pred = model.predict(test_[features])
    acc = float(accuracy_score(test_['target'], pred))
    print(f'max_depth={max_depth}  test_accuracy={acc:.4f}')

    predictions = test_[features + ['target']].copy()
    predictions['predicted'] = pred
    return {'max_depth': max_depth, 'accuracy': acc, 'predictions': predictions}


@test
def test_accuracy(output, *args) -> None:
    acc = output['accuracy']
    assert acc >= MIN_ACCURACY, f'test accuracy {acc:.3f} is below {MIN_ACCURACY}'
