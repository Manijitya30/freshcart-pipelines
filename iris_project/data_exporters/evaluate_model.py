"""C3: evaluation branch. Runs in parallel with save_results (both depend on train_model)."""
import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_recall_fscore_support)

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

NAMES = ['setosa', 'versicolor', 'virginica']


@data_exporter
def export_data(output, *args, **kwargs) -> None:
    p = output['predictions']
    cm = confusion_matrix(p['target'], p['predicted'], labels=[0, 1, 2])
    print('Confusion matrix (rows = true, columns = predicted):')
    print(pd.DataFrame(cm, index=NAMES, columns=NAMES))

    prec, rec, f1, support = precision_recall_fscore_support(
        p['target'], p['predicted'], labels=[0, 1, 2], zero_division=0)
    metrics = pd.DataFrame({'precision': prec, 'recall': rec,
                            'f1': f1, 'support': support}, index=NAMES).round(3)
    print('\nMetrics per class:')
    print(metrics)
    print(f"\nAccuracy: {accuracy_score(p['target'], p['predicted']):.4f}")
    metrics.to_csv('iris_metrics.csv')


@test
def test_metrics_written(*args) -> None:
    import os
    assert os.path.exists('iris_metrics.csv'), 'iris_metrics.csv was not created'
