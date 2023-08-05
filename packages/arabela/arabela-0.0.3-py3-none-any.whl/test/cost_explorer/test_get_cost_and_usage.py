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
from arabela.cost_explorer import get_cost_and_usage as ce


class TimePeriodTestCase(unittest.TestCase):

    def test_time_period(self):
        tp = ce.TimePeriod()
        assert hasattr(tp, 'Start')
        assert hasattr(tp, 'End')

        today = date.today()
        print(tp.asdict)
        assert today.strftime('%F') == tp.asdict['Start']
        assert today.strftime('%F') == tp.asdict['End']

    def test_start(self):
        tp = ce.TimePeriod(Start='1970-01-01')
        assert tp.Start == '1970-01-01'

    def test_end(self):
        tp = ce.TimePeriod(End='1970-01-01')
        assert tp.End == '1970-01-01'


class OptionsTestCase(unittest.TestCase):

    def test_options(self):
        option = ce.Options()
        assert hasattr(option, 'TimePeriod')
        assert hasattr(option, 'Granularity')
        assert hasattr(option, 'Filter')
        assert hasattr(option, 'Metrics')

        assert not option.asdict.get('Filter', None)
        assert not option.asdict.get('Metrics', None)
        assert 'DAILY' == option.Granularity

    def test_time_period(self):
        with self.assertRaises(TypeError):
            ce.Options(TimePeriod=dict(Start='2020-01-01', End='2020-01-31'))

        with self.assertRaises(TypeError):
            ce.Options(TimePeriod=10)

        assert ce.Options(TimePeriod=ce.TimePeriod())

    def test_filter(self):
        option = ce.Options(Filter=ce.Filter(
            Dimensions={'Key': 'REGION', 'Values': ['us-west-1']}))
        assert 'Dimensions' in option.asdict['Filter']
        assert 'REGION' == option.asdict['Filter']['Dimensions']['Key']

    def test_metrics(self):
        option = ce.Options(
            Metrics=[ce.Metrics.AmortizedCost, ce.Metrics.BlendedCost])
        assert 'AmortizedCost' in option.Metrics

    def test_group_by(self):
        with self.assertRaises(ValueError):
            ce.Options(GroupBy=ce.GroupBy(Type='DIMENSION', Key='foo'))
        assert ce.Options(GroupBy=ce.GroupBy(Type='DIMENSION', Key='SERVICE'))
