import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence, Tuple

import django
from django.contrib.admin.options import BaseModelAdmin
from django.db import models
from django.db.models import (
    BooleanField,
    DateField,
    DurationField,
    ExpressionWrapper,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    functions,
)
from django.db.models.functions import Cast
from django.utils.html import format_html

from .types import (
    BaseType,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    HTMLType,
    IsNullType,
    MonthType,
    NumberType,
    StringChoiceType,
    StringType,
    WeekDayType,
    YearType,
)

_TYPE_AGGREGATES = defaultdict(
    lambda: [("count", NumberType)],
    {
        StringType: [("count", NumberType)],
        StringChoiceType: [("count", NumberType)],
        NumberType: [
            ("average", NumberType),
            ("count", NumberType),
            ("max", NumberType),
            ("min", NumberType),
            ("std_dev", NumberType),
            ("sum", NumberType),
            ("variance", NumberType),
        ],
        DateTimeType: [
            ("count", NumberType),
            ("max", DateTimeType),
            ("min", DateTimeType),
        ],
        DateType: [("count", NumberType), ("max", DateType), ("min", DateType)],
        DurationType: [
            ("count", NumberType),
            ("average", DurationType),
            ("sum", DurationType),
            ("max", DurationType),
            ("min", DurationType),
        ],
        BooleanType: [("average", NumberType), ("sum", NumberType)],
        YearType: [("count", NumberType), ("average", NumberType)],  # todo min and max
    },
)


_DATE_FUNCTIONS = [
    "is_null",
    "year",
    "quarter",
    "month",
    "day",
    "week_day",
    "month_start",
]
if django.VERSION >= (2, 2):  # pragma: no branch
    _DATE_FUNCTIONS += ["iso_year", "iso_week", "week_start"]


_TYPE_FUNCTIONS = defaultdict(
    lambda: ["is_null"],
    {
        DateType: _DATE_FUNCTIONS,
        DateTimeType: _DATE_FUNCTIONS + ["hour", "minute", "second", "date"],
    },
)


class _CastDuration(Cast):
    def __init__(self, expression):
        super().__init__(expression, output_field=DurationField())

    def as_mysql(self, compiler, connection, **extra_context):  # pragma: mysql
        # https://github.com/django/django/pull/13398
        template = "%(function)s(%(expressions)s AS signed integer)"
        return self.as_sql(compiler, connection, template=template, **extra_context)


def _get_django_aggregate(field_type, name):
    if field_type == BooleanType:
        return {
            "average": lambda x: models.Avg(Cast(x, output_field=IntegerField())),
            "sum": lambda x: models.Sum(Cast(x, output_field=IntegerField())),
        }[name]
    if field_type == DurationType and name in ["average", "sum"]:
        return {
            "average": lambda x: models.Avg(_CastDuration(x)),
            "sum": lambda x: models.Sum(_CastDuration(x)),
        }[name]
    else:
        return {
            # these all have result type number
            "average": models.Avg,
            "count": lambda x: models.Count(x, distinct=True),
            "max": models.Max,
            "min": models.Min,
            "std_dev": models.StdDev,
            "sum": models.Sum,
            "variance": models.Variance,
        }[name]


def _get_django_lookup(field_type, lookup, filter_value):
    from .types import StringType

    if lookup == "field_equals":
        lookup, filter_value = filter_value
        return lookup, filter_value
    elif field_type == StringType:
        return (
            {
                "equals": "iexact",
                "regex": "iregex",
                "contains": "icontains",
                "starts_with": "istartswith",
                "ends_with": "iendswith",
                "is_null": "isnull",
            }[lookup],
            filter_value,
        )
    else:
        return (
            {
                "equals": "exact",
                "is_null": "isnull",
                "gt": "gt",
                "gte": "gte",
                "lt": "lt",
                "lte": "lte",
                "contains": "contains",
                "length": "len",
                "has_key": "has_key",
            }[lookup],
            filter_value,
        )


