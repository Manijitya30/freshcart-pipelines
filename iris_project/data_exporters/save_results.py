import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

OUT = 'iris_predictions.csv'


@data_exporter
def export_data(output, *args, **kwargs) -> None:
    output['predictions'].to_csv(OUT, index=False)
    print(f'saved {len(output["predictions"])} rows to {OUT}')


@test
def test_file_written(*args) -> None:
    assert os.path.exists(OUT), f'{OUT} was not created'
