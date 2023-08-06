from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User

import pytest

from aleksis.core.apps import CoreConfig
from aleksis.core.util.core_helpers import get_site_preferences

pytestmark = pytest.mark.django_db


class DummyBackend(BaseBackend):
    def authenticate(
        self, request, username: str, password: str, **kwargs
    ) -> Optional[AbstractBaseUser]:
        if username == "foo" and password == "baz":
            return User.objects.get_or_create(username="foo")[0]


backend_name = "aleksis.core.tests.test_authentication_backends.DummyBackend"


def test_backends_simple(settings):

    assert not authenticate(username="foo", password="baz")

    assert backend_name not in settings.AUTHENTICATION_BACKENDS

    settings.AUTHENTICATION_BACKENDS.append(backend_name)
    assert backend_name in settings.AUTHENTICATION_BACKENDS

    assert authenticate(username="foo", password="baz")

    settings.AUTHENTICATION_BACKENDS.remove(backend_name)

    assert not authenticate(username="foo", password="baz")


def test_backends_with_activation(settings):
    assert not authenticate(username="foo", password="baz")

    settings.CUSTOM_AUTHENTICATION_BACKENDS.append(backend_name)

    assert backend_name not in get_site_preferences()["auth__backends"]
    assert backend_name not in settings.AUTHENTICATION_BACKENDS
    assert not authenticate(username="foo", password="baz")

    print(get_site_preferences()["auth__backends"])
    print(get_site_preferences()["auth__backends"].append(backend_name))

    get_site_preferences()["auth__backends"] = [backend_name]

    assert backend_name in get_site_preferences()["auth__backends"]
    assert backend_name in settings.AUTHENTICATION_BACKENDS
    assert authenticate(username="foo", password="baz")

    get_site_preferences()["auth__backends"] = []

    assert backend_name not in get_site_preferences()["auth__backends"]
    assert backend_name not in settings.AUTHENTICATION_BACKENDS
