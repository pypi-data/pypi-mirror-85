import pytest

from aleksis.core.models import Person

pytestmark = pytest.mark.django_db


def test_full_name():
    _person = Person.objects.create(first_name="Jane", last_name="Doe")

    assert _person.full_name == "Doe, Jane"
