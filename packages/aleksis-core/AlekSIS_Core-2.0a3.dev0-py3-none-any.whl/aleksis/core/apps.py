from typing import Any, List, Optional, Tuple

import django.apps
from django.conf import settings
from django.db import OperationalError, ProgrammingError
from django.http import HttpRequest
from django.utils.module_loading import autodiscover_modules

from dynamic_preferences.registries import preference_models

from .registries import (
    group_preferences_registry,
    person_preferences_registry,
    site_preferences_registry,
)
from .util.apps import AppConfig
from .util.core_helpers import get_site_preferences, has_person
from .util.sass_helpers import clean_scss


class CoreConfig(AppConfig):
    name = "aleksis.core"
    verbose_name = "AlekSIS — The Free School Information System"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS/",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2017, 2018, 2019, 2020], "Jonathan Weth", "wethjo@katharineum.de"),
        ([2017, 2018, 2019], "Frank Poetzsch-Heffter", "p-h@katharineum.de"),
        ([2018, 2019, 2020], "Julian Leucker", "leuckeju@katharineum.de"),
        ([2018, 2019, 2020], "Hangzhi Yu", "yuha@katharineum.de"),
        ([2019, 2020], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2020], "Tom Teichler", "tom.teichler@teckids.org"),
        ([2019], "mirabilos", "thorsten.glaser@teckids.org"),
    )

    def ready(self):
        super().ready()

        # Autodiscover various modules defined by AlekSIS
        autodiscover_modules("form_extensions", "model_extensions", "checks")

        sitepreferencemodel = self.get_model("SitePreferenceModel")
        personpreferencemodel = self.get_model("PersonPreferenceModel")
        grouppreferencemodel = self.get_model("GroupPreferenceModel")

        preference_models.register(sitepreferencemodel, site_preferences_registry)
        preference_models.register(personpreferencemodel, person_preferences_registry)
        preference_models.register(grouppreferencemodel, group_preferences_registry)

        self._refresh_authentication_backends()

    @classmethod
    def _refresh_authentication_backends(cls):
        """Refresh config list of enabled authentication backends."""
        from .preferences import AuthenticationBackends  # noqa

        idx = settings.AUTHENTICATION_BACKENDS.index("django.contrib.auth.backends.ModelBackend")

        try:
            # Don't set array directly in order to keep object reference
            settings._wrapped.AUTHENTICATION_BACKENDS.clear()
            settings._wrapped.AUTHENTICATION_BACKENDS += settings.ORIGINAL_AUTHENTICATION_BACKENDS

            for backend in get_site_preferences()["auth__backends"]:
                settings._wrapped.AUTHENTICATION_BACKENDS.insert(idx, backend)
                idx += 1
        except (ProgrammingError, OperationalError):
            pass

    def preference_updated(
        self,
        sender: Any,
        section: Optional[str] = None,
        name: Optional[str] = None,
        old_value: Optional[Any] = None,
        new_value: Optional[Any] = None,
        **kwargs,
    ) -> None:
        if section == "auth" and name == "backends":
            self._refresh_authentication_backends()

        if section == "theme":
            if name in ("primary", "secondary"):
                clean_scss()
            elif name in ("favicon", "pwa_icon"):
                from favicon.models import Favicon  # noqa

                is_favicon = name == "favicon"

                if new_value:
                    Favicon.on_site.update_or_create(
                        title=name,
                        defaults={"isFavicon": name == "favicon", "faviconImage": new_value,},
                    )
                else:
                    Favicon.on_site.filter(title=name, isFavicon=is_favicon).delete()

    def post_migrate(
        self,
        app_config: django.apps.AppConfig,
        verbosity: int,
        interactive: bool,
        using: str,
        plan: List[Tuple],
        apps: django.apps.registry.Apps,
        **kwargs,
    ) -> None:
        super().post_migrate(app_config, verbosity, interactive, using, plan, apps)

        # Ensure presence of an OTP YubiKey default config
        apps.get_model("otp_yubikey", "ValidationService").objects.using(using).update_or_create(
            name="default", defaults={"use_ssl": True, "param_sl": "", "param_timeout": ""}
        )

    def user_logged_in(
        self, sender: type, request: Optional[HttpRequest], user: "User", **kwargs
    ) -> None:
        if has_person(user):
            # Save the associated person to pick up defaults
            user.person.save()
