'''
aws ce get-cost-and-usage
    --time-period <value>
    [--granularity <value>]
    [--filter <value>]
    --metrics <value>
    [--group-by <value>]
    [--next-page-token <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]
'''
import unittest
from datetime import date

import attr
from sdk.cost_explorer.get_cost_and_usage import (Filter, Metrics, Options,
                                                  TimePeriod)


class TimePeriodTestCase(unittest.TestCase):

    def test_time_period(self):
        tp = TimePeriod()
        assert hasattr(tp, 'Start')
        assert hasattr(tp, 'End')

        today = date.today()
        print(tp.asdict)
        assert today.strftime('%F') == tp.asdict['Start']
        assert today.strftime('%F') == tp.asdict['End']

    def test_start(self):
        tp = TimePeriod(Start='1970-01-01')
        assert tp.Start == '1970-01-01'

    def test_end(self):
        tp = TimePeriod(End='1970-01-01')
        assert tp.End == '1970-01-01'


class OptionsTestCase(unittest.TestCase):

    def test_options(self):
        option = Options()
        assert hasattr(option, 'TimePeriod')
        assert hasattr(option, 'Granularity')
        assert hasattr(option, 'Filter')
        assert hasattr(option, 'Metrics')

        assert not option.asdict.get('Filter', None)
        assert not option.asdict.get('Metrix', None)
        assert 'DAILY' == option.Granularity

    def test_time_period(self):
        with self.assertRaises(TypeError):
            Options(TimePeriod=dict(Start='2020-01-01', End='2020-01-31'))

        with self.assertRaises(TypeError):
            Options(TimePeriod=10)

        assert Options(TimePeriod=TimePeriod())

    def test_filter(self):
        option = Options(Filter=Filter(
            Dimensions={'Key': 'REGION', 'Values': ['us-west-1']}))
        assert 'Dimensions' in option.asdict['Filter']
        assert 'REGION' == option.asdict['Filter']['Dimensions']['Key']

    def test_metrics(self):
        option = Options(Metrics=[Metrics.AmortizedCost, Metrics.BlendedCost])
        assert 'AmortizedCost' in option.Metrics
