# flake8: noqa: DJ12

from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Union

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import JSONField, QuerySet
from django.forms.forms import BaseForm
from django.forms.models import ModelForm, ModelFormMetaclass
from django.http import HttpResponse
from django.utils.functional import lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView, ModelFormMixin

import reversion
from easyaudit.models import CRUDEvent
from guardian.admin import GuardedModelAdmin
from jsonstore.fields import IntegerField, JSONFieldMixin
from material.base import Layout, LayoutNode
from rules.contrib.admin import ObjectPermissionsModelAdmin

from aleksis.core.managers import CurrentSiteManagerWithoutMigrations, SchoolTermRelatedQuerySet


class _ExtensibleModelBase(models.base.ModelBase):
    """Ensure predefined behaviour on model creation.

    This metaclass serves the following purposes:

     - Register all AlekSIS models with django-reverseion
    """

    def __new__(mcls, name, bases, attrs):
        mcls = super().__new__(mcls, name, bases, attrs)

        if "Meta" not in attrs or not attrs["Meta"].abstract:
            # Register all non-abstract models with django-reversion
            mcls = reversion.register(mcls)

            mcls.extra_permissions = []

        return mcls


class ExtensibleModel(models.Model, metaclass=_ExtensibleModelBase):
    """Base model for all objects in AlekSIS apps.

    This base model ensures all objects in AlekSIS apps fulfill the
    following properties:

     * crud_events property to retrieve easyaudit's CRUD event log
     * created_at and updated_at properties based n CRUD events
     * Allow injection of fields and code from AlekSIS apps to extend
       model functionality.

    Injection of fields and code
    ============================

    After all apps have been loaded, the code in the `model_extensions` module
    in every app is executed. All code that shall be injected into a model goes there.

    :Example:

    .. code-block:: python

       from datetime import date, timedelta

       from jsonstore import CharField

       from aleksis.core.models import Person

       @Person.property
       def is_cool(self) -> bool:
           return True

       @Person.property
       def age(self) -> timedelta:
           return self.date_of_birth - date.today()

       Person.field(shirt_size=CharField())

    For a more advanced example, using features from the ORM, see AlekSIS-App-Chronos
    and AlekSIS-App-Alsijil.

    :Date: 2019-11-07
    :Authors:
        - Dominik George <dominik.george@teckids.org>
    """

    # Defines a material design icon associated with this type of model
    icon_ = "radio_button_unchecked"

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, default=settings.SITE_ID, editable=False
    )
    objects = CurrentSiteManager()
    objects_all_sites = models.Manager()

    extra_permissions = []

    def get_absolute_url(self) -> str:
        """Get the URL o a view representing this model instance."""
        pass

    @property
    def crud_events(self) -> QuerySet:
        """Get all CRUD events connected to this object from easyaudit."""
        content_type = ContentType.objects.get_for_model(self)

        return CRUDEvent.objects.filter(
            object_id=self.pk, content_type=content_type
        ).select_related("user", "user__person")

    @property
    def crud_event_create(self) -> Optional[CRUDEvent]:
        """Return create event of this object."""
        return self.crud_events.filter(event_type=CRUDEvent.CREATE).latest("datetime")

    @property
    def crud_event_update(self) -> Optional[CRUDEvent]:
        """Return last event of this object."""
        return self.crud_events.latest("datetime")

    @property
    def created_at(self) -> Optional[datetime]:
        """Determine creation timestamp from CRUD log."""
        if self.crud_event_create:
            return self.crud_event_create.datetime

    @property
    def updated_at(self) -> Optional[datetime]:
        """Determine last timestamp from CRUD log."""
        if self.crud_event_update:
            return self.crud_event_update.datetime

    extended_data = JSONField(default=dict, editable=False)

    @property
    def created_by(self) -> Optional[models.Model]:
        """Determine user who created this object from CRUD log."""
        if self.crud_event_create:
            return self.crud_event_create.user

    @property
    def updated_by(self) -> Optional[models.Model]:
        """Determine user who last updated this object from CRUD log."""
        if self.crud_event_update:
            return self.crud_event_update.user

    extended_data = JSONField(default=dict, editable=False)

    @classmethod
    def _safe_add(cls, obj: Any, name: Optional[str]) -> None:
        # Decide the name for the attribute
        if name is None:
            prop_name = obj.__name__
        else:
            if name.isidentifier():
                prop_name = name
            else:
                raise ValueError(f"{name} is not a valid name.")

        # Verify that attribute name does not clash with other names in the class
        if hasattr(cls, prop_name):
            raise ValueError(f"{prop_name} already used.")

        # Let Django's model magic add the attribute if we got here
        cls.add_to_class(name, obj)

    @classmethod
    def property_(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """Add the passed callable as a property."""
        cls._safe_add(property(func), name or func.__name__)

    @classmethod
    def method(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """Add the passed callable as a method."""
        cls._safe_add(func, name or func.__name__)

    @classmethod
    def class_method(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """Add the passed callable as a classmethod."""
        cls._safe_add(classmethod(func), name or func.__name__)

    @classmethod
    def field(cls, **kwargs) -> None:
        """Add the passed jsonstore field. Must be one of the fields in django-jsonstore.

        Accepts exactly one keyword argument, with the name being the desired
        model field name and the value the field instance.
        """
        # Force kwargs to be exactly one argument
        if len(kwargs) != 1:
            raise TypeError(f"field() takes 1 keyword argument but {len(kwargs)} were given")
        name, field = kwargs.popitem()

        # Force the field to be one of the jsonstore fields
        if JSONFieldMixin not in field.__class__.__mro__:
            raise TypeError("Only jsonstore fields can be added to models.")

        # Force use of the one JSONField defined in this mixin
        field.json_field_name = "extended_data"

        cls._safe_add(field, name)

    @classmethod
    def foreign_key(
        cls,
        field_name: str,
        to: models.Model,
        to_field: str = "pk",
        to_field_type: JSONFieldMixin = IntegerField,
        related_name: Optional[str] = None,
    ) -> None:
        """Add a virtual ForeignKey.

        This works by storing the primary key (or any field passed in the to_field argument)
        and adding a property that queries the desired model.

        If the foreign model also is an ExtensibleModel, a reverse mapping is also added under
        the related_name passed as argument, or this model's default related name.
        """

        id_field_name = f"{field_name}_id"
        if related_name is None:
            related_name = cls.Meta.default_related_name

        # Add field to hold key to foreign model
        id_field = to_field_type(blank=True, null=True)
        cls.field(**{id_field_name: id_field})

        @property
        def _virtual_fk(self) -> Optional[models.Model]:
            id_field_val = getattr(self, id_field_name)
            if id_field_val:
                try:
                    return to.objects.get(**{to_field: id_field_val})
                except to.DoesNotExist:
                    # We found a stale foreign key
                    setattr(self, id_field_name, None)
                    self.save()
                    return None
            else:
                return None

        @_virtual_fk.setter
        def _virtual_fk(self, value: Optional[models.Model] = None) -> None:
            if value is None:
                id_field_val = None
            else:
                id_field_val = getattr(value, to_field)
            setattr(self, id_field_name, id_field_val)

        # Add property to wrap get/set on foreign model instance
        cls._safe_add(_virtual_fk, field_name)

        # Add related property on foreign model instance if it provides such an interface
        if hasattr(to, "_safe_add"):

            def _virtual_related(self) -> models.QuerySet:
                id_field_val = getattr(self, to_field)
                return cls.objects.filter(**{id_field_name: id_field_val})

            to.property_(_virtual_related, related_name)

    @classmethod
    def syncable_fields(cls) -> List[models.Field]:
        """Collect all fields that can be synced on a model."""
        return [
            field
            for field in cls._meta.fields
            if (field.editable and not field.auto_created and not field.is_relation)
        ]

    @classmethod
    def syncable_fields_choices(cls) -> Tuple[Tuple[str, str]]:
        """Collect all fields that can be synced on a model."""
        return tuple(
            [(field.name, field.verbose_name or field.name) for field in cls.syncable_fields()]
        )

    @classmethod
    def syncable_fields_choices_lazy(cls) -> Callable[[], Tuple[Tuple[str, str]]]:
        """Collect all fields that can be synced on a model."""
        return lazy(cls.syncable_fields_choices, tuple)

    @classmethod
    def add_permission(cls, name: str, verbose_name: str):
        """Dynamically add a new permission to a model."""
        cls.extra_permissions.append((name, verbose_name))

    class Meta:
        abstract = True


class PureDjangoModel(object):
    """No-op mixin to mark a model as deliberately not using ExtensibleModel."""

    pass


class _ExtensibleFormMetaclass(ModelFormMetaclass):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)

        # Enforce a default for the base layout for forms that o not specify one
        if hasattr(x, "layout"):
            base_layout = x.layout.elements
        else:
            base_layout = []

        x.base_layout = base_layout
        x.layout = Layout(*base_layout)

        return x


class ExtensibleForm(ModelForm, metaclass=_ExtensibleFormMetaclass):
    """Base model for extensible forms.

    This mixin adds functionality which allows
    - apps to add layout nodes to the layout used by django-material

    Add layout nodes
    ================

    ```
    from material import Fieldset

    from aleksis.core.forms import ExampleForm

    node = Fieldset("field_name")
    ExampleForm.add_node_to_layout(node)
    ```

    """

    @classmethod
    def add_node_to_layout(cls, node: Union[LayoutNode, str]):
        """Add a node to `layout` attribute.

        :param node: django-material layout node (Fieldset, Row etc.)
        :type node: LayoutNode
        """
        cls.base_layout.append(node)
        cls.layout = Layout(*cls.base_layout)


class BaseModelAdmin(GuardedModelAdmin, ObjectPermissionsModelAdmin):
    """A base class for ModelAdmin combining django-guardian and rules."""

    pass


class SuccessMessageMixin(ModelFormMixin):
    success_message: Optional[str] = None

    def form_valid(self, form: BaseForm) -> HttpResponse:
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AdvancedCreateView(SuccessMessageMixin, CreateView):
    pass


class AdvancedEditView(SuccessMessageMixin, UpdateView):
    pass


class AdvancedDeleteView(DeleteView):
    """Common confirm view for deleting.

    .. warning ::

        Using this view, objects are deleted permanently after confirming.
        We recommend to include the mixin :class:`reversion.views.RevisionMixin`
        from `django-reversion` to enable soft-delete.
    """

    success_message: Optional[str] = None

    def delete(self, request, *args, **kwargs):
        r = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return r


class SchoolTermRelatedExtensibleModel(ExtensibleModel):
    """Add relation to school term."""

    objects = CurrentSiteManagerWithoutMigrations.from_queryset(SchoolTermRelatedQuerySet)()

    school_term = models.ForeignKey(
        "core.SchoolTerm",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Linked school term"),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class SchoolTermRelatedExtensibleForm(ExtensibleForm):
    """Extensible form for school term related data.

    .. warning::
        This doesn't automatically include the field `school_term` in `fields` or `layout`,
        it just sets an initial value.
    """

    def __init__(self, *args, **kwargs):
        from aleksis.core.models import SchoolTerm  # noqa

        if "instance" not in kwargs:
            kwargs["initial"] = {"school_term": SchoolTerm.current}

        super().__init__(*args, **kwargs)
