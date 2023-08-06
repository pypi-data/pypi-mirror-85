from typing import Sequence

from django.db.models import Q
from django.utils.translation import gettext as _

from django_filters import CharFilter, FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from material import Layout, Row

from aleksis.core.models import Group, GroupType, Person, SchoolTerm


class MultipleCharFilter(CharFilter):
    """Filter for filtering multiple fields with one input.

    >>> multiple_filter = MultipleCharFilter(["name__icontains", "short_name__icontains"])
    """

    def filter(self, qs, value):  # noqa
        q = None
        for field in self.fields:
            if not q:
                q = Q(**{field: value})
            else:
                q = q | Q(**{field: value})
        return qs.filter(q)

    def __init__(self, fields: Sequence[str], *args, **kwargs):
        self.fields = fields
        super().__init__(self, *args, **kwargs)


class GroupFilter(FilterSet):
    school_term = ModelChoiceFilter(queryset=SchoolTerm.objects.all())
    group_type = ModelChoiceFilter(queryset=GroupType.objects.all())
    parent_groups = ModelMultipleChoiceFilter(queryset=Group.objects.all())

    search = MultipleCharFilter(["name__icontains", "short_name__icontains"], label=_("Search"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.layout = Layout(Row("search"), Row("school_term", "group_type", "parent_groups"))
        self.form.initial = {"school_term": SchoolTerm.current}


class PersonFilter(FilterSet):
    name = MultipleCharFilter(
        [
            "first_name__icontains",
            "additional_name__icontains",
            "last_name__icontains",
            "short_name__icontains",
        ],
        label=_("Search by name"),
    )
    contact = MultipleCharFilter(
        [
            "street__icontains",
            "housenumber__icontains",
            "postal_code__icontains",
            "place__icontains",
            "phone_number__icontains",
            "mobile_number__icontains",
            "email__icontains",
        ],
        label=_("Search by contact details"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.layout = Layout(Row("name", "contact"), Row("is_active", "sex", "primary_group"))

    class Meta:
        model = Person
        fields = ["sex", "is_active", "primary_group"]
