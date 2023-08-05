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
import typing
import unittest
from datetime import date
from enum import Enum

import attr


class StrEnum(Enum):

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class AsDict:

    @property
    def asdict(self):
        return attr.asdict(
            self,
            # recurse=True,
            filter=lambda _, x: True if x is not None else False,
        )


@attr.s
class TimePeriod(AsDict):
    Start: str = attr.ib(default=date.today(), converter=str)
    End: str = attr.ib(default=date.today(), converter=str)


class Granularity(StrEnum):
    DAILY = 'DAILY'
    MONTHLY = 'MONTHLY'
    HOURLY = 'HOURLY'


@attr.s
class Filter:
    Or: typing.List[str] = attr.ib(default=None)
    And: typing.List[str] = attr.ib(default=None)
    Not: dict = attr.ib(default=None)
    Dimensions: dict = attr.ib(default=None)
    Tags: dict = attr.ib(default=None)
    CostCategories: dict = attr.ib(default=None)


class Metrics(StrEnum):
    AmortizedCost = 'AmortizedCost'
    BlendedCost = 'BlendedCost'
    NetAmortizedCost = 'NetAmortizedCost'
    NetUnblendedCost = 'NetUnblendedCost'
    NormalizedUsageAmount = 'NormalizedUsageAmount'
    UnblendedCost = 'UnblendedCost'
    UsageQuantity = 'UsageQuantity'


@attr.s
class GroupBy:
    Type: str = attr.ib(
        default=None,
        converter=attr.converters.optional(str),
        validator=attr.validators.optional(
            attr.validators.in_([
                'AZ', 'INSTANCE_TYPE', 'LEGAL_ENTITY_NAME', 'LINKED_ACCOUNT',
                'OPERATION', 'PLATFORM', 'PURCHASE_TYPE', 'SERVICE', 'TAGS',
                'TENANCY', 'RECORD_TYPE', 'USAGE_TYPE'])))
    Key: str = attr.ib(default=None)


@attr.s
class Options(AsDict):
    TimePeriod: TimePeriod = attr.ib(
        default=TimePeriod(),
        validator=attr.validators.instance_of(TimePeriod))
    Granularity: Granularity = attr.ib(
        default=Granularity.DAILY,
        converter=lambda item: item.value,
        validator=attr.validators.instance_of(str))
    Filter: Filter = attr.ib(default=None)
    Metrics: typing.List[str] = attr.ib(
        default=None,
        converter=attr.converters.optional(
            lambda items: [item.value for item in items]),
        validator=attr.validators.optional(
            attr.validators.deep_iterable(
                member_validator=attr.validators.instance_of(str),
                iterable_validator=attr.validators.instance_of(list))))
    GroupBy: GroupBy = attr.ib(default=None, converter=GroupBy)
    NextPageToken: str = None
    CliInputJson: str = None
    GenerateCliSkeleton: str = None
