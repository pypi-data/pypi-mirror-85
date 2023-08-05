import shutil
import unittest

import logging
import pandas as pd

from ..timeseries import TimeSeries
from ..logging import get_logger

logger = get_logger(__name__)

try:
    from ..models.transformer_model import _TransformerModule, TransformerModel
    TORCH_AVAILABLE = True
except ImportError:
    logger.warning('Torch not available. Transformer tests will be skipped.')
    TORCH_AVAILABLE = False


if TORCH_AVAILABLE:
    class TransformerModelTestCase(unittest.TestCase):
        __test__ = True
        times = pd.date_range('20130101', '20130410')
        pd_series = pd.Series(range(100), index=times)
        series: TimeSeries = TimeSeries.from_series(pd_series)
        series_multivariate = series.stack(series * 2)
        module = _TransformerModule(input_size=1,
                                    input_length=1,
                                    output_length=1,
                                    output_size=1,
                                    d_model=512,
                                    nhead=8,
                                    num_encoder_layers=6,
                                    num_decoder_layers=6,
                                    dim_feedforward=2048,
                                    dropout=0.1,
                                    activation="relu",
                                    custom_encoder=None,
                                    custom_decoder=None,
                                    )

        @classmethod
        def setUpClass(cls):
            logging.disable(logging.CRITICAL)

        @classmethod
        def tearDownClass(cls):
            shutil.rmtree('.darts')

        def test_creation(self):
            with self.assertRaises(ValueError):
                # cannot input anything beside 'None' or a PyTorch 'nn.Module'
                TransformerModel(model='Invalid Input')
            # can give a custom module
            model1 = TransformerModel(self.module)
            model2 = TransformerModel()
            self.assertEqual(model1.model.__repr__(), model2.model.__repr__())

        def test_fit(self):
            # Test basic fit()
            model = TransformerModel(n_epochs=2)
            model.fit(self.series)

            # Test fit-save-load cycle
            model2 = TransformerModel(n_epochs=4, model_name='unittest-model-transformer')
            model2.fit(self.series)
            model_loaded = model2.load_from_checkpoint(model_name='unittest-model-transformer', best=False)
            pred1 = model2.predict(n=6)
            pred2 = model_loaded.predict(n=6)

            # Two models with the same parameters should deterministically yield the same output
            self.assertEqual(sum(pred1.values() - pred2.values()), 0.)

            # Another random model should not
            model3 = TransformerModel(n_epochs=2)
            model3.fit(self.series)
            pred3 = model3.predict(n=6)
            self.assertNotEqual(sum(pred1.values() - pred3.values()), 0.)

            # test short predict
            pred4 = model3.predict(n=1)
            self.assertEqual(len(pred4), 1)

            # test validation series input
            model3.fit(self.series[:60], val_training_series=self.series[60:], val_target_series=self.series[60:])
            pred4 = model3.predict(n=6)
            self.assertEqual(len(pred4), 6)

            shutil.rmtree('.darts')

        @staticmethod
        def helper_test_use_full_output_length(test_case, pytorch_model, series):
            model = pytorch_model(n_epochs=2, output_length=3)
            model.fit(series)
            pred = model.predict(7, True)
            test_case.assertEqual(len(pred), 7)
            pred = model.predict(2, True)
            test_case.assertEqual(len(pred), 2)
            test_case.assertEqual(pred.width, 1)
            pred = model.predict(4, True)
            test_case.assertEqual(len(pred), 4)
            test_case.assertEqual(pred.width, 1)

        def test_use_full_output_length(self):
            TransformerModelTestCase.helper_test_use_full_output_length(self, TransformerModel, self.series)

        @staticmethod
        def helper_test_multivariate(test_case, pytorch_model, series_multivariate):
            model = pytorch_model(n_epochs=2)
            # trying to fit multivariate series with input_size=1
            with test_case.assertRaises(ValueError):
                model.fit(series_multivariate, series_multivariate["0"])
            model = pytorch_model(n_epochs=2, input_size=2, output_length=3)
            # output size is 1 while should be 2 here
            with test_case.assertRaises(ValueError):
                model.fit(series_multivariate)
            # fit function called with valid parameters
            model.fit(series_multivariate, series_multivariate["0"])
            # use_full_output_length not set to True
            with test_case.assertRaises(ValueError):
                pred = model.predict(n=1)
            # n > output_length
            with test_case.assertRaises(ValueError):
                pred = model.predict(4, True)
            # predict called with valid parameters
            pred = model.predict(3, True)
            test_case.assertEqual(pred.width, 1)
            test_case.assertEqual(len(pred), 3)
            pred = model.predict(2, True)
            test_case.assertEqual(len(pred), 2)
            # target_series.width != output_size
            with test_case.assertRaises(ValueError):
                model.fit(series_multivariate, series_multivariate[["0", "1"]])
            model = pytorch_model(n_epochs=2, input_size=2, output_length=2, output_size=2)
            # fit and predict called with valid parameters
            model.fit(series_multivariate, series_multivariate[["0", "1"]])
            pred = model.predict(2, True)
            test_case.assertEqual(pred.width, 2)

        def test_multivariate(self):
            TransformerModelTestCase.helper_test_multivariate(self, TransformerModel, self.series_multivariate)