def IsNull(field_name):
    return ExpressionWrapper(Q(**{field_name: None}), output_field=BooleanField())


def _get_django_function(name):
    mapping = {
        "year": (functions.ExtractYear, YearType),
        "quarter": (functions.ExtractQuarter, NumberType),
        "month": (functions.ExtractMonth, MonthType),
        "month_start": (lambda x: functions.TruncMonth(x, DateField()), DateType),
        "day": (functions.ExtractDay, NumberType),
        "week_day": (functions.ExtractWeekDay, WeekDayType),
        "hour": (functions.ExtractHour, NumberType),
        "minute": (functions.ExtractMinute, NumberType),
        "second": (functions.ExtractSecond, NumberType),
        "date": (functions.TruncDate, DateType),
        "is_null": (IsNull, IsNullType),
    }
    if django.VERSION >= (2, 2):  # pragma: no branch
        mapping.update(
            {
                "iso_year": (functions.ExtractIsoYear, YearType),
                "iso_week": (functions.ExtractWeek, NumberType),
                "week_start": (lambda x: functions.TruncWeek(x, DateField()), DateType),
            }
        )
    return mapping[name]


def s(path):
    return "__".join(path)


def get_model_name(model, sep="."):
    return f"{model._meta.app_label}{sep}{model.__name__}"


def get_fields_for_type(type_):
    aggregates = {
        aggregate: OrmAggregateField(type_.name, aggregate, res_type)
        for aggregate, res_type in _TYPE_AGGREGATES[type_]
    }
    functions = {
        func: OrmFunctionField(type_.name, func, _get_django_function(func)[1])
        for func in _TYPE_FUNCTIONS[type_]
    }
    others = {}
    if type_.raw_type:
        others["raw"] = OrmRawField(
            type_.name, "raw", "raw", type_.raw_type, type_.raw_type.name, None
        )

    return {**aggregates, **functions, **others}


@dataclass
class OrmBoundField:
    field: "OrmBaseField"
    previous: "OrmBoundField"
    full_path: Sequence[str]
    pretty_path: Sequence[str]
    queryset_path: Sequence[str]
    aggregate_clause: Tuple[str, models.Func] = None
    filter_: bool = False
    having: bool = False
    model_name: str = None

    @property
    def path_str(self):
        return s(self.full_path)

    @property
    def queryset_path_str(self):
        return s(self.queryset_path)

    @property
    def group_by(self):
        return self.field.can_pivot

    def _lineage(self):
        if self.previous:
            return self.previous._lineage() + [self]
        return [self]

    def annotate(self, request, qs):
        for field in self._lineage():
            qs = field._annotate(request, qs)
        return qs

    def _annotate(self, request, qs):
        return qs

    def __getattr__(self, name):
        return getattr(self.field, name)

    @classmethod
    def blank(cls):
        return cls(
            field=None, previous=None, full_path=[], pretty_path=[], queryset_path=[]
        )

    def get_format_hints(self, data):
        return self.type_.get_format_hints(self.path_str, data)


@dataclass
class OrmModel:
    fields: dict
    admin: BaseModelAdmin = None

    @property
    def root(self):
        return bool(self.admin)

    @property
    def default_filters(self):
        ddb_default_filters = getattr(self.admin, "ddb_default_filters", [])
        assert isinstance(ddb_default_filters, list)
        return [
            (f, l, v if isinstance(v, str) else json.dumps(v))
            for (f, l, v) in ddb_default_filters
        ]


@dataclass
class OrmBaseField:
    model_name: str
    name: str
    pretty_name: str
    type_: BaseType = None
    concrete: bool = False
    rel_name: str = None
    can_pivot: bool = False
    choices: Sequence[Tuple[str, str]] = ()

    def __post_init__(self):
        if not self.type_:
            assert self.rel_name
        if self.concrete or self.can_pivot:
            assert self.type_

    def get_formatter(self):
        return self.type_.get_formatter(self.choices)


class OrmFkField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, rel_name):
        super().__init__(model_name, name, pretty_name, rel_name=rel_name)

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
        )


