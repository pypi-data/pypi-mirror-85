import unittest
from pfx_insights import feature_generation_utils as fgu

def test_get_days_delta():
    utils = fgu.FeatureGenerationUtils()
    assert utils.get_days_delta('20200907', '20200909') == 2