class OrmConcreteField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, type_, rel_name, choices):
        super().__init__(
            model_name,
            name,
            pretty_name,
            concrete=True,
            type_=type_,
            rel_name=rel_name,
            can_pivot=True,
            choices=choices or (),
        )

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
            filter_=True,
        )


class OrmRawField(OrmConcreteField):
    def bind(self, previous):
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path,
            filter_=True,
        )


class OrmCalculatedField(OrmBaseField):
    def __init__(self, model_name, name, pretty_name, func):
        if getattr(func, "boolean", False):
            type_ = BooleanType
        else:
            type_ = HTMLType

        super().__init__(model_name, name, pretty_name, type_=type_, can_pivot=True)
        self.func = func

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + ["id"],
            model_name=self.model_name,
        )

    def get_formatter(self):
        base_formatter = super().get_formatter()

        def format(obj):
            if obj is None:
                return None

            try:
                value = self.func(obj)
            except Exception as e:
                return str(e)

            return base_formatter(value)

        return format


class OrmBoundAnnotatedField(OrmBoundField):
    def _annotate(self, request, qs):
        from .orm_results import admin_get_queryset

        return qs.annotate(
            **{
                s(self.queryset_path): Subquery(
                    admin_get_queryset(self.admin, request, [self.name])
                    .filter(pk=OuterRef(s(self.previous.queryset_path + ["id"])))
                    .values(self.name)[:1],
                    output_field=self.field_type,
                )
            }
        )


class OrmAnnotatedField(OrmBaseField):
    def __init__(
        self, model_name, name, pretty_name, type_, field_type, admin, choices
    ):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=type_,
            rel_name=type_.name,
            can_pivot=True,
            concrete=True,
            choices=choices or (),
        )
        self.field_type = field_type
        self.admin = admin

    def bind(self, previous):
        previous = previous or OrmBoundField.blank()

        full_path = previous.full_path + [self.name]
        return OrmBoundAnnotatedField(
            field=self,
            previous=previous,
            full_path=full_path,
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=[s(["ddb"] + full_path)],
            filter_=True,
        )


class OrmFileField(OrmConcreteField):
    def __init__(self, model_name, name, pretty_name, django_field):
        super().__init__(
            model_name,
            name,
            pretty_name,
            type_=HTMLType,
            rel_name=HTMLType.name,
            choices=None,
        )
        self.django_field = django_field

    def get_formatter(self):
        def format(value):
            if not value:
                return None

            try:
                # some storage backends will hard fail if their underlying storage isn't
                # setup right https://github.com/tolomea/django-data-browser/issues/11
                return format_html(
                    '<a href="{}">{}</a>', self.django_field.storage.url(value), value
                )
            except Exception as e:
                return str(e)

        return format


class OrmAggregateField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name, name, name.replace("_", " "), type_=type_, concrete=True
        )

    def bind(self, previous):
        assert previous
        queryset_path = previous.queryset_path + [self.name]
        agg_func = _get_django_aggregate(previous.type_, self.name)
        return OrmBoundField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=queryset_path,
            aggregate_clause=(s(queryset_path), agg_func(s(previous.queryset_path))),
            having=True,
        )


class OrmBoundFunctionField(OrmBoundField):
    def _annotate(self, request, qs):
        func = _get_django_function(self.name)[0](s(self.previous.queryset_path))
        return qs.annotate(**{s(self.queryset_path): func})


class OrmFunctionField(OrmBaseField):
    def __init__(self, model_name, name, type_):
        super().__init__(
            model_name,
            name,
            name.replace("_", " "),
            type_=type_,
            concrete=True,
            can_pivot=True,
        )

    def bind(self, previous):
        assert previous
        return OrmBoundFunctionField(
            field=self,
            previous=previous,
            full_path=previous.full_path + [self.name],
            pretty_path=previous.pretty_path + [self.pretty_name],
            queryset_path=previous.queryset_path + [self.name],
            filter_=True,
        )
